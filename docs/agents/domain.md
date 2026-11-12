# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`docs/pocket/README.md`** — the active project knowledge map. Follow its task pointers and its [ownership policy](../pocket/meta/knowledge-policy.md).
- **`README.md`** at the repo root — the only formal project document today: positioning, material structure, daily operations, deployment checks, licensing and security.

This repo has **no** `GLOSSARY.md`, `GLOSSARY-MAP.md`, `docs/adr/` or context-local ADRs yet. Terms and consequential decisions therefore go to `docs/pocket/meta/glossary.md` and `docs/pocket/adr/`, created lazily when one is actually resolved — not upfront.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in the glossary once it exists. Don't drift to synonyms it explicitly avoids.

Terms already load-bearing in this repo, to be used as written: **素材** (`library/prompts/<slug>/`, `library/skills/<slug>/`), **meta.json**, **upstream.json**, **图库** (the site in `site/`), **导入 Skill**(the issue-triggered import), **link-only / allowlisted-mit-text**(the two upstream sync modes), **external_only**(a Skill indexed by link without redistributable content).

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders), but worth reopening because…_

## Legacy authorities, pending migration

- None. No document in this repo is being relocated; `README.md` keeps its root path.
