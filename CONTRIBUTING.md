# Contributing

How to set up, what a change has to carry, and how a report is handled.
`AGENTS.md` holds the rules every change follows,
[docs/playbook.md](docs/playbook.md) the step-by-step procedures, and
chapter 5 of [docs/spec.md](docs/spec.md) where each part lives.

## 1. Scope

This repository carries the composition engine and the policy every team
shares. Stacks, platforms, process rules and the interview live in forks,
so a change to one of them goes to the fork that carries it (ADR-049,
ADR-050).

## 2. Setup

| Tool | Needed for |
|------|------------|
| Git | Everything |
| Python 3 with PyYAML (`pip install pyyaml`) | The tools and checks |
| GitHub CLI (`gh`), authenticated | The issue, pull-request and release steps |
| pyflakes 4.0.2, Node.js, pre-commit | Optional, to run CI's linters locally |

The docs write `py`, the Windows launcher; on macOS and Linux run
`python3`. There is no build step. Clone and run the structural checks
once:

```bash
git clone https://github.com/solid-ai-dev/solid-ai-templates.git
cd solid-ai-templates
py tests/run.py smoke
```

A `VERDICT: PASS` line confirms Python, PyYAML and the checkout.

## 3. Local checks

Run every suite CI runs before opening a pull request, and regenerate the
derived sections after editing anything under `templates/`:

```bash
py tests/run.py all     # smoke, conformance and fork sync
py tools/sync_docs.py   # commit what it writes with your change
```

## 4. Change requirements

| Requirement | When | What it means |
|-------------|------|---------------|
| Evidence | Every change | The quality it serves (chapter 10) and the evidence that it does, or the defect it corrects; one team's preference is not evidence for every team |
| Changelog label | Every pull request | One `changelog:` label, and a title in plain words, which the release cut turns into the entry |
| Updated documents | Every change | Each document the change touches, as `AGENTS.md` 5.1 lists them |
| Manifest entry | A new template | An entry in `templates/manifest.yaml`; smoke fails a template without one |
| Template rules | A template edit | Imperative rules, resolvable references and the authoring rules in `AGENTS.md` section 4 |
| Context cost | A rule in a widely resolved file | What the addition is worth, in the pull request; SYS-16 fails a stack category that crosses a context-window tier until `tests/smoke/context-tiers.txt` records it |
| Decision record | A change to the composition model | A record copied from `docs/decisions/template.md`, as `AGENTS.md` 5.3 says |

## 5. Branches and pull requests

Branch names, the commit and title form, one concern per pull request and
the no-force-push rule are in
[`AGENTS.md` section 2](AGENTS.md#2-git-and-pull-requests). The playbook,
["Submit a pull request"](docs/playbook.md#submit-a-pull-request), gives
the steps in order.

## 6. Issues

### 6.1 Issue forms

Open an issue through a form on the
[new issue page](https://github.com/solid-ai-dev/solid-ai-templates/issues/new/choose).
A rule that produced a bad outcome in a real project is the most useful
report this project receives.

| Form | For |
|------|-----|
| Defect | A shared rule, check or tool that does the wrong thing |
| Proposal | Changing, removing or adding a shared rule |
| Question or idea | Something the docs do not answer, or an idea not yet a proposal |
| Private advisory | A vulnerability, reported as [SECURITY.md](SECURITY.md) says, never in a public issue |

### 6.2 Duplicate search

Search open and closed issues first, with two or three plain keywords:

```bash
gh search issues --repo solid-ai-dev/solid-ai-templates --match title,body <word> <word>
```

Comment on an open match with your version and evidence. File a defect
naming a closed match when your version was released after it closed,
since that is a regression.

### 6.3 Triage dispositions

Triage runs in batches and gives every report one disposition.

| Disposition | Meaning | Marked by |
|-------------|---------|-----------|
| Accept | Valid, in scope and worth its cost | Type and priority label; a milestone only once scheduled |
| Bounded investigation | Plausible, but needs a time-boxed look first | `spike` and a priority, with the time box in a comment |
| Needs information | Cannot be acted on as filed | A comment naming what is missing; closed after 30 days without it |
| Duplicate | Already tracked by a canonical issue | `duplicate`, closed, linked to the canonical issue |
| Decline | Out of scope, a local preference, or not worth its cost | `wontdo`, closed with the reason |

Accepted is not scheduled; only a milestone schedules work. A preference
that suits one project belongs in its own context file or in a fork.
