# Contributing

Contributions are welcome. This document covers what a change has to satisfy
before it can be merged. It does not repeat the orientation material —
[docs/ONBOARDING.md](docs/ONBOARDING.md) explains what the project is and how
the templates compose, and [docs/PLAYBOOK.md](docs/PLAYBOOK.md) carries the
step-by-step procedure for each kind of change.

Start there if you have not worked in this repository before. Come back here
for the rules your pull request is checked against.

## What belongs upstream

This repository carries the composition engine and the policy every team
shares. Stacks, platforms, workflow and process rules, and the interview live
in forks, so a change to one of those goes to the fork that carries it, such
as [Imbra-Ltd/imbra-ai-templates](https://github.com/Imbra-Ltd/imbra-ai-templates).
ADR-050 in `docs/decisions/` sets the boundary.

## Before you open a pull request

Set up first: Python, PyYAML and the `py` versus `python3` launcher are in
[docs/ONBOARDING.md, "Prerequisites"](docs/ONBOARDING.md#prerequisites).
Then run the structural checks, which take about ten seconds:

```bash
py tests/run_smoke.py
```

Run fork sync too, which merges your change into a simulated fork and runs
smoke on the result. If you edited a template's prose, also run the
templates' own checks against this repository. CI runs both:

```bash
py tests/run_fork_sync.py
py tests/run_conformance.py
```

If you edited anything under `templates/`, regenerate the derived files as
well, and commit the result with your change:

```bash
py tools/sync.py
```

A pull request whose generated sections in `README.md` and `docs/SPEC.md` do
not match its templates fails CI. `py tools/sync.py --check` reports the
mismatch without writing anything.

## What a change has to carry

- **What it improves.** Name the quality the change serves — correctness,
  effectiveness, relevance, efficiency, predictability or maintainability,
  defined in `docs/design/design-notes.md`, section 22.1 — and the evidence
  that it does, or the defect it corrects. A measured result beats a
  plausible one, and a rule one team prefers is not evidence for every team
- **A manifest entry.** Every file under `templates/` has one in
  `templates/manifest.yaml`. A new template without an entry fails smoke
- **Resolvable references.** `[DEPENDS ON: ...]`, `[EXTEND: ...]` and
  `[OVERRIDE: ...]` must name things that exist and are reachable in the
  resolved chain
- **Updated documents.** If your change moves the composition model, update
  `docs/SPEC.md`; if it changes a command or the project structure, update
  `README.md`. `CLAUDE.md` section 2.9 lists which document owns what
- **A decision record** when the change moves what a consuming project
  observes without reading this repository — the composition model, such as
  a new layer or a change to the override model. Naming, prose style,
  tooling and file layout need none (`CLAUDE.md`, "Decision logs"). See
  `docs/decisions/` and copy `docs/decisions/TEMPLATE.md`
- **What it costs every chain carrying it.** A rule added to a widely
  resolved file is read by every project on those chains, on every turn.
  Nothing refuses the size, but crossing to a larger context window is
  refused: SYS-16 fails until the new tier is recorded in
  `tests/context-tiers.txt` in the same change.
  Say in the pull request what the addition is worth, and prefer stating a
  widened rule inside the paragraph that already carries the narrow version

## Writing rules

Template content is rules, not prose. The full authoring conventions are in
`CLAUDE.md` section 2.7; the ones contributors most often miss:

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
[`CLAUDE.md` section 2.1](CLAUDE.md#21-git). Agents apply them on every
turn, and human contributors follow the same ones.
[docs/PLAYBOOK.md, "Submit a pull request"](docs/PLAYBOOK.md#submit-a-pull-request)
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
carries them, as "What belongs upstream" says.

The forms ask only for what triage needs: the version, the affected stack
and template, expected and actual behaviour, and evidence. A rule that
produced a bad outcome in a real project is the most useful report this
project receives. Issue titles follow
[`CLAUDE.md` section 2.1](CLAUDE.md#21-git); the form applies the type
label, and triage adds the priority ([section 2.2](CLAUDE.md#22-issue-labels)).

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

This project has a single maintainer, so review latency varies. Reports
are triaged in batches rather than on arrival, and no response time is
promised for an issue or a pull request; the only time bound is the
security acknowledgement in [SECURITY.md](SECURITY.md). A report or pull
request that sits is not a rejection. `docs/ONBOARDING.md` records what
happens to the project if the maintainer becomes unavailable.
