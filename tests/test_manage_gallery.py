"""Regression tests for shared Prompt / Skill metadata and image editor."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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

    def test_existing_avif_cover_can_be_retained_and_selected(self):
        """Regression for issue #3: AVIF can be kept as the only visible image."""
        folder = self.make_item("prompt")
        (folder / "images" / "cover.avif").write_bytes(b"existing-avif-image")
        meta = self.read_meta(folder)
        meta["cover"] = "images/cover.avif"
        meta["images"] = ["images/cover.avif", "images/one.webp"]
        manager.write_meta(folder, meta)

        manager.edit_images({
            "保留的现有图片": "library/prompts/sample/images/cover.avif",
            "封面图片地址": "library/prompts/sample/images/cover.avif",
            "标题（显示名称）": "AVIF 电影肖像",
        }, "sample", "prompt")
        result = self.read_meta(folder)
        self.assertEqual(result["title"], "AVIF 电影肖像")
        self.assertEqual(result["images"], ["images/cover.avif"])
        self.assertEqual(result["cover"], "images/cover.avif")

    def test_metadata_only_edit_preserves_existing_avif(self):
        """The default keep-all behavior must not drop supported AVIF images."""
        folder = self.make_item("prompt")
        (folder / "images" / "cover.avif").write_bytes(b"existing-avif-image")
        meta = self.read_meta(folder)
        meta["cover"] = "images/cover.avif"
        meta["images"] = ["images/cover.avif", "images/one.webp"]
        manager.write_meta(folder, meta)

        manager.edit_images({"标题（显示名称）": "更新标题"}, "sample", "prompt")
        result = self.read_meta(folder)
        self.assertEqual(result["images"], ["images/cover.avif", "images/one.webp"])
        self.assertEqual(result["cover"], "images/cover.avif")

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

    def test_local_image_selected_as_second_upload_cover(self):
        folder = self.make_item("prompt")
        sections = {
            "保留的现有图片": "library/prompts/sample/images/one.webp",
            "封面图片地址": "upload:2",
            "本地图片上传数量": "2",
            "上传新图片": (
                "![first](https://github.com/user-attachments/assets/first-123)\n"
                "![second](https://github.com/user-attachments/assets/second-456)"
            ),
        }
        first = b"\x89PNG\r\n\x1a\nfirst-image"
        second = b"\xff\xd8\xffsecond-image"
        with patch.object(manager, "fetch_upload", side_effect=[first, second]):
            manager.edit_images(sections, "sample", "prompt")
        meta = self.read_meta(folder)
        self.assertEqual(len(meta["images"]), 3)
        self.assertEqual(meta["cover"], meta["images"][2])
        self.assertTrue((folder / meta["cover"]).is_file())

    def test_missing_staged_local_file_rejected_before_download(self):
        self.make_item("skill")
        with self.assertRaisesRegex(ValueError, "实际上传 0 张"):
            manager.edit_images({
                "本地图片上传数量": "1",
                "封面图片地址": "upload:1",
            }, "sample", "skill")

    def test_out_of_range_local_cover_rejected(self):
        self.make_item("skill")
        with patch.object(manager, "fetch_upload", return_value=b"\x89PNG\r\n\x1a\nimage"):
            with self.assertRaisesRegex(ValueError, "指定的本地封面不存在"):
                manager.edit_images({
                    "本地图片上传数量": "1",
                    "上传新图片": "![img](https://github.com/user-attachments/assets/one-1)",
                    "封面图片地址": "upload:2",
                }, "sample", "skill")

    def test_kind_mismatch_rejected(self):
        self.make_item("prompt")
        with self.assertRaisesRegex(ValueError, "不存在"):
            manager.item_folder("sample", "skill")


if __name__ == "__main__":
    unittest.main()
