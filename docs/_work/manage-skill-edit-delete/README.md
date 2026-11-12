# 修改图片 / 删除已收录 Skill

- 来源：用户需求「支持 修改 删除 导入的skill 修改主要是修改图片」
- 阶段：实现与本地验证完成（verified，2026-11-12）
- 正式落点：`scripts/manage_skill.py`、`.github/ISSUE_TEMPLATE/edit-skill.yml`、`.github/ISSUE_TEMPLATE/delete-skill.yml`、`.github/workflows/pages.yml`、`site/` 管理面板
- 验证：`tmp/test_manage.py` 通过（保留/删图/设封面/上传/附件封面、删除并清理关联、owner 校验）；`build_site.py` 生成 7 条；浏览器 390×844 / 1280×800 检查管理面板与预填 Issue URL
- 已提交：`5bdc999`（2026-11-12）。推送后由 GitHub Actions 重新构建并发布。
