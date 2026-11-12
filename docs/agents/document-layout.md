<!-- dsh-document-layout:v1 -->
# 项目统一文档布局

本表按"单一权威路由"为每个主题指定**当前真实权威**。路径均相对仓库根；已有正式资料保留原路径，未使用的分类不预建空目录。

- 知识索引: `docs/pocket/README.md`
- 中间产物根目录: `docs/_work/`
- 临时缓存根目录: `docs/_work/`（任务内 `tmp/`）

## 按类别选择路径

| 类别 | 优先位置（现有权威） | 缺失时回退目录 | 说明 |
| --- | --- | --- | --- |
| 项目定位、素材结构、日常操作 | `README.md` | — | 目前唯一正式项目说明；在其原位置增量编辑 |
| 部署与运维 | `README.md` 的「部署检查」「版权与安全」；`.github/workflows/pages.yml`、`.github/workflows/` 其他工作流 | `docs/pocket/operations/` | 工作流文件代表当前部署事实 |
| 正式需求 | 尚无正式需求/PRD 文档 | `docs/pocket/requirements/` | 新建即需确认为权威 |
| 设计与架构 | 尚无设计文档或 ADR | `docs/pocket/design/`、`docs/pocket/adr/` | ADR 用 `0001-short-title.md` |
| 接口与数据库 | 无（静态站无后端、无数据库） | 不适用 | 若将来引入接口再登记 |
| 素材规范与上游同步 | `README.md` 的「素材结构」「日常操作」；`library/skills/<slug>/meta.json`、`upstream.json` | `docs/pocket/specs/` | 每素材自身配置即事实来源 |
| 验收与交接 | `README.md` 的「部署检查」 | `docs/pocket/operations/` | 交接优先链接现有资料，不整篇复制 |
| 中间阶段成果 | 任务工作稿 | `docs/_work/<task-id>/` | 记录来源、阶段、状态（draft/pending/verified） |
| 临时缓存 | 不作为权威 | `docs/_work/<task-id>/tmp/` | 任务独立，清理前确认 |
| 外部工单 | GitHub Issues（`docs/agents/issue-tracker.md`） | 按 GitHub 约定 | 本地只保存引用 |

## 实现事实与文档的分工

`site/`、`scripts/`、`library/**` 的代码与配置代表**当前实现事实**；`README.md` 与将来获批的需求/设计文档代表**已确认决策**。两者冲突时标明差距，不以一方静默覆盖另一方。

## 维护约束

所有 Skills 和按钮先查此表及知识索引，已有正式资料保留原路径；未使用的分类不预建空目录。中间产物按任务独立存放，需区分 draft、pending 和 verified。变更布局、迁移已有产物或修改已批准资料先预览差异并确认，禁止静默复制或重命名。
