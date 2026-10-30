# 7. Deployment view

How the rules reach a project and where they run. Nothing of upstream runs
as a service. The templates travel as files at a released tag, the coding
agent reads them on a developer's machine, and pre-commit runs the shipped
hooks on that machine and again in the project's CI. A project chooses
the source it takes the rules from, how it holds them, and who moves its
pin.

The diagram is a UML deployment diagram. A 3D box is a node, such
as a repository, a machine or an execution environment. An element drawn
inside a node is deployed on it. A line is a communication path, and its
arrow points from the side that opens it.

## 7.1 Deployment overview

![Deployment overview. Upstream, solid-ai-templates, holds the templates and tools and the shipped hooks. A fork, such as imbra-ai-templates, fetches and merges upstream, and adds its stacks and platforms and, optionally, an updater. The project repository pins the templates to a release tag, by submodule, clone or copy, from upstream or from a fork, and holds AGENTS.md and CLAUDE.md, the task skills under .agents/skills, and the pre-commit configuration. The updater opens a pull request with a pin bump to the project. The developer's machine runs the coding agent, which clones the project and commits to it, and pre-commit on each commit. The project's CI checks out the pushed commit and runs pre-commit on each push. Both pre-commit runs fetch the shipped hooks from upstream at the pinned revision](../diagrams/deployment-distribution.png)

| Node | What it holds | Source |
|------|---------------|--------|
| Upstream | The templates, the tools and the shipped hooks, released as tags | FR-09-01 |
| A fork | Upstream's history, merged, with its own stacks, platforms and process | FR-08-01, ADR-050 |
| Project | The pinned templates, its context files, its task skills and its pre-commit configuration | FR-08-04, FR-05-04 |
| Developer's machine | The coding agent, which generates the context files from the project's copy of the templates, and pre-commit, which git's hook runs on each commit for early feedback | FR-05-01, ADR-055 |
| Project's CI | pre-commit, on each push, the gate every change passes, since a local hook is optional and can be skipped. Both runs fetch the shipped hooks at the revision the project pinned | FR-07-02, ADR-055 |

## 7.2 Distribution sources

| Source | What a project gets | Fits | Source |
|--------|---------------------|------|--------|
| Upstream | The core tier, the opt-in base templates and the layers, each of them a root; no stack | A project that wants the shared rules only | ADR-050 |
| A fork, such as imbra-ai-templates | Upstream unchanged, plus the fork's stacks, platforms, process and interview | A team with stacks of its own. A project on upstream moves to it without regenerating its context files | ADR-049, ADR-050, FR-08-02, FR-09-01 |

## 7.3 Integration models

Every model pins a released tag, never a branch (playbook, "Vendor the
templates in a project").

| Model | Brings | The pin | Update | Trade-off | Source |
|-------|--------|---------|--------|-----------|--------|
| Submodule | Templates and generated context files | In the project's history | Move the submodule to a newer tag | Each commit records the rules that governed it | FR-08-04 |
| Clone | Templates and generated context files | Outside the project's history | Check out a newer tag | Simple, but no commit records which rules governed it | FR-08-04 |
| Copy | Templates and generated context files | In the project's history, as files | Replace the copy with a newer tag's files | No submodule to initialise, but a local edit to the copy is lost on update | - |
| Hooks only | The shipped checks, run by pre-commit | `rev:` in `.pre-commit-config.yaml` | Move `rev:` to a newer tag | The checks, without the rules | ADR-055 |

## 7.4 Version updates

The team moves the pin, by hand, when a release holds a rule it wants
(chapter 6.5). A fork may add an updater, a bot that watches releases and
proposes the move to its projects. Any updater follows these rules.

| Rule | Source |
|------|--------|
| It moves the pin to a released tag, never a branch | FR-08-04 |
| It proposes the move as a pull request, listing the changelog entries between the two tags as candidates | FR-09-03 |
| It never rewrites a context file. Moving the pin changes nothing, and adopting a rule stays the team's decision | FR-09-03 |
