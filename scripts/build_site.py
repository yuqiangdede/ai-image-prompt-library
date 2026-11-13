#!/usr/bin/env python3
"""Build static prompt / Skill gallery. Python standard library only."""
import json
import os
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
LIBRARY = ROOT / "library"
DIST = ROOT / "dist"

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def img_path(path, folder):
    if not isinstance(path, str) or not path:
        raise ValueError(f"Invalid image path in {folder}")
    if path.startswith("https://"):
        if urlparse(path).hostname not in ("raw.githubusercontent.com", "github.com", "hand-drawn-images.pages.dev"):
            raise ValueError(f"Unapproved image URL: {path}")
        return path
    p = (folder / path).resolve()
    if not p.is_relative_to(folder.resolve()) or not p.is_file():
        raise ValueError(f"Image not found or escapes item: {path}")
    return p.relative_to(ROOT).as_posix()

def make_item(folder, kind):
    meta = read_json(folder / "meta.json")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", folder.name):
        raise ValueError(f"Invalid item directory: {folder}")
    for field in ("title", "description", "category"):
        if not isinstance(meta.get(field), str) or not meta[field].strip():
            raise ValueError(f"{folder}: missing field {field}")
    external_only = kind == "skill" and meta.get("external_only", False) is True
    body = folder / ("SKILL.md" if kind == "skill" else "prompt.md")
    if not body.is_file():
        raise ValueError(f"Missing {body}")
    images = [img_path(p, folder) for p in meta.get("images", [])]
    cover = img_path(meta["cover"], folder) if meta.get("cover") else (images[0] if images else "")
    upstream = read_json(folder / "upstream.json") if (folder / "upstream.json").exists() else {}
    return {
        "id": f"{kind}:{folder.name}", "slug": folder.name, "kind": kind,
        "title": meta["title"], "description": meta["description"], "category": meta["category"],
        "tags": meta.get("tags", []), "model": meta.get("model", "ChatGPT"),
        "updated_at": meta.get("updated_at", "2026-11-12"),
        "cover": cover, "images": images, "related_skills": meta.get("related_skills", []),
        "content_path": body.relative_to(ROOT).as_posix(),
        "search_text": body.read_text(encoding="utf-8"),
        "source_url": upstream.get("url", meta.get("source_url", "")),
        "source_sha": upstream.get("sha", ""),
        "source_branch": upstream.get("branch", ""),
        "upstream_linked": bool(upstream.get("url")),
        "external_only": external_only,
        "install_command": meta.get("install_command", ""),
    }

def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SITE, DIST)
    shutil.copytree(LIBRARY, DIST / "library")
    (DIST / "data").mkdir(exist_ok=True)
    (DIST / "downloads" / "skills").mkdir(parents=True, exist_ok=True)
    items = []
    for kind, directory in (("prompt", "prompts"), ("skill", "skills")):
        base = LIBRARY / directory
        if not base.exists():
            continue
        for folder in sorted(x for x in base.iterdir() if x.is_dir() and (x / "meta.json").exists()):
            item = make_item(folder, kind)
            if kind == "skill" and not item["external_only"]:
                zip_file = DIST / "downloads" / "skills" / (folder.name + ".zip")
                with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as z:
                    for path in sorted(folder.rglob("*")):
                        if path.is_file() and not path.is_symlink():
                            z.write(path, path.relative_to(base))
                item["skill_zip"] = zip_file.relative_to(DIST).as_posix()
            items.append(item)
    slugs = {e["slug"] for e in items if e["kind"] == "skill"}
    for item in items:
        if any(slug not in slugs for slug in item["related_skills"]):
            raise ValueError(f"Related skill missing in {item['id']}")
    items.sort(key=lambda x: (x["updated_at"], x["title"]), reverse=True)
    repo = os.environ.get("GITHUB_REPOSITORY", "yuqiangdede/ai-image-prompt-library")
    catalog = {
        "schema_version": 3, "site_name": "AI 生图 Prompt / Skill 图库",
        "repository_url": "https://github.com/" + repo,
        "generated_at": datetime.now(timezone.utc).isoformat(), "items": items,
    }
    (DIST / "data" / "catalog.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Generated {len(items)} gallery items")

if __name__ == "__main__":
    build()
