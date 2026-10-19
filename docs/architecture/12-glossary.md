# 12. Glossary

| Term | Meaning |
|------|---------|
| Base template | A template under `core/`, `security/`, `infra/` or `data/`, covering one concern for any project |
| Chain | The ordered list of templates a root resolves to |
| Context file | The file an agent reads at startup: `AGENTS.md`, `CLAUDE.md` or an agent's own format |
| Core tier | The templates seeded into every chain: `core:`, then a fork's `fork_core:` |
| Declaration block | The target header in a generated file naming its stack, extras and platform |
| Directive | A tag line a tool reads: `[ID:]`, `[DEPENDS ON:]`, `[EXTEND:]`, `[OVERRIDE:]` |
| Extra | An orthogonal template a project picks beside its stack |
| Fixture | The stack and platform under `templates/fixture/`, test input only |
| Fork | A GitHub fork of this repository carrying stacks, platforms, process rules and the interview |
| Frozen surface | What 3.x does not break: template paths, template and section IDs, the manifest shape |
| Hybrid | A context file that copies in the rules that matter and names the rest as files to read |
| Inline | A context file that copies in every rule |
| Interview | A fork's questions an agent asks before generating a context file |
| Layer template | A template under `frontend/` or `backend/` |
| Manifest | `templates/manifest.yaml`, the dependency graph and single source of truth |
| Opt-in | A template that reaches a chain only when a stack declares it |
| Orthogonal template | A template no stack declares, resolved as its own root |
| Platform | A fork's template mapping CI and security tools to one hosting platform |
| Profile | The context file generated for one project |
| Root | A template a project picks directly: a stack, a platform or an extra |
| Stack | A fork's technology-specific template, the main root of a chain |
| Upstream | This repository |
