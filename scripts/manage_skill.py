#!/usr/bin/env python3
"""Apply gallery metadata/image changes or delete a Skill from an owner's GitHub Issue."""
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "library" / "skills"
PROMPTS = ROOT / "library" / "prompts"
REPO = os.environ.get("GITHUB_REPOSITORY", "yuqiangdede/ai-image-prompt-library")
USER_AGENT = "ai-image-prompt-library"

EDIT_TITLE = "[修改素材]"
LEGACY_EDIT_TITLE = "[修改图片]"
DELETE_TITLE = "[删除 Skill]"

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg")
MAX_IMAGE_BYTES = 8_000_000
MAX_TOTAL_BYTES = 32_000_000
MAX_NEW_IMAGES = 10

LABELS = {
    "slug": "素材标识（slug）",
    "kind": "素材类型",
    "title": "标题（显示名称）",
    "description": "简介",
    "category": "分类",
    "tags": "标签（逗号分隔）",
    "keep": "保留的现有图片",
    "cover": "封面图片地址",
    "urls": "新增图片地址",
    "files": "上传新图片",
    "confirm": "确认",
}

URL_RE = re.compile(r"https://[^\s<>()\[\]\"']+")
MD_IMAGE_RE = re.compile(r"!\[[^\]]*\]\((https://[^)\s]+)\)")
HTML_IMAGE_RE = re.compile(r"<img\b[^>]*\bsrc\s*=\s*[\"'](https://[^\"']+)[\"']", re.I)


def parse_sections(body):
    """Turn a GitHub issue-form body into {heading: value}."""
    sections = {}
    heading = None
    lines = []
    for line in (body or "").splitlines():
        if line.startswith("### "):
            if heading is not None:
                sections[heading] = "\n".join(lines).strip()
            heading = line[4:].strip()
            lines = []
        elif heading is not None:
            lines.append(line)
    if heading is not None:
        sections[heading] = "\n".join(lines).strip()
    return sections


def section_value(sections, prefix):
    for heading, value in sections.items():
        if heading.startswith(prefix):
            text = value.strip()
            if text in ("No response", "_No response_"):
                return ""
            return text
    return ""


def text_refs(text):
    refs = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^[-*+]\s+", "", line).strip().strip("`").strip()
        if line in ("", "No response", "_No response_"):
            continue
        refs.append(line)
    return refs


def is_attachment(url):
    parts = urlsplit(url)
    return (
        parts.scheme == "https"
        and parts.hostname == "github.com"
        and re.match(r"^/user-attachments/(assets|files)/[A-Za-z0-9-]+", parts.path or "") is not None
    )


def linked_image_url(url):
    """Return a directly usable GitHub image URL, or None."""
    parts = urlsplit((url or "").strip())
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
        return None
    if parts.hostname == "raw.githubusercontent.com":
        return url.strip()
    if parts.hostname != "github.com":
        return None
    if is_attachment(url):
        return url.strip()
    segments = [segment for segment in parts.path.split("/") if segment]
    if len(segments) >= 5 and segments[2] in ("blob", "raw"):
        owner, repo, _, branch, *rest = segments
        if not (re.fullmatch(r"[A-Za-z0-9_.-]+", owner) and re.fullmatch(r"[A-Za-z0-9_.-]+", repo)):
            return None
        converted = "https://raw.githubusercontent.com/{}/{}/{}/{}".format(
            owner, repo, branch, "/".join(rest))
        if parts.query:
            converted += "?" + parts.query
        return converted
    return None


def attachment_urls(text):
    candidates = MD_IMAGE_RE.findall(text or "") + HTML_IMAGE_RE.findall(text or "") + URL_RE.findall(text or "")
    found = []
    for raw in candidates:
        url = raw.rstrip(".,;:!?…。，；：！？")
        if is_attachment(url) and url not in found:
            found.append(url)
    return found


def image_extension(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return ".gif"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp"
    raise ValueError("上传的文件不是 PNG、JPG、WebP 或 GIF 图片")


def fetch_upload(url):
    if not is_attachment(url):
        raise ValueError("不支持的图片上传地址：" + url)
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "image/*,*/*;q=0.8"})
    with urlopen(request, timeout=30) as response:
        data = response.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("单张图片不能超过 8 MB")
    return data


def check_linked_image(url):
    request = Request(url, method="HEAD", headers={"User-Agent": USER_AGENT, "Accept": "image/*"})
    try:
        with urlopen(request, timeout=20) as response:
            content_type = (response.headers.get("Content-Type") or "").split(";")[0].strip().lower()
    except Exception as exc:
        raise ValueError("无法读取图片地址：{}（{}）".format(url, exc)) from exc
    if not content_type.startswith("image/"):
        raise ValueError("图片地址返回的不是图片：{}".format(url))


def item_folder(slug, kind="skill"):
    slug = (slug or "").strip()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("素材标识无效：{}（只允许小写字母、数字和连字符）".format(slug or "空"))
    if kind not in ("skill", "prompt"):
        raise ValueError("未知素材类型：" + kind)
    base = SKILLS if kind == "skill" else PROMPTS
    folder = (base / slug).resolve()
    if folder.parent != base.resolve() or not folder.is_dir():
        raise ValueError("图库中不存在 {}：{}".format(kind, slug))
    if not (folder / "meta.json").is_file():
        raise ValueError("素材缺少 meta.json：" + slug)
    return folder


def skill_folder(slug):
    return item_folder(slug, "skill")


def load_meta(folder):
    return json.loads((folder / "meta.json").read_text(encoding="utf-8"))


def write_meta(folder, meta):
    (folder / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_ref(ref, slug, folder):
    """Turn a catalog path or GitHub URL into a meta.json image reference."""
    ref = (ref or "").strip().strip("`").strip()
    if not ref:
        raise ValueError("图片地址为空")
    if ref.startswith("https://"):
        linked = linked_image_url(ref)
        if not linked:
            raise ValueError("只支持 GitHub 图片地址：" + ref)
        return linked
    if ref.startswith(("http://", "data:", "//")):
        raise ValueError("只支持 HTTPS 图片地址：" + ref)
    prefix = "library/{}/{}/".format(folder.parent.name, slug)
    if ref.startswith(prefix):
        ref = ref[len(prefix):]
    if ref.startswith("./"):
        ref = ref[2:]
    target = (folder / ref).resolve()
    if not target.is_relative_to(folder.resolve()) or not target.is_file():
        raise ValueError("图片不在该 Skill 目录中：" + ref)
    if target.suffix.lower() not in IMAGE_EXTENSIONS:
        raise ValueError("图片格式不受支持：" + ref)
    return target.relative_to(folder).as_posix()


def save_upload(folder, url):
    data = fetch_upload(url)
    extension = image_extension(data)
    digest = hashlib.sha256(data).hexdigest()[:16]
    images_dir = folder / "images"
    if images_dir.is_symlink():
        raise ValueError("素材的 images 目录是符号链接，已拒绝写入")
    target = images_dir / ("upload-" + digest + extension)
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return "images/" + target.name, len(data)


def keep_all_refs(meta, slug, folder):
    refs = []
    for ref in list(meta.get("images") or []) + ([meta["cover"]] if meta.get("cover") else []):
        try:
            normalized = normalize_ref(ref, slug, folder)
        except ValueError:
            continue
        if normalized not in refs:
            refs.append(normalized)
    return refs


def edit_metadata(sections, meta):
    """Only update metadata fields present in the new edit form."""
    for field, maximum in (("title", 80), ("description", 300), ("category", 40)):
        label = LABELS[field]
        if not any(heading.startswith(label) for heading in sections):
            continue
        value = re.sub(r"\s+", " ", section_value(sections, label)).strip()
        if not value:
            raise ValueError("请填写" + label)
        if len(value) > maximum:
            raise ValueError("{}不能超过 {} 字".format(label, maximum))
        meta[field] = value
    if any(heading.startswith(LABELS["tags"]) for heading in sections):
        raw_tags = section_value(sections, LABELS["tags"])
        tags = []
        for raw in re.split(r"[,，、\n]+", raw_tags):
            tag = raw.strip().lstrip("#").strip()
            if not tag:
                continue
            if len(tag) > 30:
                raise ValueError("单个标签不能超过 30 字")
            if tag not in tags:
                tags.append(tag)
        if len(tags) > 24:
            raise ValueError("标签最多 24 个")
        meta["tags"] = tags


def edit_images(sections, slug, kind="skill"):
    folder = item_folder(slug, kind)
    meta = load_meta(folder)

    keep_text = section_value(sections, LABELS["keep"])
    keep_refs = text_refs(keep_text)
    if not keep_text:
        kept = keep_all_refs(meta, slug, folder)
    elif keep_refs and all(ref.lower() in ("无", "none") for ref in keep_refs):
        kept = []
    else:
        kept = []
        for ref in keep_refs:
            normalized = normalize_ref(ref, slug, folder)
            if normalized not in kept:
                kept.append(normalized)

    added = []
    uploaded = []
    upload_map = {}
    total_bytes = 0

    def add_upload(url):
        nonlocal total_bytes
        normalized, size = save_upload(folder, url)
        upload_map[url] = normalized
        total_bytes += size
        if total_bytes > MAX_TOTAL_BYTES:
            raise ValueError("本次上传图片总计不能超过 32 MB")
        if normalized not in kept and normalized not in added and normalized not in uploaded:
            uploaded.append(normalized)
        return normalized

    new_refs = [ref for ref in text_refs(section_value(sections, LABELS["urls"]))
                if ref.lower() not in ("无", "none")]
    files_text = section_value(sections, LABELS["files"])
    upload_urls = attachment_urls(files_text)
    if files_text and not upload_urls:
        raise ValueError("未能识别上传的图片，请重新提交或在「新增图片地址」中填写图片链接")
    if len(new_refs) + len(upload_urls) > MAX_NEW_IMAGES:
        raise ValueError("每次最多新增 {} 张图片".format(MAX_NEW_IMAGES))
    for ref in new_refs:
        normalized = normalize_ref(ref, slug, folder)
        if is_attachment(normalized):
            add_upload(normalized)
            continue
        if not normalized.startswith("https://"):
            raise ValueError("新增图片地址请填写 GitHub 图片链接，本地上传请使用上传字段")
        check_linked_image(normalized)
        if normalized not in kept and normalized not in added:
            added.append(normalized)
    for url in upload_urls:
        add_upload(url)

    final = kept + added + uploaded

    cover_refs = text_refs(section_value(sections, LABELS["cover"]))
    cover = ""
    if cover_refs:
        cover = normalize_ref(cover_refs[0], slug, folder)
        cover = upload_map.get(cover, cover)
        if cover not in final:
            raise ValueError("封面必须是保留或新增的图片之一")
    if not cover and added:
        cover = added[0]
    if not cover and uploaded:
        cover = uploaded[0]
    if not cover and final:
        cover = final[0]

    meta["images"] = final
    meta["cover"] = cover
    edit_metadata(sections, meta)
    meta["updated_at"] = date.today().isoformat()
    write_meta(folder, meta)
    print("Updated {}: {} images, cover={}".format(slug, len(final), cover or "(none)"))


def delete_skill(sections, slug):
    if not re.search(r"^\s*-\s*\[[xX]\]", section_value(sections, LABELS["confirm"]), re.M):
        raise PermissionError("删除操作需要先勾选确认")
    folder = skill_folder(slug)
    shutil.rmtree(folder)
    unlinked = 0
    for base in (PROMPTS, SKILLS):
        if not base.exists():
            continue
        for meta_path in base.glob("*/meta.json"):
            if not meta_path.parent.is_dir():
                continue
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            related = meta.get("related_skills")
            if isinstance(related, list) and slug in related:
                meta["related_skills"] = [item for item in related if item != slug]
                write_meta(meta_path.parent, meta)
                unlinked += 1
    print("Deleted {} (unlinked from {} item(s))".format(slug, unlinked))


def issue_request():
    path = os.environ.get("GITHUB_EVENT_PATH")
    if not path:
        raise ValueError("只能由仓库 GitHub Actions Issue 工作流触发")
    issue = json.loads(Path(path).read_text(encoding="utf-8")).get("issue") or {}
    actor = (issue.get("user") or {}).get("login")
    if actor != REPO.split("/")[0]:
        raise PermissionError("仅允许仓库所有者提交管理任务")
    title = (issue.get("title") or "").strip()
    sections = parse_sections(issue.get("body") or "")
    slug_text = section_value(sections, LABELS["slug"]) or section_value(sections, "Skill 标识")
    slug = slug_text.splitlines()[0].strip().strip("`").strip() if slug_text else ""
    if not slug:
        for prefix in (EDIT_TITLE, LEGACY_EDIT_TITLE, DELETE_TITLE):
            if title.startswith(prefix):
                slug = title[len(prefix):].strip()
                break
    kind = section_value(sections, LABELS["kind"]).strip().lower() or "skill"
    if kind not in ("skill", "prompt"):
        raise ValueError("素材类型只能是 skill 或 prompt")
    return title, sections, slug, kind


def main():
    title, sections, slug, kind = issue_request()
    if title.startswith(EDIT_TITLE) or title.startswith(LEGACY_EDIT_TITLE):
        edit_images(sections, slug, kind)
    elif title.startswith(DELETE_TITLE):
        delete_skill(sections, slug)
    else:
        raise ValueError("未知的管理请求：" + title)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("ERROR:", str(exc), file=sys.stderr)
        raise
