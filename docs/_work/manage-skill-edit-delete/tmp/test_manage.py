"""Local checks for scripts/manage_skill.py. Not part of the site."""
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from scripts import manage_skill as m  # noqa: E402


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def meta(**extra):
    data = {
        "title": "Test Skill", "description": "test", "category": "综合 Skill",
        "tags": [], "model": "ChatGPT", "updated_at": "2026-01-01",
        "cover": "images/a.png", "images": ["images/a.png"], "related_skills": [],
    }
    data.update(extra)
    return data


def sections(slug, keep, cover="", urls="", confirm=""):
    return m.parse_sections(
        "### Skill 标识（slug）\n\n{}\n\n### 保留的现有图片\n\n{}\n\n### 封面图片地址\n\n{}\n\n"
        "### 新增图片地址\n\n{}\n\n### 上传新图片\n\nNo response\n\n### 确认\n\n{}".format(
            slug, keep, cover, urls, confirm))


def run():
    assert m.linked_image_url("https://github.com/a/b/blob/main/x.png") == "https://raw.githubusercontent.com/a/b/main/x.png"
    assert m.linked_image_url("https://github.com/a/b/raw/main/x.png") == "https://raw.githubusercontent.com/a/b/main/x.png"
    assert m.linked_image_url("https://example.com/x.png") is None
    assert m.linked_image_url("https://github.com/a/b/tree/main") is None
    assert m.attachment_urls("![x](https://github.com/user-attachments/assets/abc),") == [
        "https://github.com/user-attachments/assets/abc"]
    assert m.image_extension(b"\x89PNG\r\n\x1a\nx") == ".png"
    assert m.image_extension(b"\xff\xd8\xffx") == ".jpg"
    assert m.image_extension(b"GIF89ax") == ".gif"
    assert m.image_extension(b"RIFF1234WEBPx") == ".webp"
    try:
        m.image_extension(b"<svg>")
        raise AssertionError("svg should be rejected")
    except ValueError:
        pass

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        m.SKILLS = tmp / "skills"
        m.PROMPTS = tmp / "prompts"
        folder = m.SKILLS / "test-skill"
        (folder / "images").mkdir(parents=True)
        (folder / "images" / "a.png").write_bytes(b"\x89PNG\r\n\x1a\nx")
        (folder / "images" / "b.png").write_bytes(b"\x89PNG\r\n\x1a\nx")
        write(folder / "meta.json", json.dumps(meta(), ensure_ascii=False))
        write(folder / "SKILL.md", "# test\n")
        write(folder / "upstream.json", '{"url": "https://github.com/a/b"}')

        # Keep one image, choose it as cover.
        m.edit_images(sections(
            "test-skill",
            "library/skills/test-skill/images/a.png",
            "library/skills/test-skill/images/a.png"), "test-skill")
        data = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
        assert data["images"] == ["images/a.png"], data
        assert data["cover"] == "images/a.png", data

        # Add a linked image without touching the network; it becomes the cover.
        original_check = m.check_linked_image
        m.check_linked_image = lambda url: None
        try:
            m.edit_images(sections(
                "test-skill",
                "No response",
                "",
                "https://github.com/a/b/blob/main/images/new.png",
                "- [X] yes"), "test-skill")
        finally:
            m.check_linked_image = original_check
        data = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
        assert data["images"] == [
            "images/a.png",
            "https://raw.githubusercontent.com/a/b/main/images/new.png"], data
        assert data["cover"] == "https://raw.githubusercontent.com/a/b/main/images/new.png", data

        # Uploaded images are copied into images/ and become the cover.
        original_fetch = m.fetch_upload
        m.fetch_upload = lambda url: b"\x89PNG\r\n\x1a\nuploaded"
        try:
            m.edit_images(m.parse_sections(
                "### Skill 标识（slug）\n\ntest-skill\n\n### 保留的现有图片\n\n无\n\n"
                "### 封面图片地址\n\nNo response\n\n### 新增图片地址\n\nNo response\n\n"
                "### 上传新图片\n\n![x](https://github.com/user-attachments/assets/abc)\n\n"
                "### 确认\n\n- [X] yes"), "test-skill")
        finally:
            m.fetch_upload = original_fetch
        data = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
        assert len(data["images"]) == 1 and data["images"][0].startswith("images/upload-"), data
        assert data["cover"] == data["images"][0] and (folder / data["images"][0]).is_file(), data

        # An attachment URL pasted into the new-image field can also be the cover.
        m.fetch_upload = lambda url: b"\x89PNG\r\n\x1a\ncover-upload"
        try:
            m.edit_images(m.parse_sections(
                "### Skill 标识（slug）\n\ntest-skill\n\n### 保留的现有图片\n\n无\n\n"
                "### 封面图片地址\n\nhttps://github.com/user-attachments/assets/cover\n\n"
                "### 新增图片地址\n\nhttps://github.com/user-attachments/assets/cover\n\n"
                "### 上传新图片\n\nNo response\n\n### 确认\n\n- [X] yes"), "test-skill")
        finally:
            m.fetch_upload = original_fetch
        data = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
        assert len(data["images"]) == 1 and data["images"][0].startswith("images/upload-"), data
        assert data["cover"] == data["images"][0], data

        # Remove everything.
        m.edit_images(sections("test-skill", "无", ""), "test-skill")
        data = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
        assert data["images"] == [] and data["cover"] == "", data

        # Deleting requires the confirmation checkbox.
        try:
            m.delete_skill(sections("test-skill", "", confirm=""), "test-skill")
            raise AssertionError("delete should require confirmation")
        except PermissionError:
            pass

        write(tmp / "prompts" / "p1" / "meta.json",
              json.dumps(meta(related_skills=["test-skill"]), ensure_ascii=False))
        m.delete_skill(sections("test-skill", "", confirm="- [X] yes"), "test-skill")
        assert not folder.exists()
        data = json.loads((tmp / "prompts" / "p1" / "meta.json").read_text(encoding="utf-8"))
        assert data["related_skills"] == [], data

        # Slug traversal and unknown slugs are rejected.
        for bad in ("../x", "Test-Skill", "missing"):
            try:
                m.skill_folder(bad)
                raise AssertionError("slug should be rejected: " + bad)
            except ValueError:
                pass

        event = tmp / "event.json"
        original_repo = m.REPO
        try:
            m.REPO = "owner/repo"
            event.write_text(json.dumps({
                "issue": {"user": {"login": "someone"}, "title": "[修改图片] x", "body": ""},
            }), encoding="utf-8")
            os.environ["GITHUB_EVENT_PATH"] = str(event)
            try:
                m.issue_request()
                raise AssertionError("non-owner should be rejected")
            except PermissionError:
                pass
            event.write_text(json.dumps({
                "issue": {"user": {"login": "owner"}, "title": "[删除 Skill] test-skill", "body": ""},
            }), encoding="utf-8")
            title, parsed, slug = m.issue_request()
            assert title == "[删除 Skill] test-skill" and parsed == {} and slug == "test-skill"
        finally:
            m.REPO = original_repo
            os.environ.pop("GITHUB_EVENT_PATH", None)

    with tempfile.TemporaryDirectory() as tmp2:
        tmp2 = Path(tmp2)
        m.SKILLS = tmp2 / "skills"
        m.PROMPTS = tmp2 / "prompts"
        folder = m.SKILLS / "gh-skill"
        folder.mkdir(parents=True)
        first = "https://raw.githubusercontent.com/a/b/main/one.jpg"
        second = "https://raw.githubusercontent.com/a/b/main/two.jpg"
        write(folder / "meta.json", json.dumps(
            meta(cover=first, images=[first, second]), ensure_ascii=False))
        write(folder / "SKILL.md", "# gh\n")
        write(folder / "upstream.json", '{"url": "https://github.com/a/b"}')
        event = tmp2 / "event.json"
        original_repo = m.REPO
        try:
            m.REPO = "owner/repo"
            os.environ["GITHUB_EVENT_PATH"] = str(event)
            event.write_text(json.dumps({"issue": {
                "user": {"login": "owner"}, "title": "[修改图片]",
                "body": "### Skill 标识（slug）\n\ngh-skill\n\n### 保留的现有图片\n\n" + second +
                        "\n\n### 封面图片地址\n\n" + second +
                        "\n\n### 新增图片地址\n\nNo response\n\n### 上传新图片\n\nNo response\n\n"
                        "### 确认\n\n- [X] yes",
            }}), encoding="utf-8")
            m.main()
            data = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
            assert data["images"] == [second] and data["cover"] == second, data
            event.write_text(json.dumps({"issue": {
                "user": {"login": "owner"}, "title": "[删除 Skill]",
                "body": "### Skill 标识（slug）\n\ngh-skill\n\n### 确认\n\n- [X] yes",
            }}), encoding="utf-8")
            m.main()
            assert not folder.exists()
        finally:
            m.REPO = original_repo
            os.environ.pop("GITHUB_EVENT_PATH", None)

    print("manage_skill checks passed")


if __name__ == "__main__":
    run()
