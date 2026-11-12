# Knowledge ownership and maintenance

- Canonical knowledge is defined **per topic** by this project's current index and Agent instructions. Existing approved documents outside Pocket keep their original authority; Pocket is an index and fallback for missing topics, not a universal migration target. Generated indexes and external issues are pointers, not second authoritative copies.
- Code, executable tests, tool configuration, and dependency lockfiles remain authoritative for actual implementation and installed versions. If they contradict a requirement or ADR, flag and resolve; do not change accepted requirements to match code without approval.
- New docs should state status (pending/accepted/superseded/deprecated), scope/owner where useful, and links to related requirements, tasks, and ADRs. Keep one authoritative location per fact. The Pocket index (`docs/pocket/README.md`) and this policy are status-exempt meta files.
- Use progressive disclosure: load this policy and relevant active documents, then referenced detail as needed. Do not load the whole knowledge directory by default.
- Keep secrets, credentials, user data, and raw session transcripts out of committed knowledge.
- Prefer links over copying content. Do not duplicate large configuration/code inventories easily discovered from the repository.
- After requirements, architectural changes, or substantial PRs, inspect affected knowledge and correct the active index (whether inside Pocket or not). Monthly, run `/pocket-maintenance` to propose duplicates, conflicts, stale docs, and archival candidates.
- Maintain history through Git and explicit successor links. Never automatically delete an ADR, erase an unresolved decision, or silently rewrite an approved requirement.

## 本项目适用要点

- `README.md` 是现行唯一正式项目说明，直接在原位置增量编辑；它是**运维与项目概览**的权威，不是素材清单的权威。
- 每个素材的 `meta.json` / `upstream.json` 是该素材的事实来源；Pocket 不复制其字段。
- 本站为公开静态仓库：**不得**写入私人照片、私密提示词、访问令牌或第三方未授权艺术资源（`mono-color` 的 `examples/` 即属此类，仅允许链接原始 URL）。
