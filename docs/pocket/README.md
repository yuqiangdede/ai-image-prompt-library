# Pocket — project knowledge map

Pocket is the Markdown knowledge map for this project. Existing authoritative documents stay in their original locations; Pocket supplies only the index and, lazily, missing topics. Git records their history; no RAG index is required.

## Always read

- [Knowledge policy](meta/knowledge-policy.md) — document authority, updates and maintenance
- [文档目录说明](../文档目录说明.md) — 中文目录导航
- [README.md](../../README.md) — 项目定位、素材结构、日常操作、部署检查、版权与安全；目前唯一正式项目说明

## Select documents by task

| Task/trigger | Actual authoritative path (existing first) | Required next read |
| --- | --- | --- |
| 了解项目定位、素材结构、日常操作 | [README.md](../../README.md) | 对应 `library/<slug>/` 的配置 |
| 发布、部署或排查上线 | [README.md](../../README.md)「部署检查」 | [pages.yml](../../.github/workflows/pages.yml) |
| 改网页行为或界面 | [site/index.html](../../site/index.html)、[site/app.js](../../site/app.js) | [site/app.css](../../site/app.css) |
| 改素材校验或站点生成 | [scripts/build_site.py](../../scripts/build_site.py) | 目标素材的 `meta.json` |
| 上游同步，或改同步白名单 | [scripts/sync_upstream.py](../../scripts/sync_upstream.py) | 目标 Skill 的 [upstream.json](../../library/skills/mono-color/upstream.json) |
| 自动导入 Skill | [scripts/import_skill.py](../../scripts/import_skill.py) | [add-skill.yml](../../.github/ISSUE_TEMPLATE/add-skill.yml) |
| 修改图片或删除已收录 Skill | [scripts/manage_skill.py](../../scripts/manage_skill.py)、[site/app.js](../../site/app.js) 管理面板 | [edit-skill.yml](../../.github/ISSUE_TEMPLATE/edit-skill.yml)、[delete-skill.yml](../../.github/ISSUE_TEMPLATE/delete-skill.yml) |
| 排查 Bug 或历史变更 | 尚无事件/踩坑记录 | 按需补 `docs/pocket/pitfalls/` |
| 澄清或固化需求 | 尚无正式需求文档 | 按需补 `docs/pocket/requirements/` |
| 记录不可逆架构决策 | 尚无 ADR | 按需补 `docs/pocket/adr/` |
| 统一术语 | 尚无 `GLOSSARY.md` | 按需补 `docs/pocket/meta/glossary.md` |

尚未建立的类别只在上表以文字说明，不伪造链接；首次真正需要时再创建对应文件。

## Knowledge status

- Current/accepted: load for applicable tasks. `README.md` and the `site/`、`scripts/`、`library/**` files above carry current status.
- Pending/draft: read only when resolving an open question; never treat as approval.
- Superseded/deprecated: load only for historical investigation; identify the replacing document.

## Maintenance

Review affected entries after material, script or workflow changes and significant PRs. Run `/pocket-maintenance` monthly or when duplication, contradictory instructions, or stale pointers appear.
