# AGENTS.md

AI 生图 Prompt / Skill 图库：GitHub Pages 静态站（原生 HTML/CSS/JS）+ Python 标准库脚本，素材在 `library/`，构建产物 `dist/` 不入库。

## Agent skills

### Image upload / cover materialization

When a user asks to upload generated images, add a Prompt, or replace a cover, **first read** `docs/pocket/pitfalls/2026-11-18-chatgpt-image-direct-upload.md`. Prefer the verified direct WebP → Base64 bridge → GitHub Blob/Tree/Commit → `main` path and verify the exact GitHub Blob SHA plus final Actions success. Treat Issue upload as fallback; do not equate local conversion, an Issue, a Blob, a branch commit, and deployment. Keep actual generated image bytes and the user's full prompt intact.

### Issue tracker

Issues and specs live in this repo's GitHub Issues (`gh` CLI, `yuqiangdede/ai-image-prompt-library`). See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical triage roles map to same-named GitHub labels. See `docs/agents/triage-labels.md`.

### Domain docs

No glossary or ADR exists yet; terms and decisions go to `docs/pocket/meta/glossary.md` and `docs/pocket/adr/` when resolved. See `docs/agents/domain.md`.

### Document and intermediate artifact layout

Before creating, reading, or relying on any document, report, Gate result or intermediate file, read `docs/agents/document-layout.md` and its knowledge index `docs/pocket/README.md`. Reuse existing authorized formal destinations. Save intermediate files only under `docs/_work/<task-id>/`. Never override this layout with a hardcoded Skill default.

### Project knowledge (Pocket)

Before working on project requirements, design, or code, read `docs/pocket/README.md` and its task-specific pointers. Follow the documented authoritative locations for each topic; reuse existing requirements, designs, ADRs and operations files before considering `docs/pocket/` for missing topics. Write confirmed decisions to their authoritative files, not solely in chat. If source, existing docs, or task instructions conflict, report the discrepancy rather than silently rewriting requirements.
