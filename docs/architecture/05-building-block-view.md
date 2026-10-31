# 5. Building block view

Upstream's parts and what each is responsible for, first as a whole, then
inside each part. Each block names where it lives in the repository. In
the diagrams, a dashed arrow points from a block to the block it uses,
labelled with the use.

## 5.1 Level 1: upstream

![Upstream's building blocks. The coding agent runs the resolver and emitter, which reads the templates and the manifest. The templates name the shipped hooks, which pre-commit in a project's CI runs. Doc sync reads the manifest and the templates, and runs the resolver and emitter. The self-checks, which CI runs, check the manifest and the templates, run the templates' own checks and run the shipped hooks. The maintainer runs the maintenance tools, which resolve and score the templates through the manifest](../diagrams/building-blocks-overview.png)

| Block | Responsibility | Implementation | Source |
|-------|----------------|----------------|--------|
| Templates | Hold the shared rules, one concern per file | `templates/` | FR-01-01, FR-02-01, ADR-001 |
| Manifest | Registers every template with its ID and dependencies, the one source of truth for the graph | `templates/manifest.yaml` | FR-03-01, ADR-004 |
| Resolver and emitter | Turn a root into its ordered chain, and a chain into a root file and task skills | `tools/resolve_chain.py`, `tools/emit_context.py` | FR-04-01, FR-06-03, ADR-058, proposed |
| Doc sync | Writes the sections of the documentation derived from the manifest, the templates and the files the resolver and emitter build, such as context sizes, and fails on drift | `tools/sync_docs.py` | - |
| Shipped hooks | Run the checks too long for a fence, in a project's CI | `hooks/solid_ai_checks/`, `.pre-commit-hooks.yaml` | FR-07-02, ADR-055 |
| Self-checks | Check that the templates compose, that upstream obeys them, and that a fork still merges | `tests/` | FR-10-01, FR-10-02, ADR-030 |
| Maintenance tools | Check a release, audit redundancy and hold each template's score | `tools/` | QG-01-01, QG-03-02, QG-04-02 |

## 5.2 Level 2: templates

![The template groups as they compose. In a fork, stacks depend on the backend and frontend layers and declare the opt-in templates they need, such as security; platforms and the fork core sit beside them. Upstream holds the backend layer, which extends security, the frontend layer, which extends the core tier, the fixture, the security, infrastructure and data groups, the opt-in core files, the core tier, seeded into every chain, and the output contract, which the coding agent reads](../diagrams/building-blocks-templates.png)

| Block | Responsibility | Implementation | Source |
|-------|----------------|----------------|--------|
| Core tier | The rules every project gets, for Git, documentation, quality, testing and review | `templates/core/`, listed under `core:` | FR-03-02 |
| Opt-in core files | Configuration, quality gates, OOP, embedded checks and measurement, reached only when declared | `templates/core/` | FR-03-03 |
| Security | Application and pipeline security | `templates/security/` | FR-02-02 |
| Infrastructure | CI/CD, containers and deployment | `templates/infra/` | FR-03-03 |
| Data | Data modelling, quality, governance and migration | `templates/data/` | FR-03-03 |
| Backend layer | Rules every backend shares, from HTTP and APIs to jobs and observability | `templates/backend/` | FR-02-01 |
| Frontend layer | Rules every frontend shares, for UX, quality and content | `templates/frontend/` | FR-02-01 |
| Output contract | How the context file is written, read by the coding agent and not a rule in the chain | `templates/core/agents.md` | FR-05-02 |
| Fixture | One stack and one platform the checks read, which no listing offers | `templates/fixture/` | ADR-049 |

A fork extends upstream at these points, and never edits a file upstream
owns.

| Extension point | What a fork adds | Source |
|-----------------|------------------|--------|
| Stacks and platforms | Its own templates, under `stacks:`, `platform:` or a key of its own | FR-08-02, ADR-050 |
| Fork core | Templates every chain takes after the core tier, under `fork_core:` | FR-08-03 |
| Kinds of task | Task skills of its own, under `fork_tasks:` | ADR-058, proposed |
| Interview | The questions its projects answer before generating | ADR-049 |
| Suites | A test suite under `tests/`, which the suite runner finds | FR-10-02 |
| Checks, dispositions and examples | `tests/fork_checks.py`, `tests/fork_dispositions.py` and `tools/fork_examples.py`, loaded when present, which register its template directories, conformance dispositions and documentation examples | ADR-050 |

## 5.3 Level 2: manifest

![How a template reaches a chain. The resolver starts from a stack's root, seeds the core tier, follows depends_on into the opt-in tier and resolves an orthogonal template when the project picks it. It writes the chain in order, the core tier, the base templates the chain reaches, the layer templates, then the stack. An orthogonal root resolves to a chain of its own in the same way](../diagrams/building-blocks-manifest.png)

| Tier | Members | Reaches a chain | Source |
|------|---------|-----------------|--------|
| Core | `core:`, then a fork's `fork_core:` | Seeded into every chain, so it never needs declaring | FR-03-02 |
| Opt-in | CI (`cicd`, `quality-gates`), security, devsecops, containers, deployment, config, data | Only when a stack's `depends_on` names it | FR-03-03 |
| Orthogonal | Advanced data templates, embedded checks, measurement, a fork's platforms and workflow choices | Picked by the project, in a fork's interview where it has one, and resolved as a root of its own | FR-04-01 |

Every top-level list of entries except `core` and `fork_core` is a section
the resolver reads, so a fork keeps its templates under a key of its own
and never edits one upstream owns. The core tier, as the manifest states
it today:

<!-- generated:spec-core-tier -->
- `templates/core/quality.md`
- `templates/core/git.md`
- `templates/core/docs.md`
- `templates/core/testing.md`
- `templates/core/review.md`

8 `[DEPENDS ON]` tokens across 5 templates name one of these files, and 5
manifest entries name a core id in `depends_on`. Declaring one is redundant
rather than forbidden, since the seeding reaches the file either way and the
directive documents a dependency a reader would otherwise infer. Only the
seeding reaches `base-review`. A chain assembled by walking the directives
misses it and reports nothing, because nothing declares what is absent.
<!-- /generated:spec-core-tier -->

## 5.4 Level 2: resolver and emitter

![The resolver reads the root IDs, the manifest and the templates, and writes a file list or the concatenated chain. The emitter takes the chain from the resolver, reads the project's declined list, and writes the root file, read on every turn with its trigger table, and the task skills under .agents/skills, one per kind of task. With a mirror, it copies them where an agent reads only its own folder](../diagrams/building-blocks-resolver.png)

| Mode | In | Out | Source |
|------|----|-----|--------|
| `resolve_chain.py <root>` | A root ID | The chain's files, in order | FR-04-01 |
| `--concat` | A root ID | The chain's text, concatenated | FR-04-01 |
| `--roots` | The manifest | Every root a project can pick | FR-03-01 |
| `--emit <dir> <root>...` | Roots and the declined list | The root file and one skill per kind of task | FR-06-03, FR-06-04, FR-06-06 |
| `--inline-skills` | As `--emit` | One root file with the skills inlined, for an agent without skills | ADR-058, proposed |
| `--mirror <dir>` | As `--emit` | A copy of the skills where an agent reads only its own folder | ADR-058, proposed |

## 5.5 Level 2: self-checks

![The suite runner runs smoke, conformance, fork sync and any suite a fork adds. Smoke reads the manifest and the templates. Conformance extracts the checks from the templates and runs the shipped hooks. Fork sync merges the change into a simulated fork and runs smoke there. Every suite writes a timestamped report under tests/reports](../diagrams/building-blocks-checks.png)

`docs/tests/index.md` lists every check, and `docs/tests/codification.md`
its ID scheme.

| Block | Responsibility | Implementation | Source |
|-------|----------------|----------------|--------|
| Suite runner | Runs a suite by name, and finds a fork's suite with no edit | `tests/run.py` | FR-10-01 |
| Smoke | Checks that references resolve, IDs are unique and chains are valid, one module per family | `tests/smoke/` | FR-10-01 |
| Conformance | Gives every fenced check the templates ship a disposition, and runs each one that applies to upstream | `tests/conformance/` | ADR-030, FR-07-01 |
| Fork sync | Merges the change into a simulated fork that appends a stack, and runs smoke there | `tests/fork_sync/` | FR-10-02 |
| Test kit | The files, verdict words, arguments and report every suite shares | `tests/testkit/` | - |

## 5.6 Level 2: maintenance tools

| Tool | Responsibility | Source |
|------|----------------|--------|
| `tools/check_release.py` | Checks a release's changelog cut and SemVer step | QG-03-02 |
| `tools/audit_redundancy.py` | Finds a rule repeated across the sections of one resolved chain | QG-01-01 |
| `tools/score_templates.py` | Scores each template and holds it to its baseline | QG-04-02 |
| `tools/check_doc_figures.py` | Finds a count about the tree outside a generated block, as a local pre-commit hook | - |
| `tools/check_horizontal_rules.py` | Finds a horizontal rule in tracked Markdown, as a local pre-commit hook | - |
| `tools/ask_reviewers.py` | Asks several models to review the templates against the project goal and score them | - |
