# 2. Constraints

The givens the design accepts rather than chooses.

## 2.1 Technical constraints

| # | Constraint | In practice | Source |
|---|------------|-------------|--------|
| 1 | Plain Markdown, no build step | A template is read as written; nothing compiles or packages it. Python is needed only for the tools and checks | Chapter 4 |
| 2 | Agent-agnostic | Any agent that reads a Markdown context file can use the output: Claude Code, Codex CLI, Cursor, GitHub Copilot and others | `templates/core/docs.md`, "Output file by agent" |
| 3 | Generation is an agent reading Markdown | No compiler sits between the fork and the context file; instructions use neutral wording ("ask the user") | Chapter 6 |
| 4 | Context windows are finite | Every rule in a widely resolved file is read by every project on that chain, on every turn | `tests/smoke/context-tiers.txt`, SYS-16 |

## 2.2 Compatibility constraints

| # | Constraint | In practice | Source |
|---|------------|-------------|--------|
| 1 | 3.x freezes the contract | Template paths, template and section IDs and the manifest shape do not break inside a major; a template is deprecated, then removed at the next major | ADR-051, chapter 8 |
| 2 | Forks sync by merge | Upstream never edits a path a fork owns, and a fork never edits an upstream manifest key | ADR-049, ADR-050 |

## 2.3 Organisational constraints

| # | Constraint | In practice | Source |
|---|------------|-------------|--------|
| 1 | One maintainer | Automated checks carry the review load, the maintainer approves every merge, and triage runs in batches | `CONTRIBUTING.md`, "Maintainership" |
| 2 | Licence | The repository is published under the licence in `LICENSE` | `LICENSE` |

## 2.4 Conventions

| # | Convention | In practice |
|---|------------|-------------|
| 1 | arc42 | The architecture is one chapter per file, indexed by `docs/spec.md` |
| 2 | RFC 2119 | A rule is a plain imperative or carries MUST, SHOULD or MAY |
| 3 | Kebab-case file names | Every document under `docs/` and every template |
| 4 | Line width 88 | Declared in `.editorconfig` and the markdownlint config, and enforced on every Markdown file |
