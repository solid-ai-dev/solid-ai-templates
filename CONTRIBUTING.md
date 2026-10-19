# Contributing

Contributions are welcome. This document gets you set up and lists what a
change has to satisfy before it can be merged.
[docs/playbook.md](docs/playbook.md) carries the step-by-step procedure for
each kind of change.

## What belongs upstream

This repository carries the composition engine and the policy every team
shares. Stacks, platforms, workflow and process rules, and the interview live
in forks, so a change to one of those goes to the fork that carries it.
ADR-049 and ADR-050 in `docs/decisions/` set the boundary.

## Set up

You need:

- Git
- Python 3 with PyYAML (`pip install pyyaml`) for the checks. The docs write
  `py`, the Windows launcher; on macOS and Linux run `python3`, and CI runs
  `python`
- GitHub CLI (`gh`), authenticated, for the issue, pull-request and release
  steps in the playbook
- Optional, to run CI's linters before pushing: `pip install pyflakes==4.0.2`,
  Node.js for `npx --yes markdownlint-cli2@0.23.3`, and
  `pip install pre-commit` then `pre-commit install`

There is no build step: the templates are plain Markdown. Clone the
repository and run the structural checks once; a `VERDICT: PASS` line
confirms Python, PyYAML and the checkout:

```bash
git clone https://github.com/solid-ai-dev/solid-ai-templates.git
cd solid-ai-templates
py tests/run_smoke.py
```

## Find your way around

| Read | To understand |
|------|---------------|
| `docs/spec.md` | The architecture, arc42: the composition model is chapter 8 |
| `templates/manifest.yaml` | The dependency graph every tool reads |
| `docs/decisions/` | Why the model is the way it is |
| `docs/playbook.md` | How to make each kind of change |
| `AGENTS.md` | The rules an agent applies in this repository |

`py tools/resolve.py --roots` lists every root, and
`py tools/resolve.py <id>` prints the chain a root resolves to.

## Before you open a pull request

Run the structural checks, fork sync, and, if you edited a template's
prose, the templates' own checks against this repository. CI runs all
three:

```bash
py tests/run_smoke.py
py tests/run_fork_sync.py
py tests/run_conformance.py
```

If you edited anything under `templates/`, regenerate the derived files and
commit the result with your change. `py tools/sync.py --check` reports a
mismatch without writing anything, and CI fails on one:

```bash
py tools/sync.py
```

## What a change has to carry

- **What it improves.** Name the quality the change serves — correctness,
  effectiveness, relevance, efficiency, predictability or maintainability,
  defined in `docs/architecture/10-quality-requirements.md` — and the evidence
  that it does, or the defect it corrects. A measured result beats a
  plausible one, and a rule one team prefers is not evidence for every team
- **A manifest entry.** Every file under `templates/` has one in
  `templates/manifest.yaml`. A new template without an entry fails smoke
- **Resolvable references.** `[DEPENDS ON: ...]`, `[EXTEND: ...]` and
  `[OVERRIDE: ...]` must name things that exist and are reachable in the
  resolved chain
- **Updated documents.** If your change moves the composition model, update
  `docs/architecture/`; if it changes how a project sets up, update
  `README.md`. `AGENTS.md` section 2.5 lists which document owns what
- **A decision record** when the change moves what a consuming project
  observes without reading this repository — the composition model, such as
  a new layer or a change to the override model. Naming, prose style,
  tooling and file layout need none (`AGENTS.md`, "Decision records"). See
  `docs/decisions/` and copy `docs/decisions/template.md`
- **What it costs every chain carrying it.** A rule added to a widely
  resolved file is read by every project on those chains, on every turn.
  Nothing refuses the size, but crossing to a larger context window is
  refused: SYS-16 fails until the new tier is recorded in
  `tests/context-tiers.txt` in the same change.
  Say in the pull request what the addition is worth, and prefer stating a
  widened rule inside the paragraph that already carries the narrow version

## Writing rules

Template content is rules, not prose. The full authoring conventions are in
`AGENTS.md` section 2.4; the ones contributors most often miss:

- Write imperatively: "Use X", "Never Y". An RFC 2119 keyword — MUST,
  SHOULD, MAY — marks a rule's strength where it matters
- A short reason may sit in the bullet beside its rule; an explanatory
  paragraph between two rules of one list may not
- Give a section an `[ID: ...]` when another template or a rule
  references it, and never remove an existing one
- Keep lines under 88 characters. Table rows, fenced code and
  `[DEPENDS ON: ...]` lines are exempt
- A rule that can be checked mechanically MUST name the command that checks
  it and the condition that counts as passing. A rule that cannot stays
  declarative — do not invent a brittle check to satisfy this
- Markdown only, no HTML

## Branches, commits and pull requests

Branch names, the commit and pull-request title form, one concern per pull
request and the no-force-push rule are in
[`AGENTS.md` section 2.1](AGENTS.md#21-git). Agents apply them on every
turn, and human contributors follow the same ones.
[docs/playbook.md, "Submit a pull request"](docs/playbook.md#submit-a-pull-request)
gives the steps in order.

## Issues

Open an issue through a form on the
[new issue page](https://github.com/solid-ai-dev/solid-ai-templates/issues/new/choose):

| Route | For |
|-------|-----|
| Defect | A shared rule, check or tool that does the wrong thing |
| Proposal | Changing, removing or adding a shared rule |
| Question or idea | Something the docs do not answer, or an idea not yet a proposal |
| Private advisory | A vulnerability — see [Reporting a vulnerability](#reporting-a-vulnerability) |

Stacks, platforms, workflow rules and the interview go to the fork that
carries them, as "What belongs upstream" says. Discussions are not enabled.

The forms ask only for what triage needs: the version, the affected stack
and template, expected and actual behaviour, and evidence. A rule that
produced a bad outcome in a real project is the most useful report this
project receives. Issue titles follow
[`AGENTS.md` section 2.1](AGENTS.md#21-git); the form applies the type
label, and triage adds the priority ([section 2.2](AGENTS.md#22-issue-labels)).

### Search before filing

Search open and closed issues, titles and bodies, with two or three plain
keywords. A hyphenated or quoted phrase misses reports worded differently:

```bash
gh search issues --repo solid-ai-dev/solid-ai-templates --match title,body <word> <word>
```

- An open issue matches: comment there with your version and evidence
- A closed issue matches, and your version was released after it closed:
  that is a regression, so file a defect naming the closed issue
- Nothing matches: file a new issue

### What happens to a report

Triage gives every report one disposition:

| Disposition | Meaning | Marked by |
|-------------|---------|-----------|
| Accept | Valid, in scope and worth its cost | Type and priority label; a milestone only once scheduled |
| Bounded investigation | Plausible, but needs a time-boxed look before a decision | `spike` and a priority, with the time box in a comment |
| Needs information | Cannot be acted on as filed | A comment naming what is missing; no priority yet |
| Duplicate | Already tracked by a canonical issue | `duplicate`, closed, linked to the canonical issue |
| Decline | Out of scope, a local preference, or not worth its cost | `wontdo`, closed with the reason |

Accepting a report is not a promise to deliver it. Accepted work waits in
the backlog, with no milestone, until a release selects it; only a
milestone means scheduled. A report still waiting for information 30 days
after the request is closed, and reopened when the information arrives.

A proposal can be accepted as no change, with the reason stated. A
preference that suits one project belongs in that project's own context
file or in a fork, not in the shared rules.

## Reporting a vulnerability

Do not open a public issue. See [SECURITY.md](SECURITY.md) for the private
disclosure route.

## Maintainership

This project has a single maintainer, Branimir Georgiev, so review latency
varies. Reports are triaged in batches rather than on arrival, and no
response time is promised for an issue or a pull request; the only time
bound is the security acknowledgement in [SECURITY.md](SECURITY.md). A
report or pull request that sits is not a rejection.

Everything needed to understand, maintain and extend the project is in the
repository: the spec, the playbook, the decision records and `AGENTS.md`.
If the maintainer becomes unavailable, the project can be forked and
continued from the repository alone.
