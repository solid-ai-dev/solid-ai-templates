# 7. Deployment view

How the rules reach a project and where they run. Nothing of upstream runs
as a service. The templates travel as files at a released tag, the coding
agent reads them on a developer's machine, and pre-commit runs the shipped
hooks in the project's CI. A project chooses the source it takes the
rules from, how it holds them, and who moves its pin.

The diagram is a UML deployment diagram. A 3D box is a node, such
as a repository, a machine or an execution environment. An element drawn
inside a node is deployed on it. A line is a communication path, and its
arrow points from the side that opens it.

## 7.1 Level 1: from upstream to a project

![From upstream to a project. Upstream, solid-ai-templates, holds the templates and tools and the shipped hooks. A fork, such as imbra-ai-templates, fetches and merges upstream, and adds its stacks and platforms and, optionally, an updater. The project repository pins the templates to a release tag, by submodule, clone or copy, from upstream or from a fork, and holds AGENTS.md and CLAUDE.md, the task skills under .agents/skills, and the pre-commit configuration. The updater opens a pull request with a pin bump to the project. The developer's machine runs the coding agent, which clones the project and commits to it. The project's CI fetches the commit, and pre-commit fetches the shipped hooks from upstream at the pinned revision](../diagrams/deployment-distribution.png)

| Node | What it holds | Source |
|------|---------------|--------|
| Upstream | The templates, the tools and the shipped hooks, released as tags | FR-09-01 |
| A fork | Upstream's history, merged, with its own stacks, platforms and process | FR-08-01, ADR-050 |
| Project | The pinned templates, its context files, its task skills and its pre-commit configuration | FR-08-04, FR-05-04 |
| Developer's machine | The coding agent, which generates the context files from the project's copy of the templates | FR-05-01 |
| Project's CI | pre-commit, which fetches the shipped hooks at the revision the project pinned | FR-07-02, ADR-055 |

## 7.2 Source

| Source | What a project gets | Fits | Source |
|--------|---------------------|------|--------|
| Upstream | The core tier, the opt-in base templates and the layers, each of them a root; no stack | A project that wants the shared rules only | ADR-050 |
| A fork, such as imbra-ai-templates | Upstream, plus the fork's stacks, platforms, process and interview | A team with stacks of its own | ADR-049, ADR-050 |

A project moves from upstream to a fork without regenerating.

1. It points its copy at the fork, at a tag that contains the upstream
   tag it pins.
2. Its context files stay valid. A fork never edits a key upstream owns,
   and no 3.x release removes or renames a frozen ID (FR-08-02, FR-09-01).
3. It regenerates only to adopt a stack, as any adoption (chapter 6.5).

## 7.3 Attachment

Every model keeps the generated context files in the project. They differ
in where the templates live and whether the project's history records the
pin. A pin names a released tag, never a branch, because a revision
between two releases carries rules no release has cut (playbook, "Vendor
the templates in a project").

| Model | The pin | Update | Trade-off | Source |
|-------|---------|--------|-----------|--------|
| Submodule | In the project's history | Move the submodule to a newer tag | Each commit records the rules that governed it | FR-08-04 |
| Clone | Outside the project's history | Check out a newer tag | Simple, but no commit records which rules governed it | FR-08-04 |
| Copy | In the project's history, as files | Replace the copy with a newer tag's files | No submodule to initialise, but a local edit to the copy is lost on update | - |
| Hooks only | `rev:` in `.pre-commit-config.yaml` | Move `rev:` to a newer tag | The checks, without the rules | ADR-055 |

## 7.4 Update

The team moves the pin, by hand, when a release holds a rule it wants
(chapter 6.5). A fork may add an updater, a bot that watches releases and
proposes the move to its projects. Any updater follows these rules.

| Rule | Source |
|------|--------|
| It moves the pin to a released tag, never a branch | FR-08-04 |
| It proposes the move as a pull request, listing the changelog entries between the two tags as candidates | FR-09-03 |
| It never rewrites a context file. Moving the pin changes nothing, and adopting a rule stays the team's decision | FR-09-03 |
