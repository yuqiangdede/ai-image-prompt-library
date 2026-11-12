"""Temporary check: a Skill with a local uploaded image builds correctly."""
import base64
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from scripts import build_site  # noqa: E402

FOLDER = ROOT / "library" / "skills" / "zz-build-test"
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Y9Z2S8AAAAASUVORK5CYII="
)


def main():
    try:
        (FOLDER / "images").mkdir(parents=True)
        (FOLDER / "images" / "cover.png").write_bytes(PNG)
        (FOLDER / "meta.json").write_text(json.dumps({
            "title": "Build Test", "description": "local image", "category": "综合 Skill",
            "tags": [], "model": "ChatGPT", "updated_at": "2026-11-12",
            "cover": "images/cover.png", "images": ["images/cover.png"], "related_skills": [],
        }, ensure_ascii=False), encoding="utf-8")
        (FOLDER / "SKILL.md").write_text("# build test\n", encoding="utf-8")
        build_site.build()
        catalog = json.loads((ROOT / "dist" / "data" / "catalog.json").read_text(encoding="utf-8"))
        item = next(x for x in catalog["items"] if x["slug"] == "zz-build-test")
        assert item["cover"] == "library/skills/zz-build-test/images/cover.png", item
        assert item["upstream_linked"] is False, item
        print("local image build check passed")
    finally:
        shutil.rmtree(FOLDER, ignore_errors=True)
        build_site.build()


if __name__ == "__main__":
    main()
