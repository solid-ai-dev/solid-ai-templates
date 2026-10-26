# solid-ai-templates

The rules every agent applies in this repository. `CLAUDE.md` imports this
file. What the project is: `README.md`; how it works: `docs/spec.md`.

## 1. Project

### 1.1 Overview

- **Owner**: Imbra Ltd — Branimir Georgiev
- **Repo**: github.com/solid-ai-dev/solid-ai-templates
- **Stack**: plain Markdown templates; Python for `tools/`, `tests/` and the
  pre-commit hooks in `hooks/`, which run in consumers' CI (ADR-055)
- **Model**: inline — every rule is in this file
- **Upstream**: stacks, platforms, process templates and the interview
  live in forks (ADR-049, ADR-050), never here

### 1.2 Commands

`py` is the Windows launcher; on macOS and Linux run `python3`.

```bash
py tools/sync_docs.py              # regenerate generated sections
py tools/sync_docs.py --check      # exit 1 if any is stale
py tools/resolve_chain.py --roots   # every root a project can pick
py tools/resolve_chain.py <id>      # one root's resolved file list
py tools/resolve_chain.py --emit <dir> <root>...   # root file and task skills
py tests/run.py smoke         # structure and resolution
py tests/run.py conformance   # the templates' own checks, run here
py tests/run.py fork_sync     # the change merged into a simulated fork
PYTHONPATH=hooks py -m solid_ai_checks <hook-id>   # run one hook directly
```

The playbook lists the rest: release check, redundancy audit, quality
scorer.

## 2. Conventions

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
  the PR number either way
- A subject MUST NOT name an issue its PR does not close. The merged-work
  sweep fails on every open issue a merged subject names, so the part
  PRs of a split issue carry "Part of #N" in the body and only the PR
  that closes it carries `(#N)`
- Issue titles: sentence case, imperative verb — no type prefix
  (labels carry the type)
- PRs are small and focused — one concern per PR
- An agent never merges a PR. The maintainer approves each merge
  explicitly; green checks are not approval, and approval of one PR does
  not extend to the next
- After a PR is merged, delete the branch and pull `main` before
  starting new work
- Never force-push, including with `--force-with-lease`. To bring a
  branch up to date, merge `main` into it or run `gh pr update-branch`
- Do not commit `.idea/`, editor config, or any generated output

### 2.2 Issue labels

Every issue MUST have exactly one type label and one priority label,
applied at creation — never create a ticket unlabeled. A report filed
through an issue form carries only the form's type label; triage adds the
priority when it accepts it (playbook, "Triage a report").

| Type | When to use |
|------|-------------|
| `bug` | Defect in existing functionality |
| `epic` | Large initiative spanning multiple tasks |
| `task` | Atomic implementable work |
| `spike` | Research or exploration — output is a decision |
| `incident` | Production outage or degradation affecting users now |

| Priority | Meaning |
|----------|---------|
| `P0` | Critical — blocks everything |
| `P1` | High — must fix before next milestone |
| `P2` | Medium — important but not blocking |
| `P3` | Low — nice to have, including trivial |

There is no fifth band. Deferral is an empty milestone field, not a label:
milestoned means planned, unmilestoned means backlog (ADR-024). Triage
labels are terminal, applied when closing without action: `duplicate`
(tracked elsewhere) and `wontdo` (acknowledged, not addressed).

### 2.3 Templates

- Base and layer files are named for their concern (`core/quality.md`,
  `backend/http.md`). Upstream's only stack and platform are the fixture,
  test input only
- Stacks and platforms are added in a fork, never here. A fork registers
  them under `stacks:`, `platform:` or a key of its own and never edits
  `core:`, `base:`, `backend:` or `frontend:` (spec, chapter 8.6)
- A new base or layer template follows the playbook, "Add a new base or
  layer template"
- A review, rewrite or cut of a template follows the playbook, "Review a
  template"
- Every template file has an entry in `templates/manifest.yaml`; IDs are
  unique across all layers, and `depends_on` names only valid IDs
- Base entries go under `base:`, layer entries under `backend:` or
  `frontend:`; the fixture stays under `stacks:` and `platform:`

### 2.4 Template authoring

- Sections use imperative, direct language: "Use X", "Never Y",
  "Always Z". A plain imperative is a rule; an RFC 2119 keyword marks
  its strength where that matters (see 2.7)
- A rule MAY carry a short reason in the same bullet. Never put an
  explanatory paragraph between two items of one rule list — context
  goes in a lead-in paragraph above the list
- Keep a rule's condition and main exception; shorten it by splitting,
  never by dropping either. The score gate measures form, not whether a
  rule still applies correctly
- Give a section an `[ID: ...]` when something references it: another
  template EXTENDs or OVERRIDEs it, or a rule names it. Never remove or
  rename an existing ID — shipped IDs are frozen surface (spec, chapter 8.7)
- Add a new ID only on new content: a new file, or a heading after the
  last line a shipped section holds. An ID inserted inside a section
  shrinks it, and SYS-24 fails it
- Optional sections are marked `(if applicable)` in the heading
- Keep line length under 88 characters, the width declared in
  `.editorconfig` for Markdown and Python —
  exempt: table rows, fenced code, `[DEPENDS ON: ...]` directives, and
  unbreakable tokens (long URLs, Markdown link targets)
- Write a directive's name in prose, never its bracket form — a parser
  scanning for the form finds it in the sentence describing it
- No HTML — Markdown only
- No horizontal rule in any Markdown file — headings separate sections;
  `tools/check_horizontal_rules.py` gates it as a local pre-commit hook
- A mechanically-checkable output constraint MUST name its
  agent-runnable check (command + pass condition); subjective
  constraints stay declarative (see `quality-gates-pair-check`)
- A shipped check states its command in a fenced block, with the pass
  condition in prose beside it — a command typed into a sentence cannot
  be extracted, counted or run (ADR-031)
- A check script over 15 lines ships as a hook under `hooks/`, listed in
  `.pre-commit-hooks.yaml`; the template states
  `pre-commit run <hook-id> --all-files --verbose` (ADR-055). A shipped
  hook ID is frozen like a section ID
- A check that derives a comparison baseline by running a command MUST
  verify the command produced one and refuse when it did not — the
  refusal is a finding, never exit 3; see `base-quality-gates`
- Never name another file's section ID in running prose unless that file
  resolves into every chain carrying yours — state the substance inline
  instead; SYS-11 checks it per chain (spec, chapter 8.4)
- When a rule could live in either of two templates, measure both files'
  chain reach first and put it in the wider one (ADR-028)

### 2.5 Documentation

- Before every PR, update every document the change touches:
  - `AGENTS.md` — if a rule agents apply here changes
  - `README.md` — if the features or the quick setup change
  - `docs/architecture/` — if the composition model, inheritance rules
    or ID system change
  - `templates/manifest.yaml` — if a template is added, removed,
    renamed or re-depended
  - `docs/playbook.md` — if a procedure changes
  - `CONTRIBUTING.md` — if prerequisites or first steps change
  - `CHANGELOG.md` — an `Unreleased` entry for any change a consuming
    project would notice, in the same PR: one line of about fifteen plain
    words saying what changed, with no code formatting, ending with a link
    to the PR, which holds the why. A change needing no entry says so in the PR body
- Do not duplicate content across documents — cross-reference instead
- Never state a count about the tree in a document outside a generated
  block or a dated record; `tools/check_doc_figures.py` gates it as a
  local pre-commit hook
- Write in present tense — past or future tense indicates out-of-sync
  documentation

### 2.6 Decision records

- A decision record is owed only when a decision changes something a
  consuming project can observe without reading this repository — the
  composition model. Prose style, tooling, release procedure, naming and
  file layout do not, however consequential they are
- One coherent decision may cover related choices across several issues
  or PRs; do not require a record per implementation concern
- Until the first implementation of an ADR merges, the record MAY be
  rewritten or split in place; from then on it is history
- What is immutable in a merged ADR is the decision — the claims in
  Context, Decision, Alternatives considered and Consequences. Routine
  refinements update current docs; material changes need a new ADR.
  Supersession metadata and format-only edits are permitted
- Where a merged ADR and the templates disagree, the templates govern
  and the ADR stands as history
- Copy `docs/decisions/template.md` for a new ADR;
  `py tests/run.py smoke ADR-01` enforces the schema

### 2.7 Rule language

A rule in a template is a plain imperative ("Use X", "Never Y"), read as
MUST / MUST NOT, or carries an RFC 2119 keyword where strength matters
(`templates/core/docs.md`, "Rule language"):

| Word | Meaning |
|------|---------|
| MUST | Absolute requirement |
| MUST NOT | Absolute prohibition |
| SHOULD | Recommended — deviations require justification |
| MAY | Optional |

## 3. Quality

### 3.1 Checks

- CI runs smoke, conformance, fork sync, `check_release.py --self-test`,
  `sync_docs.py --check`, `resolve_chain.py --check`, the redundancy audit, the
  template-quality ratchet, pyflakes, markdownlint, the pre-commit hooks
  and gitleaks on every PR and on push to `main`
- Every runner writes a timestamped report to `tests/reports/`
  (gitignored); `docs/tests/index.md` lists every check
- markdownlint holds every tracked Markdown file to the rules; never add
  an `ignores` entry to `.github/linters/.markdownlint-cli2.jsonc`

### 3.2 Review priority

1. **Correctness** — do `[DEPENDS ON]`, `[EXTEND]`, `[OVERRIDE]`
   references resolve? Does the manifest entry match?
2. **Completeness** — are all required documents updated (see 2.5)?
3. **Clarity** — are rules imperative and unambiguous?
4. **Conventions** — does the template follow the authoring rules
   (see 2.4)?

## 4. Session protocol

### 4.1 Startup

1. Read `AGENTS.md` (this file) and `docs/spec.md`
2. Run `git branch --no-merged main` and flag any unmerged branch to the
   user — it may hold lost work
3. Confirm the scope with the user before making changes
4. If the task is ambiguous, ask: "What is the specific deliverable
   for this session?"

### 4.2 During the session

- Size the local checks to the change. A template, manifest, tool or test
  change runs `py tests/run.py smoke` and, for any template prose edit,
  `py tests/run.py conformance`: smoke reads structure, while every rule
  about the templates' own text, such as a check outside a fence, is
  enforced from conformance. A documentation-only change runs
  markdownlint and a scan for lines over 88 characters, and pushes once
- Adding a fenced `bash`/`python` block to a template MUST add its
  disposition in `tests/conformance/dispositions.py` — run it here, or skip it with
  the reason it does not apply. A block unrunnable only because it names
  a placeholder takes a `substitute`, not a skip. A hook command takes the
  arguments this repository runs it with in `args`. A judgement disposition
  MUST state what takes a person and name the check in
  `tests/conformance/reading-budget.txt`
- A conformance run is not clean until its judgement readings are read —
  `0 failed` counts only the automatic verdicts (playbook, "Run the test
  suite")
- Run `py tools/sync_docs.py` after the LAST template edit of a change, not
  the first — a section regenerated before a later edit is stale
- If a change affects multiple documents, update all in the same PR
- Do not drift from the agreed scope without checking with the user
- When a path-based shell query returns an unexpected empty or negative,
  first verify the working directory — an earlier `cd` persists
- Verify the branch, not only the directory, before trusting a
  measurement — a parallel session shares this checkout and moves HEAD
- Before running a control test, follow the playbook, "Control-test a
  check you are changing": commit first, plant where the check reads,
  assert the mutation landed, and force the path under test to run
- Report only measurements this session took. A figure an issue states
  about the tree on its filing date is not a claim about the tree now

### 4.3 End of session

When the user signals the end of a session ("wrap up", "let's finish",
"end session", "close out", or similar), print the checklist in the
playbook, "Wrap up a session", and execute each item in order, marking
each done with its result before the next. Do not batch, skip or
summarize.

## 5. Communication

- Concise, direct answers — no filler, no preamble, no restating the
  request before answering
- State your preferred option after presenting suggestions — do not make
  the user choose when you have a view
- Ask before assuming scope on an ambiguous instruction — do not silently
  expand it
- Brevity applies to analysis, reports and audit findings, not only to
  edit recaps — a long answer is not more thorough, it is harder to act on
- When the user says a finding is unclear, restate it concretely with a
  worked example; do not defend the original wording

| Verb | Meaning |
|------|---------|
| `next` | Move to the next item without asking for confirmation |
| `stop` | Stop working; this does NOT mean save or commit |
| `yes` | Proceed; do not summarise what you are about to do, just do it |
