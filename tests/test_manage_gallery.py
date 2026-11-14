"""Regression tests for shared Prompt / Skill metadata and image editor."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts import manage_skill as manager


class ManageGalleryItemTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.original = (manager.SKILLS, manager.PROMPTS)
        self.addCleanup(self.restore_roots)
        root = Path(self.tmp.name)
        manager.SKILLS = root / "library" / "skills"
        manager.PROMPTS = root / "library" / "prompts"

    def restore_roots(self):
        manager.SKILLS, manager.PROMPTS = self.original

    def make_item(self, kind, slug="sample"):
        base = manager.SKILLS if kind == "skill" else manager.PROMPTS
        folder = base / slug
        images = folder / "images"
        images.mkdir(parents=True)
        for name in ("one.webp", "two.webp"):
            (images / name).write_bytes(b"fake-image-for-local-reference-test")
        meta = {
            "title": "Old title",
            "description": "Old description",
            "category": "Old category",
            "tags": ["旧标签"],
            "cover": "images/one.webp",
            "images": ["images/one.webp", "images/two.webp"],
        }
        (folder / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
        return folder

    def read_meta(self, folder):
        return json.loads((folder / "meta.json").read_text(encoding="utf-8"))

    def test_edit_prompt_metadata_and_select_second_cover(self):
        folder = self.make_item("prompt")
        manager.edit_images({
            "保留的现有图片": (
                "library/prompts/sample/images/one.webp\n"
                "library/prompts/sample/images/two.webp"
            ),
            "封面图片地址": "library/prompts/sample/images/two.webp",
            "标题（显示名称）": "双风格俯视地图",
            "简介": "两种风格多图轮换",
            "分类": "地图",
            "标签（逗号分隔）": "明日方舟, 原神， 地图, 明日方舟",
        }, "sample", "prompt")
        result = self.read_meta(folder)
        self.assertEqual(result["title"], "双风格俯视地图")
        self.assertEqual(result["description"], "两种风格多图轮换")
        self.assertEqual(result["category"], "地图")
        self.assertEqual(result["tags"], ["明日方舟", "原神", "地图"])
        self.assertEqual(result["cover"], "images/two.webp")
        self.assertEqual(result["images"], ["images/one.webp", "images/two.webp"])

    def test_legacy_skill_image_editor_does_not_change_metadata(self):
        folder = self.make_item("skill")
        manager.edit_images({
            "保留的现有图片": "library/skills/sample/images/one.webp",
            "封面图片地址": "library/skills/sample/images/one.webp",
        }, "sample")
        result = self.read_meta(folder)
        self.assertEqual(result["title"], "Old title")
        self.assertEqual(result["tags"], ["旧标签"])
        self.assertEqual(result["images"], ["images/one.webp"])

    def test_invalid_selected_cover_rejected(self):
        self.make_item("prompt")
        with self.assertRaisesRegex(ValueError, "封面必须"):
            manager.edit_images({
                "保留的现有图片": "library/prompts/sample/images/one.webp",
                "封面图片地址": "library/prompts/sample/images/two.webp",
            }, "sample", "prompt")

    def test_issue_render_text_fences_are_ignored(self):
        self.assertEqual(
            manager.text_refs("```text\nlibrary/prompts/sample/images/one.webp\n```"),
            ["library/prompts/sample/images/one.webp"],
        )
        self.assertEqual(manager.text_refs("```text\n无\n```"), ["无"])

    def test_kind_mismatch_rejected(self):
        self.make_item("prompt")
        with self.assertRaisesRegex(ValueError, "不存在"):
            manager.item_folder("sample", "skill")


if __name__ == "__main__":
    unittest.main()
