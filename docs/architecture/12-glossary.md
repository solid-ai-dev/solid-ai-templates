# 12. Glossary

Each entry says what a term names. What the system does with it is a
requirement in [requirements.md](../requirements.md).

| Term | Meaning |
|------|---------|
| Base template | A template under `core/`, `security/`, `infra/` or `data/`, covering one concern for any project |
| Chain | The ordered list of templates a root resolves to |
| Context file | The file an agent reads at startup, such as `AGENTS.md`, `CLAUDE.md` or an agent's own format |
| Core tier | The templates seeded into every chain, `core:` and then a fork's `fork_core:` |
| Declaration block | The target header in a generated file naming its stack, extras and platform |
| Directive | A tag line a tool reads, one of `[ID:]`, `[DEPENDS ON:]`, `[EXTEND:]`, `[OVERRIDE:]` and `[LOAD:]` |
| Emitter | The tool that builds a project's root file and task skills from the adopted rules, `resolve_chain.py --emit` |
| Extra | An orthogonal template a project picks beside its stack |
| Fixture | The stack and platform under `templates/fixture/`, test input only |
| Fork | A GitHub fork of upstream carrying stacks, platforms, process rules and the interview |
| Frozen surface | What 3.x does not break, such as paths, IDs, the manifest schema, the core tier, exit codes, hooks and fork entry points (chapter 8.7) |
| Hook | A shipped check too long for a fence, which pre-commit runs from upstream at the pinned revision |
| Hybrid | A context file that copies in the rules that matter and names the rest as files to read |
| Inline | A context file that copies in every rule |
| Integration model | How a project holds the rules, by submodule, clone, copy, generated files only or hooks only (chapter 7.3) |
| Interview | A fork's questions an agent asks before generating a context file |
| Layer template | A template under `frontend/` or `backend/` |
| Load | Where a heading's rules are delivered, on every turn or in the skill for one kind of task (chapter 8.1) |
| Manifest | `templates/manifest.yaml`, the dependency graph and single source of truth |
| Opt-in | A template that reaches a chain only when a stack declares it |
| Orthogonal template | A template no stack declares, resolved as its own root |
| Pin | The released tag a project takes the templates or the hooks from |
| Platform | A fork's template mapping CI and security tools to one hosting platform |
| Root | A template a project picks directly, as a stack, a platform or an extra. Upstream has no stack, so every one of its templates is a root |
| Root file | The context file at a project's root, read on every turn, which lists the task skills that load on demand |
| Stack | A fork's technology-specific template, the main root of a chain |
| Task kind | A kind of task, such as `release`, that a load directive names and a skill serves, listed under the manifest's `tasks:` |
| Task skill | A folder under `.agents/skills/` holding the rules for one task kind, loaded when that task starts |
| Updater | A fork's optional bot that proposes moving a project's pin, as a pull request |
| Upstream | solid-ai-templates, the repository every fork merges from |
