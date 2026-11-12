#!/usr/bin/env python3
"""Add a public GitHub Agent Skill to the gallery without mirroring its code."""
import base64
import json
import os
import posixpath
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "library" / "skills"
REPO = os.environ.get("GITHUB_REPOSITORY", "yuqiangdede/ai-image-prompt-library")
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif")


def api(url):
    if urlsplit(url).hostname != "api.github.com":
        raise ValueError("Invalid API host")
    headers = {"User-Agent": "ai-image-prompt-library", "Accept": "application/vnd.github+json"}
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request(url, headers=headers), timeout=25) as response:
        data = response.read(8_000_001)
    if len(data) > 8_000_000:
        raise ValueError("Upstream metadata too large")
    return json.loads(data)


def parse_url(raw):
    u = urlsplit(raw.strip())
    if u.scheme != "https" or u.hostname != "github.com" or u.username or u.password:
        raise ValueError("请填写 https://github.com/作者/仓库")
    parts = [unquote(p) for p in u.path.strip("/").split("/")]
    if len(parts) < 2:
        raise ValueError("GitHub 仓库地址不完整")
    owner, repo = parts[:2]
    repo = re.sub(r"\.git$", "", repo)
    if not all(re.fullmatch(r"[A-Za-z0-9_.-]+", s) and s not in (".", "..") for s in (owner, repo)):
        raise ValueError("GitHub 仓库地址无效")
    extra = parts[2:]
    if extra and (len(extra) < 3 or extra[0] not in ("tree", "blob")):
        raise ValueError("请提供仓库首页或具体 SKILL.md 文件链接")
    return owner, repo, extra


def read_source(owner, repo, commit, filename):
    url = "https://api.github.com/repos/{}/{}/contents/{}?ref={}".format(
        owner, repo, quote(filename, safe="/"), commit)
    result = api(url)
    if result.get("type") != "file" or result.get("size", 0) > 400000 or result.get("encoding") != "base64":
        raise ValueError("上游文件无法读取或过大：" + filename)
    return base64.b64decode(result["content"]).decode("utf-8-sig", "replace")


def frontmatter(text):
    match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
    if not match:
        return {}
    fields = {}
    for line in match.group(1).splitlines():
        part = re.match(r"^(name|description):\s*(.*)", line)
        if part:
            fields[part.group(1)] = part.group(2).strip().strip("\"'")
    return fields


def sanitize(text):
    text = re.sub(r"!\[[^]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", re.sub(r"[*_#|>]", "", text)).strip()


def readme_details(readme, fallback_title, fallback_desc):
    title = fallback_title
    candidates = []
    fenced = False
    for line in readme.splitlines():
        t = line.strip()
        if t.startswith(chr(96) * 3):
            fenced = not fenced
            continue
        if fenced:
            continue
        if t.startswith("# ") and title == fallback_title:
            name = sanitize(t[2:])
            if name and len(name) <= 75:
                title = name
        if not t or t.startswith(("#", "!", "-", "*", "|", "[", "<", ">")):
            continue
        clean = sanitize(t)
        if len(clean) >= 20:
            candidates.append(clean)
    chinese = [s for s in candidates if re.search(r"[\u4e00-\u9fff]", s)]
    desc = (chinese or candidates or [fallback_desc])[0]
    return title, desc[:170] + ("…" if len(desc) > 170 else "")


def find_image(readmes, paths, owner, repo, branch):
    found = []
    for filename, text in readmes:
        matches = re.findall(r"!\[[^\]]*\]\(([^)\s]+)", text)
        matches += re.findall(r"<img\b[^>]*\bsrc\s*=\s*['\"]([^'\"]+)['\"]", text, re.I)
        for candidate in matches:
            candidate = unquote(candidate.strip("<>\"'").split("?")[0].split("#")[0])
            if not candidate or candidate.startswith(("https:", "http:", "/", "data:")):
                continue
            path = posixpath.normpath(posixpath.join(posixpath.dirname(filename), candidate))
            if path in paths and path.lower().endswith(IMAGE_EXTENSIONS):
                found.append(path)
    if not found:
        found = [p for p in sorted(paths) if p.lower().endswith(IMAGE_EXTENSIONS)
                 and any(w in posixpath.basename(p).lower() for w in ("cover", "hero", "preview", "showcase"))]
    if not found:
        return ""
    return "https://raw.githubusercontent.com/{}/{}/{}/{}".format(
        owner, repo, quote(branch, safe="/"), quote(found[0], safe="/"))


def select_entry(paths, branch, extra):
    options = sorted(p for p in paths if p.rsplit("/", 1)[-1].lower() == "skill.md")
    if not options:
        raise ValueError("该仓库未发现 SKILL.md")
    if extra:
        remainder = "/".join(extra[1:])
        if not (remainder == branch or remainder.startswith(branch + "/")):
            raise ValueError("文件链接必须使用原仓库默认分支")
        hint = remainder[len(branch):].strip("/")
        if extra[0] == "blob":
            if hint not in options:
                raise ValueError("指定的 SKILL.md 不存在")
            return hint
        options = [p for p in options if p.startswith(hint.rstrip("/") + "/")]
        if len(options) != 1:
            raise ValueError("目录内包含 {} 个 Skill，请链接具体 SKILL.md".format(len(options)))
        return options[0]
    if "SKILL.md" in options:
        return "SKILL.md"
    if len(options) != 1:
        raise ValueError("仓库包含 {} 个 Skill，请粘贴具体 SKILL.md 的链接".format(len(options)))
    return options[0]


def import_repository(url):
    owner, repo, extra = parse_url(url)
    base = "https://api.github.com/repos/{}/{}".format(owner, repo)
    info = api(base)
    if info.get("private") or info.get("archived") or info.get("disabled"):
        raise ValueError("只支持公开且未归档的仓库")
    branch = info["default_branch"]
    sha = api(base + "/commits/" + quote(branch, safe=""))["sha"]
    tree = api(base + "/git/trees/{}?recursive=1".format(sha))
    if tree.get("truncated"):
        raise ValueError("上游文件树过大，无法安全扫描")
    paths = {x["path"] for x in tree.get("tree", []) if x.get("type") == "blob"}
    entry = select_entry(paths, branch, extra)
    original = read_source(owner, repo, sha, entry)
    fm = frontmatter(original)
    name = fm.get("name", "")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,70}", name):
        name = posixpath.basename(posixpath.dirname(entry)) if "/" in entry else repo
    readme_paths = [posixpath.join(posixpath.dirname(entry), "README.md"), "README.md", "README.zh.md"]
    readmes = [(p, read_source(owner, repo, sha, p)) for p in dict.fromkeys(readme_paths) if p in paths]
    readme = next((text for p, text in readmes if p == "README.md"), readmes[0][1] if readmes else "")
    title, desc = readme_details(readme, name.replace("-", " ").title(), fm.get("description") or name)
    subject = (title + " " + desc + " " + fm.get("description", "")).lower()
    if any(x in subject for x in ("海报", "poster", "typography", "平面设计")):
        category, tags = "平面设计 / 海报", ["海报", "平面设计"]
    elif any(x in subject for x in ("image", "图片", "图像", "绘图", "生成图")):
        category, tags = "图像生成 / 编辑", ["生图", "图像编辑"]
    elif any(x in subject for x in ("video", "视频", "分镜")):
        category, tags = "视频 / 分镜", ["视频", "分镜"]
    else:
        category, tags = "综合 Skill", ["Agent Skill", "GitHub"]
    cover = find_image(readmes, paths, owner, repo, branch)
    upstream = "https://github.com/{}/{}".format(owner, repo)
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60] or "external-skill"
    if (SKILLS / slug).exists():
        existing = SKILLS / slug / "upstream.json"
        if existing.exists() and json.loads(existing.read_text(encoding="utf-8")).get("url") == upstream:
            raise ValueError("图库中已经存在相同 Skill：" + slug)
        slug = re.sub(r"[^a-z0-9]+", "-", (owner + "-" + name).lower()).strip("-")[:60]
    folder = SKILLS / slug
    if folder.exists():
        raise ValueError("目录名称冲突：" + slug)
    folder.mkdir(parents=True)
    today = date.today().isoformat()
    cmd = "npx skills add {} --skill {}".format(upstream, name)
    metadata = {
        "title": title, "description": desc, "category": category, "tags": tags,
        "model": "ChatGPT", "updated_at": today, "cover": cover,
        "images": [cover] if cover else [], "related_skills": [],
        "external_only": True, "install_command": cmd
    }
    source = {
        "url": upstream, "branch": branch, "sha": sha, "last_synced": today,
        "sync_mode": "link-only", "entry": entry,
        "image_license": "Upstream asset links only; no third-party source files mirrored"
    }
    entry_url = upstream + "/blob/" + quote(branch, safe="/") + "/" + quote(entry, safe="/")
    notes = (
        "# " + title + "（图库自动生成的外部索引）\n\n"
        + "**上游项目**：" + upstream + "\n\n"
        + "**完整 SKILL.md**：" + entry_url + "\n\n"
        + "**简介**：" + desc + "\n\n"
        + "## 安装\n\n" + chr(96)*3 + "bash\n" + cmd + "\n" + chr(96)*3 + "\n\n"
        + "本页面仅索引原始 Skill；未复制上游完整文件。"
        + "在支持 Skills 的 Agent 中运行安装命令，按原作者许可使用。\n"
    )
    for filename, text in (
        ("meta.json", json.dumps(metadata, ensure_ascii=False, indent=2) + "\n"),
        ("upstream.json", json.dumps(source, ensure_ascii=False, indent=2) + "\n"),
        ("SKILL.md", notes),
    ):
        (folder / filename).write_text(text, encoding="utf-8")
    print("Imported {} from {} (cover={})".format(slug, entry_url, bool(cover)))


def main():
    path = os.environ.get("GITHUB_EVENT_PATH")
    if not path:
        raise ValueError("只能由仓库 GitHub Actions Issue 工作流触发")
    issue = json.loads(Path(path).read_text(encoding="utf-8")).get("issue") or {}
    actor = (issue.get("user") or {}).get("login")
    if actor != REPO.split("/")[0] or not (issue.get("title") or "").startswith("[导入 Skill]"):
        raise PermissionError("仅允许仓库所有者提交自动导入任务")
    body = issue.get("body") or ""
    found = re.findall(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[^\s<>)]*)?", body)
    if len(found) != 1:
        raise ValueError("Issue 必须恰好包含一个 GitHub 仓库或 SKILL.md 地址")
    import_repository(found[0].rstrip(".,，。"))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("ERROR:", str(exc), file=sys.stderr)
        raise
