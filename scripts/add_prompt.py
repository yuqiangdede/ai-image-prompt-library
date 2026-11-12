#!/usr/bin/env python3
"""Add a text Prompt to the gallery from a repository owner's GitHub Issue.

The gallery is static, so the browser only prepares a prefilled Issue form.
This script turns the confirmed Issue into library/prompts/<slug>/.
"""
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import date, datetime, timezone
from pathlib import Path

try:  # imported from the repository root (CI validation, tests)
    from scripts.manage_skill import (
        attachment_urls,
        check_linked_image,
        fetch_upload,
        image_extension,
        linked_image_url,
    )
except ImportError:  # run as `python scripts/add_prompt.py`
    from manage_skill import (
        attachment_urls,
        check_linked_image,
        fetch_upload,
        image_extension,
        linked_image_url,
    )

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "library" / "prompts"
REPO = os.environ.get("GITHUB_REPOSITORY", "yuqiangdede/ai-image-prompt-library")

TITLE_PREFIX = "[添加提示词]"

# Keep these headings unique: the script splits the Issue body on them, and a
# prompt may itself contain ordinary "### " Markdown headings.
LABELS = {
    "title": "标题（显示名称）",
    "description": "简介（卡片说明）",
    "category": "分类（主题）",
    "tags": "标签（用逗号分隔）",
    "model": "适用模型",
    "prompt": "提示词正文（原样写入 prompt.md）",
    "cover_url": "封面图地址（GitHub 图片链接）",
    "cover_file": "上传封面图（没有链接时使用）",
    "slug": "目录标识（slug，可留空自动生成）",
    "confirm": "确认",
}
HEADINGS = {label: key for key, label in LABELS.items()}

MAX_TITLE_CHARS = 80
MAX_DESCRIPTION_CHARS = 300
MAX_CATEGORY_CHARS = 40
MAX_MODEL_CHARS = 40
MAX_TAG_CHARS = 30
MAX_TAGS = 8
MAX_PROMPT_CHARS = 20000
MAX_BODY_CHARS = 120000
MAX_SLUG_CHARS = 60


def parse_issue_body(body):
    """Split a form body on the known headings only, preserving prompt headings."""
    values = {key: [] for key in LABELS}
    current = None
    for line in (body or "").splitlines():
        stripped = line.strip()
        if stripped.startswith("### "):
            key = HEADINGS.get(stripped[4:].strip())
            if key:
                current = key
                continue
        if current:
            values[current].append(line)
    return {key: "\n".join(lines).strip() for key, lines in values.items()}


def clean_line(value, label, maximum):
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if not text:
        raise ValueError("请填写" + label)
    if len(text) > maximum:
        raise ValueError("{}不能超过 {} 个字符".format(label, maximum))
    return text


def normalize_tags(value):
    tags = []
    for raw in re.split(r"[,，、\n]+", str(value or "")):
        tag = raw.strip().lstrip("#").strip()
        if not tag:
            continue
        if len(tag) > MAX_TAG_CHARS:
            raise ValueError("单个标签不能超过 {} 个字符：{}".format(MAX_TAG_CHARS, tag))
        if tag not in tags:
            tags.append(tag)
    if len(tags) > MAX_TAGS:
        raise ValueError("标签最多 {} 个".format(MAX_TAGS))
    return tags


def normalize_prompt(value):
    text = str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    if not text.strip():
        raise ValueError("请填写提示词正文")
    if len(text) > MAX_PROMPT_CHARS:
        raise ValueError("提示词正文不能超过 {} 个字符".format(MAX_PROMPT_CHARS))
    return text + "\n"


def explicit_slug(value):
    slug = str(value or "").strip().strip("`").strip()
    if not slug:
        return ""
    if len(slug) > MAX_SLUG_CHARS or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError(
            "目录标识只允许小写字母、数字和单个连字符，最长 {} 个字符".format(MAX_SLUG_CHARS))
    return slug


def generated_slug(title, prompt):
    digest = hashlib.sha1((title + "\n" + prompt).encode("utf-8")).hexdigest()[:6]
    return "prompt-{}-{}".format(datetime.now(timezone.utc).strftime("%Y%m%d"), digest)


def resolve_cover(sections):
    """Return ("file", bytes, extension) for an upload, or ("url", url)."""
    uploaded = attachment_urls(sections.get("cover_file", ""))
    if uploaded:
        data = fetch_upload(uploaded[0])
        return "file", data, image_extension(data)
    linked_text = str(sections.get("cover_url") or "").strip().strip("`").strip()
    if not linked_text:
        raise ValueError("封面为必填：请填写封面图地址，或在 Issue 中上传一张封面图")
    linked = linked_image_url(linked_text)
    if not linked:
        raise ValueError(
            "封面图地址必须是 GitHub 图片链接（raw.githubusercontent.com，或 "
            "github.com 的 raw/blob / user-attachments 链接）")
    if linked.startswith("https://github.com/user-attachments/"):
        data = fetch_upload(linked)
        return "file", data, image_extension(data)
    check_linked_image(linked)
    return "url", linked


def add_prompt(sections):
    title = clean_line(sections.get("title"), "标题", MAX_TITLE_CHARS)
    description = clean_line(sections.get("description"), "简介", MAX_DESCRIPTION_CHARS)
    category = clean_line(sections.get("category"), "分类", MAX_CATEGORY_CHARS)
    tags = normalize_tags(sections.get("tags"))
    model = str(sections.get("model") or "").strip()
    model = clean_line(model, "适用模型", MAX_MODEL_CHARS) if model else "ChatGPT"
    prompt = normalize_prompt(sections.get("prompt"))
    slug = explicit_slug(sections.get("slug"))

    PROMPTS.mkdir(parents=True, exist_ok=True)
    if not slug:
        base = generated_slug(title, prompt)
        slug = base
        suffix = 2
        while (PROMPTS / slug).exists():
            slug = "{}-{}".format(base, suffix)
            suffix += 1
    folder = PROMPTS / slug
    if folder.exists():
        raise ValueError("图库中已存在同名条目：{}；请换一个目录标识".format(slug))

    cover = resolve_cover(sections)
    try:
        folder.mkdir(parents=True)
    except FileExistsError:
        raise ValueError("图库中已存在同名条目：{}".format(slug)) from None
    try:
        if cover[0] == "file":
            _, data, extension = cover
            images = folder / "images"
            images.mkdir(parents=True, exist_ok=True)
            (images / ("cover" + extension)).write_bytes(data)
            cover_ref = "images/cover" + extension
        else:
            cover_ref = cover[1]
        metadata = {
            "title": title,
            "description": description,
            "category": category,
            "tags": tags,
            "model": model,
            "updated_at": date.today().isoformat(),
            "cover": cover_ref,
            "images": [cover_ref],
            "related_skills": [],
        }
        (folder / "meta.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (folder / "prompt.md").write_text(prompt, encoding="utf-8")
    except Exception:
        shutil.rmtree(folder, ignore_errors=True)
        raise
    return slug, title


def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise ValueError("只能由仓库 GitHub Actions Issue 工作流触发")
    issue = json.loads(Path(event_path).read_text(encoding="utf-8")).get("issue") or {}
    actor = (issue.get("user") or {}).get("login")
    if actor != REPO.split("/")[0]:
        raise PermissionError("仅允许仓库所有者提交添加提示词任务")
    title = (issue.get("title") or "").strip()
    if not title.startswith(TITLE_PREFIX):
        raise ValueError("Issue 标题必须以 {} 开头".format(TITLE_PREFIX))
    body = issue.get("body") or ""
    if len(body) > MAX_BODY_CHARS:
        raise ValueError("Issue 内容过长")
    sections = parse_issue_body(body)
    if not re.search(r"^\s*-\s*\[[xX]\]", sections.get("confirm", ""), re.M):
        raise PermissionError("请先勾选「确认」再提交")
    slug, prompt_title = add_prompt(sections)
    print("Added prompt {}: {}".format(slug, prompt_title))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("ERROR:", str(exc), file=sys.stderr)
        raise
