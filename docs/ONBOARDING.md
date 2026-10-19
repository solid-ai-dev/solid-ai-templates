# Onboarding

Welcome to solid-ai-templates. This guide gets a new contributor from zero
to first PR.

## What this project is

A composable, SOLID-inspired template system for generating AI agent context
files. This repository is upstream: it holds the composition engine and the
policy every team shares.

```
templates/core/       → rules that apply to every project; security/,
                        infra/ and data/ sit beside it
templates/backend/    → rules for backend services and APIs
templates/frontend/   → rules for frontend and UI projects
templates/fixture/    → test input for the checks; no project reads it
tools/, tests/        → the resolver, sync, and the checks
```

Stacks, platforms, workflow and process rules, and the interview live in
forks. A project uses a fork, or forks upstream to make its own, and hands
its agent that fork's interview and a resolved chain. The first fork is
[Imbra-Ltd/imbra-ai-templates](https://github.com/Imbra-Ltd/imbra-ai-templates);
a stack template change belongs there, not here. ADR-049 and ADR-050 in
`docs/decisions/` set the boundary.

Read `docs/SPEC.md` for the full composition model before contributing.

## Prerequisites

- Git
- A Markdown editor (any)
- Python 3.x — for running the smoke, conformance and fork-sync runners.
  The contributor documents write it as `py`, the Windows launcher; on
  macOS and Linux run `python3` instead, and CI runs `python`
- GitHub CLI (`gh`), authenticated — for the issue, pull-request and
  release steps in `docs/PLAYBOOK.md`

## First steps

```bash
git clone https://github.com/solid-ai-dev/solid-ai-templates.git
cd solid-ai-templates
```

No build step — all templates are plain Markdown, so nothing is compiled
and nothing is packaged. The checks are the exception and do take a
dependency: they need Python and PyYAML, `pip install pyyaml`. Without it
the smoke runner refuses the run and names what is missing rather than
reporting the manifest-reading checks as failures.

Set up pre-commit hooks for local validation:
```bash
pip install pre-commit
pre-commit install
```

## Understand the structure

| File / folder | Read this to understand |
|---------------|------------------------|
| `docs/SPEC.md` | The full composition model — inheritance, OVERRIDE, EXTEND, IDs |
| `CLAUDE.md` | Rules for contributing to this repo |
| `templates/manifest.yaml` | Machine-readable dependency graph |
| `tools/resolve.py` | Dependency resolver — resolves a template's full chain |
| `docs/decisions/` | Decision records, including the fork model (ADR-049, ADR-050) |

## How templates relate

Every template that builds on others starts with `[DEPENDS ON: ...]` listing
its parent templates. Read those parent templates first — the child only adds
or overrides what differs from the parent. Every chain starts with the core
tier.

Example chain:
```
templates/core/quality.md + templates/core/git.md + ...
    ↓
templates/backend/http.md
    ↓
templates/backend/api.md
```

To see the full resolved chain for any root, run:
```bash
py tools/resolve.py --roots              # list every root
py tools/resolve.py backend-api          # print file list
py tools/resolve.py backend-api --concat # print concatenated content
```

## Check your setup

Run the structural smoke tests once. A `VERDICT: PASS` line confirms
Python, PyYAML and the checkout:

```bash
py tests/run_smoke.py
```

To see what a project receives, use a fork: its interview and a resolved
stack chain are the input an agent generates a context file from.

## Making your first contribution

- What a pull request must pass and carry: [CONTRIBUTING.md](../CONTRIBUTING.md)
- Step-by-step procedures, from adding a template to submitting a PR, and
  what each runner reports: [docs/PLAYBOOK.md](PLAYBOOK.md)

## Conventions to know before you write

- How a rule is worded, and which sections carry an `[ID: ...]`:
  [CONTRIBUTING.md, "Writing rules"](../CONTRIBUTING.md#writing-rules)
- `templates/manifest.yaml` must be updated whenever a file is added, removed, or
  renamed

## Maintainership

This project has a bus factor of 1 — Branimir Georgiev is the sole
author and maintainer. The mitigation is documentation: everything
needed to understand, maintain, and extend the project is in the
repository (docs/SPEC.md, CLAUDE.md, PLAYBOOK.md, ADRs in docs/decisions/,
dev journal). No oral knowledge transfer is required.

If the maintainer becomes unavailable, the project can be forked and
continued from the repository alone.

## Getting help

- `docs/SPEC.md` — answers most "how does X work" questions
- Open a "Question or idea" issue if something is still unclear —
  Discussions are not enabled. `CONTRIBUTING.md`, "Issues", lists the routes
