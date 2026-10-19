# solid-ai-templates

Composable, SOLID-inspired template system for generating AI agent context
files (CLAUDE.md, AGENTS.md, .cursor/rules/project.mdc, etc.) for any
project type.

## 1. Project

### 1.1 Overview

- **Name**: solid-ai-templates
- **Owner**: Imbra Ltd — Branimir Georgiev
- **Repo**: github.com/solid-ai-dev/solid-ai-templates
- **Stack**: plain Markdown — no build step, no runtime dependencies
- **Output**: context files for Claude Code, Cursor, GitHub Copilot,
  Codex CLI
- **Model**: inline — all rules are self-contained in this file

### 1.2 Architecture

```
templates/          # All template source files
  core/             # Cross-cutting foundation (git, docs, quality, testing, ...)
  security/         # Security rules
  infra/            # CI/CD, containers, deployment
  data/             # Data modeling, quality, governance, migration
  backend/          # Backend layer — HTTP, API, database, observability
  frontend/         # Frontend layer — UX, accessibility, CSS, SSG
  fixture/          # Test-input stack and platform — checked, never listed
  manifest.yaml     # Machine-readable dependency graph
docs/               # spec.md and architecture/ (arc42), playbook, decisions
tests/              # Smoke, conformance and fork-sync runners, specs, reports
tools/              # sync.py, resolve.py, release_check.py, audit_redundancy.py
```

Stacks, platforms, the workflow and process templates, the interview,
examples and generated chains live in forks (ADR-049, ADR-050); the first
is `Imbra-Ltd/imbra-ai-templates`.

### 1.3 Commands

```bash
# No build step — all templates are plain Markdown. `py` is the Windows
# launcher; on macOS and Linux run python3 instead
git clone https://github.com/solid-ai-dev/solid-ai-templates.git

# Sync generated sections after editing templates/manifest.yaml
py tools/sync.py            # update generated sections in docs and README
py tools/sync.py --check    # exit 1 if any file is out of sync

# Resolve dependency chain for a stack
py tools/resolve.py --list                    # list stack IDs
py tools/resolve.py --roots                   # list every root a project picks
py tools/resolve.py <stack-id>               # print resolved file list
py tools/resolve.py <stack-id> --concat      # print concatenated content

# Check a release's changelog cut and SemVer step
py tools/release_check.py vA.B.C             # from the release commit
py tools/release_check.py --self-test         # planted cases

# Audit redundant rules across resolved chains
py tools/audit_redundancy.py                 # exact in-chain duplicates
py tools/audit_redundancy.py --near          # include near-duplicates
py tools/audit_redundancy.py --check          # CI gate — fail on new dups

# Score template documents (docs/design/template-content-quality.md)
py tools/template_quality.py                 # every template's score
py tools/template_quality.py <file>          # one file's metrics and worst parts
py tools/template_quality.py --check         # CI gate — no score below baseline
py tools/template_quality.py --update        # re-record after improving a file
```

A project generates its context file from a fork: the fork's interview and
a resolved chain, handed to an agent (README, "Quick setup").

## 2. Code conventions

### 2.1 Git

- Branch: `main` (protected) — never commit directly
- Branch naming: `feat/<scope>`, `fix/<scope>`, `docs/<scope>`,
  `chore/<scope>`
- Commits: `<type>(<scope>): <summary>` — types: feat, fix, chore,
  docs, refactor
- PR titles: `<type>(<scope>): <summary> (#issue)` — same format
  as commits, with issue number(s) at the end
- A single-commit PR MUST carry the issue number in the commit subject
  too: GitHub squashes using the PR title only when the branch holds two
  or more commits, and the commit subject when it holds one. A PR that
  closes no issue — a changelog cut, a journal entry, one part of an
  issue split across several PRs — is outside this: the squash appends
  the PR number either way, so the merged subject still resolves to the
  work
- A subject MUST NOT name an issue its PR does not close. The merged-work
  sweep fails on every open issue a merged subject names, so the part
  PRs of a split issue carry "Part of #N" in the body and only the PR
  that closes it carries `(#N)`
- Issue titles: sentence case, imperative verb — no type prefix
  (labels carry the type)
- PRs are small and focused — one concern per PR, merged once its
  checks pass; no approving review is required, and none is enforced
- After a PR is merged, delete branch and pull main before starting
  new work
- Never force-push, including with `--force-with-lease`. To bring a
  branch up to date, merge `main` into it or run `gh pr update-branch`
- Do not commit `.idea/`, editor config, or any generated output

### 2.2 Issue labels

Every issue MUST have exactly one type label and one priority label,
applied at creation — never create a ticket unlabeled. Triage labels
are terminal — applied when closing without action.

A report filed through an issue form carries only the form's type
label, and the missing priority marks it untriaged. Triage adds the
priority when it accepts the report; a report closed without being
accepted needs none (playbook, "Triage a report").

#### Type labels (pick one)

| Label | Color | When to use |
|-------|-------|-------------|
| `bug` | `#C9372C` | Defect in existing functionality |
| `epic` | `#9F8FEF` | Large initiative spanning multiple tasks |
| `task` | `#579DFF` | Atomic implementable work |
| `spike` | `#6CC3E0` | Research or exploration — output is a decision |
| `incident` | `#AE2E24` | Production outage or degradation affecting users now |

#### Priority labels (pick one)

| Label | Color | Meaning |
|-------|-------|---------|
| `P0` | `#E06C00` | Critical — blocks everything |
| `P1` | `#FCA700` | High — must fix before next milestone |
| `P2` | `#EED12B` | Medium — important but not blocking |
| `P3` | `#4BCE97` | Low — nice to have, including trivial |

There is no fifth band. Deferral is carried by an empty milestone
field, not by a label — milestoned means planned, unmilestoned means
backlog (ADR-024).

#### Triage labels

| Label | Color | When to use |
|-------|-------|-------------|
| `duplicate` | `#C1C7D0` | Already tracked by another issue |
| `wontdo` | `#C1C7D0` | Acknowledged but will not be addressed |

### 2.3 Template naming convention

Base and layer files are named for their concern (`core/quality.md`,
`backend/http.md`). Upstream ships no stacks: a fork names its own, and
upstream's one stack is the fixture, `templates/fixture/stack.md`.

### 2.4 Inheritance model

```
concerns ──┬── frontend/ ──┐
           ├── backend/  ──┼── a fork's stacks
           └── a fork's platforms

concerns = core/, security/, infra/, data/
```

- Every stack declares `[DEPENDS ON: ...]` at the top
- Sections are tagged `[ID: ...]`, extended with `[EXTEND: ...]`,
  replaced with `[OVERRIDE: ...]`
- Platform templates are orthogonal to the stack chain — a project
  picks one platform regardless of stack, and it resolves as its own
  root, so its guaranteed context is the core tier plus its own
  `depends_on` tree and nothing from the stack (ADR-035); the same
  holds for every opt-in extra
- `templates/manifest.yaml` is the machine-readable dependency graph

### 2.5 Adding a stack or platform

Stacks and platforms are added in a fork, never here. A fork registers
them under `stacks:`, `platform:` or a key of its own and never edits
`core:`, `base:`, `backend:` or `frontend:` (spec, chapter 8.6). The fixture
stack and platform are test input only.

### 2.6 Adding a new base or layer template

1. Create the file in the correct directory:
   - `templates/core/` — foundation (git, docs, quality, etc.)
   - `templates/security/` — security rules
   - `templates/infra/` — CI/CD, containers, deployment
   - `templates/data/` — data modeling, quality, governance, migration
   - `templates/backend/` — backend services
   - `templates/frontend/` — frontend/UI projects
2. Tag the file with `[ID: <layer>-<name>]`
3. Tag with a unique `[ID: ...]` each section something references
   (see 2.7)
4. Register in `templates/manifest.yaml` under the correct layer
   key with a `description` field
5. Run `py tools/sync.py` — updates the generated sections
6. Reference from dependent templates via `[DEPENDS ON: ...]`

### 2.7 Template authoring rules

- Sections use imperative, direct language: "Use X", "Never Y",
  "Always Z". A plain imperative is a rule; an RFC 2119 keyword marks
  its strength where that matters (see "Rule language")
- A rule MAY carry a short reason in the same bullet. Never put an
  explanatory paragraph between two items of one rule list — context
  goes in a lead-in paragraph above the list
- Give a section an `[ID: ...]` when something references it: another
  template EXTENDs or OVERRIDEs it, or a rule names it. Never remove or
  rename an existing ID — shipped IDs are frozen surface (ADR-051)
- Optional sections are marked `(if applicable)` in the heading
- Keep line length under 88 characters, the width declared in
  `.markdownlint.json` for Markdown and `.editorconfig` for Python —
  exempt: table rows, fenced code, single-line `[DEPENDS ON: ...]`
  directives, and unbreakable tokens (long URLs / Markdown link
  targets)
- No HTML — Markdown only
- A mechanically-checkable output constraint MUST name its
  agent-runnable check (command + pass condition); subjective
  constraints stay declarative (see `quality-gates-pair-check`)
- A shipped check states its command in a fenced block, with the pass
  condition in prose beside it — a command typed into a sentence cannot
  be extracted, counted or run. A sentence naming no command states no
  check at all (ADR-031)
- A check that derives a comparison baseline by running a command MUST
  verify the command produced one and refuse when it did not — the
  refusal is a finding, never exit 3; see `base-quality`
- Never name another file's section ID in running prose unless that file
  resolves into every chain carrying yours — state the substance inline
  instead; SYS-11 checks it per chain (see spec, chapter 8.4, "Reach";
  section in prose")
- When a rule could live in either of two templates, measure both files'
  chain reach first and put it in the wider one, leaving the narrower to
  defer — the reverse gives the consumers in the gap a deferral and no
  rule (ADR-028)
- Stack templates follow the canonical section structure (ADR-017):
  MUST sections are Stack, Commands, Project structure (pure
  libraries exempt from the last); see ADR-017 for SHOULD/MAY tiers,
  ordering, and the `<Language> conventions` naming — gated by SYS-06

### 2.8 manifest.yaml

- Every template file MUST have a corresponding entry in
  `templates/manifest.yaml`
- IDs MUST be unique across all layers
- `depends_on` lists MUST reference valid IDs — no dangling
  references
- Base entries go under `base:`, layer under `backend:` or `frontend:`;
  the fixture stays under `stacks:` and `platform:`. A fork's templates
  go under a key of its own, and its core-tier additions under
  `fork_core:`

### 2.9 Documentation

#### Standard documents

| File | Purpose |
|------|---------|
| `README.md` | Front page: what it is, features, quick setup, links to the docs |
| `CLAUDE.md` | AI agent context and project rules (this file) |
| `docs/spec.md` | arc42 index of `docs/architecture/` — goals, context, building blocks, runtime, composition rules, quality, risks |
| `templates/manifest.yaml` | Machine-readable dependency graph for all templates (single source of truth for descriptions, labels, layers) |
| `docs/playbook.md` | Operational reference — how to add templates, validate a change, release |
| `docs/migrating-to-v3.md` | Moving a 2.x project or fork to v3.0 |
| `CHANGELOG.md` | Released versions and what changed in each; versions up to v2.63.0 are in the GitHub Releases (ADR-029) |
| `SECURITY.md` | Private disclosure route, supported versions, scope, acknowledgement window |
| `CONTRIBUTING.md` | Setup, orientation, and what a change is checked against — gates, manifest duty, authoring rules; links §2.1 for branch and commit form |
| `docs/design/` | Design documents deeper than a chapter — agent-context tradeoffs, template-content quality |

#### Documentation rules

- Before every PR, update all relevant documents:
  - `CLAUDE.md` — if architecture, naming conventions, or authoring
    rules change
  - `README.md` — if the features or the quick setup change
  - `docs/architecture/` — if the composition model, inheritance rules,
    or ID system change
  - `templates/manifest.yaml` — if any template is added, removed,
    renamed, or re-depended
  - `docs/playbook.md` — if the workflow for generating or
    validating changes
  - `CONTRIBUTING.md` — if prerequisites or first steps change
  - `CHANGELOG.md` — add an `Unreleased` entry for any change a
    consuming project would notice, in the same PR that makes it. A
    change needing no entry says so in the PR body rather than staying
    silent; a template change almost always needs one, and a change to
    this repo's own tooling or tests usually does not. Keep each entry
    within forty words, checked in that PR rather than at the cut
- Do not duplicate content across documents — cross-reference
  instead
- Write in present tense — past or future tense indicates
  out-of-sync documentation

#### Decision logs

- A decision record is owed only when a decision changes something a
  consuming project can observe without reading this repository — the
  composition model. Prose style, tooling, release procedure, naming and
  file layout do not, however consequential they are.
- Each ADR carries Context, a one-sentence Decision, Rationale, an
  optional Design, Alternatives considered, Consequences, Compatibility
  and Security
- One coherent architectural decision may cover related choices across
  several issues or PRs; do not require a record per implementation concern.
- Until the first implementation of an ADR merges, the record MAY be
  rewritten or split in place; from then on it is history
- What is immutable in a merged ADR is the decision — the claims
  made in Context, Decision, Alternatives considered and
  Consequences. Preserve those claims as history; routine refinements update
  current docs and the PR, while material architectural changes need a new ADR.
  Supersession
  metadata (`superseded_by` / `status` / `date`) and format-only
  edits that move no claim are both permitted
- Where a merged ADR and the templates disagree, the templates
  govern and the ADR stands as history. This repository owns the
  rules it applies, so a record describes a rule rather than
  departing from one, and a correction is complete when the rule is
  right in the templates — whether or not a new ADR was written. A
  project consuming the templates declares its own ordering
- ADR schema, introduced by ADR-010 with three statuses — YAML
  frontmatter required (`id` as quoted string, `status` in {Proposed,
  Accepted, Superseded, Rejected, Withdrawn}, `date` YYYY-MM-DD,
  `category` in {composition, templates, tooling, process, release},
  reciprocal `supersedes` / `superseded_by` links). Copy
  `docs/decisions/template.md` when authoring a new ADR;
  `py tests/run_smoke.py ADR-01` enforces the schema and governs where
  it and ADR-010 differ

#### Rule language

A rule in a template is a plain imperative ("Use X", "Never Y"), read as
MUST / MUST NOT, or carries an RFC 2119 keyword. Use a keyword where
strength matters — SHOULD or MAY for anything weaker
(`templates/core/docs.md`, "Rule language", states it for consumers):

| Word | Meaning |
|------|---------|
| MUST | Absolute requirement |
| MUST NOT | Absolute prohibition |
| SHOULD | Recommended — deviations require justification |
| MAY | Optional |

## 3. Quality

### 3.1 Testing

The suite lives in `tests/`:

| File | Purpose |
|------|---------|
| `tests/lib.py` | Shared utilities (constants, file reading, report writing, arg parsing) |
| `tests/run_smoke.py` | Smoke test runner (structural checks) |
| `tests/conformance.py` | Disposition per embedded check — run here, or skip with a reason |
| `tests/fork_checks.py`, `tests/fork_dispositions.py`, `tools/fork_examples.py` | A fork's own smoke checks, dispositions and chain examples, loaded when present; upstream carries none |
| `tests/run_conformance.py` | Runs the templates' own embedded checks against this repository |
| `tests/run_fork_sync.py` | Merges the change under test into a simulated fork and runs smoke on the result |

```bash
py tests/run_smoke.py              # structural checks
py tests/run_smoke.py SYS-01       # run one check by ID

py tests/run_conformance.py        # the templates' checks, against this repo
py tests/run_conformance.py --list # dispositions only, run nothing

py tests/run_fork_sync.py         # a fork that only appends merges HEAD
```

- Every runner writes a timestamped Markdown report to
  `tests/reports/` (gitignored)
- Spec files live in `tests/specs/` — see `tests/CODIFICATION.md`
  for the ID scheme and `tests/INDEX.md` for the full list
- CI runs smoke, conformance, fork sync, `release_check.py --self-test`,
  `sync.py --check`, `resolve.py --check`, the redundancy audit, the
  template-quality ratchet, pyflakes
  over `tools/` and `tests/`, markdownlint, the pre-commit hooks and
  gitleaks on PRs and on push to main
- markdownlint holds every tracked Markdown file to the rules; never add
  an `ignores` entry to `.markdownlint-cli2.jsonc`
- The e2e suite and the efficacy benchmark exercise stacks and the
  interview, so they live in the Imbra fork
- To validate a new template: run `py tests/run_smoke.py` and
  `py tests/run_conformance.py`

## 4. Identity

Not applicable — this project has no design system or brand voice.

## 5. Review process

### 5.1 Code review

Priority order (highest first):
1. **Correctness** — do `[DEPENDS ON]`, `[EXTEND]`, `[OVERRIDE]`
   references resolve? Does the manifest entry match?
2. **Completeness** — are all required documents updated (see 2.9)?
3. **Clarity** — are rules imperative and unambiguous?
4. **Conventions** — does the template follow authoring rules
   (see 2.7)?

### 5.2 Structure audit

Run `py tests/run_smoke.py` before every PR. It checks:
- All `[DEPENDS ON: ...]` reference existing files
- All `[EXTEND: ...]` and `[OVERRIDE: ...]` reference valid IDs
- All EXTEND/OVERRIDE targets are reachable in the resolved chain
- No chain overrides one section ID from two templates
- All manifest entries point to existing files
- All template files have a manifest entry
- No duplicate IDs across layers
- All stacks resolve to valid, non-empty file lists
- All resolved chains include core tier files
- SYS-15: every stack outside the `library` and `embedded` layers
  resolves the security tier
- SYS-16: no stack category crosses a context-window tier without
  `tests/context-tiers.txt` being updated in the same change
- SYS-17: every registered check names a spec document that exists and
  has a row in `tests/INDEX.md`
- SYS-18: every stack outside the categories recorded at the most
  constrained context tier resolves `base-quality-gates`, and each
  exemption's recorded reason still holds (ADR-044)
- SYS-19: `resolve.py` names a missing dependency and a dependency cycle,
  each with its own message and exit 1
- SYS-20: a fork leaves the manifest's upstream keys (`core`, `base`,
  `backend`, `frontend`) as it last merged them, against the ref in
  `SAIT_UPSTREAM_REF`; upstream sets none and passes against itself
- SYS-21: a fork's templates under a key of its own, and its `fork_core`
  additions to every chain, resolve
- SYS-22: a manifest entry's `deprecated` names an entry that exists and
  is not itself deprecated
- Prompt builds for all stacks

## 6. Session protocol

### 6.1 Startup

1. Read `CLAUDE.md` (this file) and `docs/spec.md`
2. Check for stale branches: run `git branch --no-merged main`
   and flag any unmerged branches to the user — they may contain
   lost work
3. Confirm the scope with the user before making changes
4. If the task is ambiguous, ask: "What is the specific deliverable
   for this session?"

### 6.2 During the session

- Run `py tests/run_smoke.py` after any template or manifest change, and
  `py tests/run_conformance.py` after any edit to a template's prose. The
  two runners read different things: smoke checks structure and
  resolution, while every rule the templates state about their own text —
  line width, a check stated outside a fence, a decision record's prose
  bounds — is enforced from conformance. A prose edit smoke passes can
  still be red in CI: one such edit put a 127-character line into every
  generated chain, 36 findings, with smoke green over it
- Adding a fenced `bash`/`python` block to a template MUST add its
  disposition in `tests/conformance.py` — run it here, or skip it with
  the reason it does not apply. `py tests/run_conformance.py` fails on a
  block with no entry, and on a skip stating no reason. A block unrunnable
  only because it names a placeholder is not a skip: resolve the
  placeholder with `substitute` so it runs, because a skip written against
  a placeholder describes the repository on the day it was written and
  nothing re-reads it when the repository grows the thing. A block whose
  pass condition declares a threshold
  takes a predicate, not a judgement; a judgement disposition MUST state
  what takes a person, and MUST name the check in
  `tests/reading-budget.txt` beside that reason. The runner fails on a
  judgement stating neither
- A conformance run is NOT clean until its judgement readings are read —
  `0 failed` counts only the automatic verdicts. The `not applicable`
  count is not among them: those checks answered by exiting 3 and need no
  reader (playbook, "Run the test suite")
- Run `py tools/sync.py` after the LAST template edit of a change, not
  the first — a generated section refreshed before a later edit is stale,
  and smoke does not read it, so it surfaces only in CI
- If a change affects multiple documents, update all in the same PR
- Do not drift from the agreed scope without checking with the user
- When a path-based shell query (`test -f`, `ls`, `git -C <path>`,
  `git submodule status`, `git ls-tree`, etc.) returns an
  unexpected empty/negative, FIRST verify the working directory
  (`pwd`) — shell tool cwd persists across commands and an earlier
  `cd` may make "from the repo root" diagnostics false-negative
- Verify the branch, not only the directory, before trusting a
  measurement — a parallel session shares this checkout and moves HEAD,
  so take any figure you will report from a worktree pinned to an
  explicit ref
- A control's plant MUST take a form the check actually inspects: a
  prose section proves nothing against a detector that fingerprints
  bullet lines, and the clean result reads as the check holding
- The inverse holds too: when a probe returns an unexpected *uniform*
  positive — every repository carries the file, every case passes —
  validate it against a control that MUST fail before believing it. A
  failed call is not always visible in the output: `gh api` prints the
  404 body to stdout, so `gh api <missing-path> --jq '.name'
  2>/dev/null` yields a non-empty string and reads as a hit for every
  input
- Stage or commit before running a control that mutates the tree. The
  revert step is `git checkout -- <path>`, which restores from the index
  and discards unstaged work without saying so — an uncommitted edit to
  the file under test is exactly what the control destroys
- A control MUST assert its mutation landed before its result is read.
  A pattern written with the wrong line endings edits nothing, the check
  then reports clean because the tree never changed, and that reads as
  the guard holding when it was never exercised
- That landing assertion MUST name the entity it mutated and compare its
  value before and after. An assertion that merely finds the planted
  value somewhere passes when a sibling already carried it, so it holds
  whether or not the edit landed — the weakest link in a control is the
  step that proves it happened
- A control MUST also force the path under test to run. Satisfying the
  precondition is not the same as exercising the code: a tool that
  writes nothing to a file already in its target state reports clean
  because it never executed, and that reads as the tool being innocent
  of what it is suspected of
- Plant the mutation where the check actually reads, not merely in the
  working tree. A check that reads committed state — `git show HEAD:`,
  `git ls-files`, a tag's tree — is untouched by an edit that is not
  staged or committed, so the run comes back byte-identical to the clean
  one. An identical result is the strongest thing a control can look
  like and the weakest thing it can be
- Report only measurements this session took. An issue states its
  measurement against the tree on its filing date; repeating that figure
  in a commit message or pull request body asserts it about the tree
  now, and the two differ precisely when the defect has since been fixed

### 6.3 End of session

When the user signals end of session ("wrap up", "let's finish",
"end session", "close out", or similar), print the full checklist
below and execute each item sequentially. Mark each item done
(with result) before moving to the next. Do not batch, skip, or
summarize — visible sequential execution prevents missed steps.

1. **Commits and push** — all changes committed and pushed (via
   PR if branch-protected)
2. **Close issues** — close completed issues (verify auto-close
   worked)
3. **Epic checklists** — update epic checklists if relevant
4. **ADRs** — record any architectural decisions in
   `docs/decisions/`
5. **Smoke tests** — run `py tests/run_smoke.py` and confirm all
   checks pass
6. **CLAUDE.md** — for each new convention/rule, place it by
   evaluating code → ADR → README → playbook → CLAUDE.md → memory in
   order. CLAUDE.md is the home ONLY if the
   agent MUST apply the rule on every turn.

   CLAUDE.md contains rules only — not changelogs, package
   architecture, per-feature progress, or session logs. Keep necessary
   qualifiers; paragraph length does not require an ADR.
7. **README.md** — for each new command, dependency, or structural
   change, is it reflected? Name the section.
8. **docs/architecture/** — for each change to composition model or ID
   system, is it reflected? Name the section.
9. **templates/manifest.yaml** — for each template added, removed,
   or re-depended, is it registered? Name the entry.
10. **CONTRIBUTING.md** — for each new tool, prerequisite, or
    setup step, is it documented? Name the section.
11. **docs/playbook.md** — for each new command, script, or
    workflow added, is it documented? Name the section.
12. **Template feedback** — consider a demonstrated shared defect or recurring
    need, reconcile existing issues, and act within the authorized scope.
    A reusable-looking preference alone requires no ticket or ADR.
13. **Branch cleanup** — delete local branches whose PRs have merged,
    verified against the PR record: `gh pr view <N> --json
    state,headRefOid` must report `MERGED`, then `git branch -D`.
    `git branch --merged` cannot see a squash merge and silently
    matches nothing; a `headRefOid` that differs from the local tip
    usually means `gh pr update-branch` rewrote the remote head, so
    inspect it rather than assume unpushed work
14. **Flag gaps** — if any of the above cannot be completed, flag
    it to the user before closing
15. **Dev journal** — add a session entry to `docs/dev-journal.md`
    (date, tool, key changes, PRs merged, issues closed/created). This
    item sits after flagging gaps because it is the only one whose output
    is a record of the others, and item 14 resolves into a change whenever
    a flagged gap has a fix small enough to apply on the spot. Written
    earlier, its merged-pull-request, issue and upstream lines are
    incomplete by construction, and an entry's account is fixed once
    written, so the correction costs a second entry for one session.
    Where the checklist runs twice in a session — a release wrap-up, then
    a close-out — only the last pass writes the entry; the earlier one
    records that the session owes it
16. **Summary** — summarize what was done and what's next

## 7. Communication

Communication defaults, inlined per this project's inline model.

- Concise, direct answers — no filler, no preamble, no restating the
  request before answering
- State your preferred option after presenting suggestions — do not make
  the user choose when you have a view
- Ask before assuming scope on an ambiguous instruction — do not silently
  expand it

### 7.1 Shorthand verbs

| Verb | Meaning |
|------|---------|
| `next` | Move to the next item without asking for confirmation |
| `stop` | Stop working; this does NOT mean save or commit |
| `yes` | Proceed; do not summarise what you are about to do, just do it |

### 7.2 Project additions

- Brevity applies to analysis, reports and audit findings, not only to
  edit recaps — a long answer is not more thorough, it is harder to act on
- When the user says a finding is unclear, restate it concretely with a
  worked example; do not defend the original wording
