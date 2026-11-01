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

## 2. Git and pull requests

- Never commit to `main`, which is protected; work on a branch named
  `feat/<scope>`, `fix/<scope>`, `docs/<scope>` or `chore/<scope>`
- Write a commit subject as `<type>(<scope>): <summary>`, with the type
  feat, fix, chore, docs or refactor
- Title a PR the same way, ending with the issues it closes:
  `<type>(<scope>): <summary> (#issue)`
- Put the issue number in the commit subject of a single-commit PR too;
  GitHub squashes with the commit subject when the branch holds one commit
- Leave the issue number out of the title and commit subject of a PR that
  closes none, such as a changelog cut or one part of a split issue; the
  squash appends the PR number
- Never name an issue in a subject whose PR does not close it; the
  merged-work sweep fails on every open issue a merged subject names
- Mark each part PR of a split issue "Part of #N" in its body; only the PR
  that closes the issue carries `(#N)`
- Keep each PR small, one concern per PR
- Never merge a PR as an agent; the maintainer approves each merge
  explicitly
- Never read green checks as approval, or one PR's approval as approval of
  the next
- Delete the branch and pull `main` after a PR merges, before new work
- Never force-push, `--force-with-lease` included; update a branch by
  merging `main` into it or with `gh pr update-branch`
- Never commit `.idea/`, editor config or generated output

## 3. Issues

- Title an issue in sentence case with an imperative verb and no type
  prefix; the labels carry the type
- Give every issue exactly one type label and one priority label at
  creation; never create one unlabeled
- Add the priority to a report filed through an issue form when triage
  accepts it, since the form sets only the type (playbook, "Triage a
  report")

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

- Use no fifth priority band
- Mark deferral with an empty milestone field, never a label; a
  milestoned issue is planned, an unmilestoned one is backlog (ADR-024)
- Close an issue without action with a terminal label, `duplicate` when it
  is tracked elsewhere and `wontdo` when it is acknowledged, not addressed

## 4. Templates

### 4.1 Files and the manifest

- Name a base or layer file for its concern, such as `core/quality.md` or
  `backend/http.md`
- Add stacks and platforms in a fork, never here; upstream's only stack
  and platform are the fixture, which is test input only
- Register a fork's templates under `stacks:`, `platform:` or a key of its
  own (spec, chapter 8.6)
- Never edit `core:`, `base:`, `backend:` or `frontend:` in a fork
- Give every template file an entry in `templates/manifest.yaml`, with an
  ID unique across all layers and a `depends_on` naming only valid IDs
- Put base entries under `base:` and layer entries under `backend:` or
  `frontend:`; keep the fixture under `stacks:` and `platform:`
- Follow the playbook, "Add a new base or layer template", to add one
- Follow the playbook, "Review a template", to review, rewrite or cut any
  template

### 4.2 Rules and sections

A rule in a template is a plain imperative ("Use X", "Never Y"), read as
MUST / MUST NOT, or carries an RFC 2119 keyword where strength matters
(`templates/core/docs.md`, "Rule language"):

| Word | Meaning |
|------|---------|
| MUST | Absolute requirement |
| MUST NOT | Absolute prohibition |
| SHOULD | Recommended — deviations require justification |
| MAY | Optional |

- Write each rule as a direct imperative, such as "Use X", "Never Y" or
  "Always Z"
- Give a rule at most a short reason in its own bullet; put context in a
  lead-in above the list, never between two items of one list
- Keep a rule's condition and main exception; shorten it by splitting,
  never by dropping either, since the score gate measures only form
- Give a section an `[ID: ...]` when another template extends or overrides
  it, or a rule names it
- Never remove or rename an existing ID; shipped IDs are frozen (spec,
  chapter 8.7)
- Add a new ID only on new content, in a new file or under a heading after
  the last line a shipped section holds; SYS-24 fails an ID inserted inside
  a section, which shrinks it
- Mark an optional section `(if applicable)` in its heading
- Keep lines under 88 characters, the width `.editorconfig` declares for
  Markdown and Python
- Exempt from the width only table rows, fenced code, `[DEPENDS ON: ...]`
  directives and unbreakable tokens, such as long URLs and link targets
- Write a directive's name in prose, never its bracket form; a parser
  scanning for the form finds it in the sentence describing it
- Write Markdown only, with no HTML
- Never use a horizontal rule in any Markdown file; headings separate
  sections, and `tools/check_horizontal_rules.py` gates it as a local
  pre-commit hook
- Never name a template file's path in a template's prose, since an
  emitted project carries the rules, not the templates; name the section by
  its heading, which SYS-27 checks in every root's emitted files
- Never name another file's section ID in running prose unless that file
  resolves into every chain carrying yours; state the substance inline,
  which SYS-11 checks per chain (spec, chapter 8.4)
- Measure both files' chain reach before placing a rule that could live in
  either, and put it in the wider one (ADR-028)

### 4.3 Shipped checks

- Name the agent-runnable check, command and pass condition, of every
  mechanically checkable output constraint; keep subjective constraints
  declarative (see `quality-gates-pair-check`)
- State a shipped check's command in a fenced block, with its pass
  condition in prose beside it; a command typed into a sentence cannot be
  extracted, counted or run (ADR-031)
- Ship a check script over 15 lines as a hook under `hooks/`, listed in
  `.pre-commit-hooks.yaml`, and state
  `pre-commit run <hook-id> --all-files --verbose` in the template
  (ADR-055)
- Never rename a shipped hook ID; it is frozen like a section ID
- Make a check that derives its comparison baseline by running a command
  verify that the command produced one, and refuse when it did not
- Report that refusal as a finding, never as exit 3; see
  `base-quality-gates`
- Give every fenced `bash` or `python` block added to a template a
  disposition in `tests/conformance/dispositions.py`, run here or skipped
  with its reason (playbook, "Run the test suite")

## 5. Documentation

### 5.1 Keeping documents current

- Update every document a change touches before opening its PR, in that
  PR:
  - `AGENTS.md` — if a rule agents apply here changes
  - `README.md` — if the features or the quick setup change
  - `docs/architecture/` — if the composition model, inheritance rules
    or ID system change
  - `templates/manifest.yaml` — if a template is added, removed,
    renamed or re-depended
  - `docs/playbook.md` — if a procedure changes
  - `CONTRIBUTING.md` — if prerequisites or first steps change
  - `CHANGELOG.md` — if a consuming project would notice the change
- Write a changelog entry under `Unreleased` as one line of about fifteen
  plain words saying what changed, with no code formatting
- End the entry with a link to the PR, which holds the why; say in the PR
  body when a change needs no entry
- Cross-reference instead of duplicating content across documents
- Never state a count about the tree outside a generated block or a dated
  record; `tools/check_doc_figures.py` gates it as a local pre-commit hook
- Write in present tense; past or future tense marks documentation that
  is out of sync

### 5.2 Architecture documents

These hold for `docs/spec.md` and the chapters in `docs/architecture/`.

- Name a section with a neutral, technical noun phrase, such as
  "Integration models"; never a question or a conversational phrase
- Never put a colon in the middle of a sentence
- Cite requirements and decision records in a table's Source column; a
  lead-in above a table explains in plain words and cites nothing
- Never cite or quote the playbook, and never write a procedure as steps;
  cite the requirement or the record the procedure implements
- Refer back to an earlier chapter, never forward to a later one
- Never cite a document as the source of its own claims

### 5.3 Decision records

- Write a decision record when a decision changes something a consuming
  project can observe without reading this repository, the composition
  model; only such a decision owes one
- Owe no record for prose style, tooling, release procedure, naming or
  file layout, however consequential they are
- Let one record cover related choices across several issues or PRs when
  they form one coherent decision; never require one per implementation
  concern
- Rewrite or split a record in place only until its first implementation
  merges; from then on it is history
- Never change the decision in a merged record, the claims in its Context,
  Decision, Alternatives considered and Consequences
- Update current docs for a routine refinement, and write a new record for
  a material change; supersession metadata and format-only edits are
  permitted in a merged record
- Let the templates govern where a merged record disagrees with them; the
  record stands as history
- Copy `docs/decisions/template.md` for a new record;
  `py tests/run.py smoke ADR-01` enforces its schema

## 6. Quality

### 6.1 Checks

- CI runs smoke, conformance, fork sync, `check_release.py --self-test`,
  `sync_docs.py --check`, `resolve_chain.py --check`, the redundancy audit,
  the template-quality ratchet, pyflakes, markdownlint, the pre-commit
  hooks and gitleaks on every PR and on push to `main`
- Every runner writes a timestamped report to `tests/reports/`
  (gitignored); `docs/tests/index.md` lists every check
- Hold every tracked Markdown file to markdownlint; never add an `ignores`
  entry to `.github/linters/.markdownlint-cli2.jsonc`

### 6.2 Review priority

1. **Correctness** — do `[DEPENDS ON]`, `[EXTEND]`, `[OVERRIDE]`
   references resolve? Does the manifest entry match?
2. **Completeness** — are all required documents updated (see 5.1)?
3. **Clarity** — are rules imperative and unambiguous?
4. **Conventions** — does the template follow the authoring rules
   (see 4.2 and 4.3)?

## 7. Session protocol

### 7.1 Startup

1. Read `AGENTS.md` (this file) and `docs/spec.md`
2. Run `git branch --no-merged main` and flag any unmerged branch to the
   user — it may hold lost work
3. Confirm the scope with the user before making changes
4. If the task is ambiguous, ask: "What is the specific deliverable
   for this session?"

### 7.2 During the session

- Size the local checks to the change:
  - Run `py tests/run.py smoke` for a template, manifest, tool or test
    change
  - Run `py tests/run.py conformance` as well for any template prose edit;
    smoke reads structure, and every rule about the templates' own text is
    enforced from conformance
  - Run markdownlint and a scan for lines over 88 characters for a
    documentation-only change, and push once
- Read a conformance run's judgement readings before calling it clean;
  `0 failed` counts only the automatic verdicts (playbook, "Run the test
  suite")
- Run `py tools/sync_docs.py` after the last template edit of a change,
  never the first; a section regenerated before a later edit is stale
- Check with the user before drifting from the agreed scope
- Verify the working directory first when a path-based shell query returns
  an unexpected empty or negative; an earlier `cd` persists
- Verify the branch, not only the directory, before trusting a
  measurement; a parallel session shares this checkout and moves HEAD
- Follow the playbook, "Control-test a check you are changing", before a
  control test: commit first, plant where the check reads, assert the
  mutation landed, and force the path under test to run
- Report only measurements this session took; a figure an issue states
  about the tree on its filing date is no claim about the tree now

### 7.3 End of session

When the user signals the end of a session ("wrap up", "let's finish",
"end session", "close out", or similar), print the checklist in the
playbook, "Wrap up a session", and execute each item in order, marking
each done with its result before the next. Do not batch, skip or
summarize.

## 8. Communication

- Answer concisely and directly, with no filler, no preamble and no
  restating of the request
- State your preferred option after presenting suggestions; never make the
  user choose when you have a view
- Ask before assuming scope on an ambiguous instruction; never expand it
  silently
- Keep analysis, reports and audit findings brief, not only edit recaps; a
  long answer is not more thorough, it is harder to act on
- Restate a finding the user calls unclear concretely, with a worked
  example; never defend the original wording

| Verb | Meaning |
|------|---------|
| `next` | Move to the next item without asking for confirmation |
| `stop` | Stop working; this does NOT mean save or commit |
| `yes` | Proceed; do not summarise what you are about to do, just do it |
