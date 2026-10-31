# 2. Constraints

The givens the design accepts rather than chooses.

## 2.1 Technical constraints

| # | Constraint | In practice | Source |
|---|------------|-------------|--------|
| 1 | Plain Markdown, no build step required | A template is read as written, and nothing compiles or packages it. Python runs the tools, the checks and the optional emitter | ADR-007, FR-05-01 |
| 2 | Agent-agnostic | Any agent that reads a Markdown context file can use the output, such as Claude Code, Codex CLI, Cursor or GitHub Copilot | FR-05-04 |
| 3 | An agent can generate by reading Markdown | No tool is needed between the templates and the context file, and instructions use neutral wording ("ask the user"). The emitter, where a project runs it, builds the same files | ADR-007, FR-05-01; ADR-058, proposed |
| 4 | Context windows are finite | Every rule in the root file is read on every turn by every project on that chain. A task's procedures load only when that task starts | ADR-041, ADR-058, QG-02-02 |

## 2.2 Compatibility constraints

| # | Constraint | In practice | Source |
|---|------------|-------------|--------|
| 1 | 3.x freezes the contract | The frozen surface does not break inside a major; a template is deprecated, then removed at the next major | ADR-051, FR-09-01, FR-09-02 |
| 2 | Forks sync by merge | Upstream never edits a path a fork owns, and a fork never edits an upstream manifest key | ADR-049, ADR-050, FR-08-01, FR-08-02 |

## 2.3 Organisational constraints

| # | Constraint | In practice | Source |
|---|------------|-------------|--------|
| 1 | One maintainer | Automated checks carry the review load, the maintainer approves every merge, and triage runs in batches | Chapter 1, Maintainer |
| 2 | MIT licence | Anyone may fork the templates, use them commercially and keep the fork private, so upstream cannot rely on seeing its forks | `LICENSE` |
| 3 | Built by agents | Agents develop and review upstream, and the maintainer specifies and approves. Every procedure is one an agent can follow | Chapter 1, Team |
| 4 | Hosted on GitHub | Issues, pull requests, CI and the fork model all run on GitHub | - |

## 2.4 Conventions

| # | Convention | In practice | Source |
|---|------------|-------------|--------|
| 1 | arc42 | The architecture is one chapter per file, indexed by `docs/spec.md` | `docs/spec.md` |
| 2 | RFC 2119 | A rule is a plain imperative or carries MUST, SHOULD or MAY | FR-01-01 |
| 3 | Kebab-case file names | Every document under `docs/` and every template | - |
| 4 | Line width 88 | Declared in `.editorconfig` and the markdownlint config, and enforced on every Markdown file | `.editorconfig` |
