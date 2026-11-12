"""Local checks for scripts/add_prompt.py. Run from the repository root."""
import json
import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from scripts import add_prompt as ap  # noqa: E402

PNG = b"\x89PNG\r\n\x1a\n" + b"local-test"


def test_issue_template_labels():
    text = (ROOT / ".github" / "ISSUE_TEMPLATE" / "add-prompt.yml").read_text(encoding="utf-8")
    labels = re.findall(r"^ {6}label: (.+)$", text, re.M)
    assert set(labels) == set(ap.LABELS.values()), (labels, list(ap.LABELS.values()))
    ids = re.findall(r"^ {4}id: (.+)$", text, re.M)
    assert ids == ["prompt_title", "prompt_description", "prompt_category", "prompt_tags",
                   "prompt_model", "prompt_body", "cover_url", "cover_image", "prompt_slug",
                   "confirm"], ids


def sections(**overrides):
    data = {
        "title": "科普图鉴测试",
        "description": "输入主题生成竖版科普信息图。",
        "category": "科普图鉴",
        "tags": "知识信息图, 模块化排版",
        "model": "ChatGPT",
        "prompt": "第一行\n### 正文自己的标题\n第三行",
        "cover_url": "https://raw.githubusercontent.com/example/repo/main/cover.png",
        "cover_file": "",
        "slug": "",
        "confirm": "- [x] 我确认这段提示词可以公开",
    }
    data.update(overrides)
    return data


def test_parse_issue_body():
    body = "\n".join([
        "### 标题（显示名称）",
        "",
        "示例",
        "",
        "### 提示词正文（原样写入 prompt.md）",
        "",
        "第一行",
        "### 正文自己的标题",
        "第三行",
        "",
        "### 封面图地址（GitHub 图片链接）",
        "",
        "https://raw.githubusercontent.com/a/b/main/c.png",
    ])
    parsed = ap.parse_issue_body(body)
    assert parsed["title"] == "示例"
    assert parsed["prompt"] == "第一行\n### 正文自己的标题\n第三行"
    assert parsed["cover_url"] == "https://raw.githubusercontent.com/a/b/main/c.png"
    assert ap.normalize_tags("海报, 平面设计，海报") == ["海报", "平面设计"]
    assert ap.normalize_prompt("a\r\nb") == "a\nb\n"
    assert ap.explicit_slug(" science-encyclopedia-infographic ") == "science-encyclopedia-infographic"


def test_cover_url_conversion():
    seen = []
    ap.check_linked_image = lambda url: seen.append(url)
    kind, url = ap.resolve_cover({
        "cover_url": "https://github.com/a/b/blob/main/x.png",
        "cover_file": "",
    })
    assert kind == "url"
    assert url == "https://raw.githubusercontent.com/a/b/main/x.png"
    assert seen == [url]


def test_url_cover_and_auto_slug():
    with tempfile.TemporaryDirectory() as tmp:
        ap.PROMPTS = Path(tmp) / "prompts"
        ap.check_linked_image = lambda url: None
        slug, title = ap.add_prompt(sections())
        folder = ap.PROMPTS / slug
        assert title == "科普图鉴测试"
        assert slug.startswith("prompt-")
        assert (folder / "prompt.md").read_text(encoding="utf-8") == "第一行\n### 正文自己的标题\n第三行\n"
        meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
        assert meta["cover"] == "https://raw.githubusercontent.com/example/repo/main/cover.png"
        assert meta["images"] == [meta["cover"]]
        assert meta["tags"] == ["知识信息图", "模块化排版"]
        assert meta["model"] == "ChatGPT"


def test_uploaded_cover():
    with tempfile.TemporaryDirectory() as tmp:
        ap.PROMPTS = Path(tmp) / "prompts"
        ap.fetch_upload = lambda url: PNG
        slug, _ = ap.add_prompt(sections(
            cover_url="",
            cover_file="![cover](https://github.com/user-attachments/assets/abc)",
            slug="uploaded-cover-test",
        ))
        folder = ap.PROMPTS / slug
        assert (folder / "images" / "cover.png").read_bytes() == PNG
        meta = json.loads((folder / "meta.json").read_text(encoding="utf-8"))
        assert meta["cover"] == "images/cover.png"


def test_validation_and_collision():
    with tempfile.TemporaryDirectory() as tmp:
        ap.PROMPTS = Path(tmp) / "prompts"
        ap.check_linked_image = lambda url: None
        try:
            ap.add_prompt(sections(cover_url="", cover_file=""))
        except ValueError as exc:
            assert "封面" in str(exc)
        else:
            raise AssertionError("missing cover must fail")
        try:
            ap.add_prompt(sections(prompt="   "))
        except ValueError as exc:
            assert "提示词正文" in str(exc)
        else:
            raise AssertionError("empty prompt must fail")
        ap.add_prompt(sections(slug="same-slug"))
        try:
            ap.add_prompt(sections(slug="same-slug"))
        except ValueError as exc:
            assert "已存在" in str(exc)
        else:
            raise AssertionError("duplicate slug must fail")


def test_main_from_issue_event():
    with tempfile.TemporaryDirectory() as tmp:
        ap.PROMPTS = Path(tmp) / "prompts"
        ap.REPO = "yuqiangdede/ai-image-prompt-library"
        ap.check_linked_image = lambda url: None
        body = "\n".join([
            "### 标题（显示名称）", "", "事件测试提示词", "",
            "### 简介（卡片说明）", "", "验证 Issue 事件解析。", "",
            "### 分类（主题）", "", "测试分类", "",
            "### 标签（用逗号分隔）", "", "测试, 提示词", "",
            "### 适用模型", "", "ChatGPT", "",
            "### 提示词正文（原样写入 prompt.md）", "", "这是正文。", "",
            "### 封面图地址（GitHub 图片链接）", "",
            "https://raw.githubusercontent.com/a/b/main/c.png", "",
            "### 目录标识（slug，可留空自动生成）", "", "issue-event-test", "",
            "### 确认", "", "- [x] 我确认这段提示词可以公开，封面图有权在本仓库展示",
        ])
        event = {
            "issue": {
                "title": "[添加提示词] 事件测试提示词",
                "body": body,
                "user": {"login": "yuqiangdede"},
            }
        }
        event_path = Path(tmp) / "event.json"
        event_path.write_text(json.dumps(event, ensure_ascii=False), encoding="utf-8")
        old = os.environ.get("GITHUB_EVENT_PATH")
        os.environ["GITHUB_EVENT_PATH"] = str(event_path)
        try:
            ap.main()
        finally:
            if old is None:
                os.environ.pop("GITHUB_EVENT_PATH", None)
            else:
                os.environ["GITHUB_EVENT_PATH"] = old
        assert (ap.PROMPTS / "issue-event-test" / "prompt.md").is_file()


if __name__ == "__main__":
    test_issue_template_labels()
    print("template labels: ok")
    test_parse_issue_body()
    print("parse: ok")
    test_url_cover_and_auto_slug()
    print("url cover: ok")
    test_cover_url_conversion()
    print("cover conversion: ok")
    test_uploaded_cover()
    print("upload: ok")
    test_validation_and_collision()
    print("validation: ok")
    test_main_from_issue_event()
    print("issue event: ok")
