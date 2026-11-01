# 8. Crosscutting concepts

The concepts that hold across every template, tool and fork. They cover
how sections combine, which rule wins, how far a reference reaches, what a
fork may change, what 3.x freezes, how rules are written, what a root
costs in context, which level owns a rule, and how a template's form is
scored.

## 8.1 Sections, IDs and directives

A section that something references carries a unique ID. A later template
extends or replaces it by naming that ID; with neither, the section is used
as written.

```markdown
## Git conventions [ID: base-git]
- Base rules

## Git conventions [EXTEND: base-git]
- Do not commit `dist/`            <- added on top of the base rules

## Git conventions [OVERRIDE: base-git]
- Always run `npm run dev` first   <- replaces the base rules
```

A heading may carry several tag lines:

```markdown
## Heading
[ID: section-id]
[DEPENDS ON: path/to/dep.md, path/to/other.md]
[EXTEND: parent-id]
[LOAD: release]
```

- `[ID:]` names the section and comes first
- `[DEPENDS ON:]` declares file-level dependencies; it is metadata, not
  content, and may be split over several lines to keep the width
- `[EXTEND:]` or `[OVERRIDE:]` declares the relationship to a parent
- `[LOAD:]` says where the heading's rules load, either a kind of task
  the manifest's `tasks:` lists, such as `release`, or `check` for rules a
  check enforces. A heading without one loads on every turn, and a
  heading's subheadings take its load (ADR-058, proposed)
- A heading carries one load at most, among its tags, and none under a
  heading that has one. A template that guards data, credentials or
  authentication carries none. SYS-25 checks each of these
- A section runs from its tags to the next `[ID:]` or the end of the file,
  and is never empty
- Shipped IDs are frozen, never removed, renamed or moved to another
  file inside a major, and a new ID never splits a shipped section (8.7)

`[DEPENDS ON]` lists direct dependencies only, matching the manifest's
`depends_on` for the entry. The manifest wins a mismatch, and SYS-04 checks
it.

## 8.2 Precedence

When several templates name one section ID, the higher level wins:

1. Base template, the default
2. Layer template, frontend or backend
3. Stack template
4. Interview answers, which always win

`core/testing.md` sets a test naming convention, a fork's Python stack
extends it, and the interview answer "use BDD-style names" overrides both.

## 8.3 Conflicts

When two templates in one chain name the same ID, the kind of each
settles which rule applies.

| Situation | Resolution | Source |
|-----------|------------|--------|
| One template extends, another overrides one ID | The override replaces the base, and the extension applies on top | FR-04-03 |
| Two templates override one ID | The chain is refused, and TPL-10 fails it | FR-04-04, ADR-039 |
| Two templates extend one ID | Both apply, in the stack's declared dependency order | FR-04-03 |

To specialise across three levels, each override declares an ID of its own
and the next level overrides that:

```text
frontend/content.md           [ID: static-site-content]
stack/static-site-astro.md    [ID: astro-content]    [OVERRIDE: static-site-content]
stack/static-site-tutorial.md [ID: tutorial-content] [OVERRIDE: astro-content]
```

## 8.4 Chain reach

A rule that names another file's section in running prose is not a
directive, and the resolver does not resolve it. It reads correctly only in
chains that carry both files. Never name a section from a file that is
absent from some chain carrying yours; state the substance inline. SYS-11
checks this per chain (FR-01-03, ADR-028).

An orthogonal template is the sharpest case. Its guaranteed context is the
core tier plus its own `depends_on` tree, so every `[EXTEND]` and prose
reference in it resolves there (ADR-035).

When a rule could live in either of two templates, measure both files' chain
reach and put it in the wider one.

## 8.5 Opt-in tier membership

Two opt-in tiers are not left to what the dependency declarations produce.
Membership is stated by stack category, the `layer` a stack declares, with
a reason for each exempt category, and a smoke check enforces it both
ways. A list of stack IDs would be correct the day it is written and
silently wrong at the next stack.

| Tier | Exempt categories | Reason | Check | Source |
|------|-------------------|--------|-------|--------|
| Security | library, embedded | A library's caller owns the trust boundary; an embedded target has no HTTP surface, sessions or TLS | SYS-15 | FR-02-02, ADR-044 |
| Quality gates | Named by a fork in `tests/fork_checks.py` | A category at the most constrained context tier cannot admit the tier without changing which models can run it | SYS-18 | ADR-044 |

## 8.6 Fork contract

What a fork may change, and how it stays current with upstream.

| Mechanism | Rule | Source |
|-----------|------|--------|
| Sync by merge | A fork stays current with `git merge upstream/main`, never by copying files | FR-08-01, ADR-049 |
| Keys of its own | A fork appends under `stacks:`, `platform:` and keys of its own, never `core:`, `base:`, `backend:` or `frontend:`. SYS-20 checks the upstream keys against `SAIT_UPSTREAM_REF` | FR-08-02 |
| `fork_core` | Joins every chain's core tier after `core:`; an entry there depends only on core-tier IDs. SYS-21 checks it | FR-03-02, FR-08-03 |
| Namespaces | Upstream holds `base-*`, `backend-*`, `frontend-*` and its template directories; forks hold `stack-*`, `platform-*` and `<org>-*`. A duplicate ID fails MNF-01 and stops the resolver | FR-03-01 |
| `Fork-merge: ours` | Marks an upstream commit that removes what forks carry. The fork merges it with `-s ours`, keeping its own files | ADR-049 |
| Fork-owned files | `README.md`, `AGENTS.md`, `CLAUDE.md` and `CHANGELOG.md`; the fork keeps its side on every merge | ADR-050 |
| Fork-owned modules | `tests/fork_checks.py`, `tests/fork_dispositions.py` and `tools/fork_examples.py`, loaded when present. `fork_examples.py` may set `CHAIN_EXAMPLES_DOC`, default `docs/architecture/06-runtime-view.md` | ADR-050 |

## 8.7 Frozen surface

From 3.0.0 no release removes, renames or changes the meaning of an
element below before 4.0.0, except for a security fix. A minor may add
elements, and deprecate one by naming its replacement.

| Element | What is frozen | Source |
|---------|----------------|--------|
| Template paths | The file path of every shipped template | ADR-051 |
| Template IDs | The `id` of every manifest entry | ADR-051 |
| Section IDs | Every `[ID:]`, in the file that holds it, and the headings its section holds. A section does not move to another file, and a minor adds an ID only on new content, never in front of lines a shipped section holds. SYS-24 checks it against the newest 3.x tag | ADR-051 |
| Manifest schema | The fields the header comment of `templates/manifest.yaml` lists, and their meaning; a minor adds only optional fields | ADR-051 |
| Core-tier membership | The IDs under `core:`; a new template is reached by declaring it, never by joining the core | ADR-051 |
| Check exit codes | 0 passes, 1 fails, 3 does not apply | ADR-051 |
| Task kinds | The kinds under the manifest's `tasks:`, which a load directive names | ADR-058, proposed |
| Hooks | A shipped hook ID, its direct exit codes, its `not applicable` line and its violation codes | ADR-055 |
| Hook arguments | The name and default of each argument a consumer writes into its config, such as `--path`, `--forbid` and `--base`; a minor adds only arguments whose default keeps the hook's behaviour | ADR-051, applied to hooks |
| Fork entry points | The fork-owned module names (8.6), and the names upstream reads from them, `bind`, `CHECKS`, `TEMPLATE_DIRS`, `CORE_DIRS` and `QUALITY_GATES_EXEMPT_LAYERS` from `fork_checks.py`; `CHECKS` and `SKIP_BUDGET` from `fork_dispositions.py`; `SPEC_CHAIN_EXAMPLES` and `CHAIN_EXAMPLES_DOC` from `fork_examples.py`. The disposition words `tests/conformance` defines for a fork to import | ADR-051, applied to forks |
| Fork baseline | The `SAIT_UPSTREAM_REF` variable smoke reads | ADR-051, applied to forks |
| Resolver CLI | `tools/resolve_chain.py <id>` and its `--concat`, `--generate`, `--list`, `--roots` and `--check` flags | ADR-051, applied to forks |

These elements are not frozen.

| Element | Why | Source |
|---------|-----|--------|
| The wording inside a section | Prose is free while the section keeps its ID | ADR-051 |
| The declaration block | A target with no producer and no reader | ADR-053 |
| The fixture, `stack-fixture` and `platform-fixture` | Test input; no listing offers it and no project resolves it | - |
| The helpers `bind()` hands `fork_checks.py` | Every name in the smoke modules; a change to one is listed in the changelog | - |

## 8.8 Deprecation

From 3.0.0 a template is not removed inside a major (ADR-051). Its manifest
entry names the template that replaces it, and the release that marks it
lists it under `Deprecated` in the changelog.

```yaml
- id: base-old
  file: templates/core/old.md
  description: ...
  deprecated: base-new
```

The entry still resolves. SYS-22 fails a `deprecated` that names no entry,
or one that is itself deprecated. Removal waits for the next major.

A shipped hook that no template prescribes any more is deprecated the same
way. Its `name` in `.pre-commit-hooks.yaml` starts with `Deprecated:`, and
the changelog lists it under `Deprecated`. It keeps its frozen behaviour
(8.7) until the next major removes it.

## 8.9 Rule language and naming

A rule is a plain imperative, read as MUST or MUST NOT, or carries an RFC
2119 keyword where strength matters (`templates/core/docs.md`, "Rule
language"). A mechanically checkable rule names its command in a fence and
its pass condition beside it (FR-01-01, FR-07-01, ADR-031).

```text
templates/<concern>/<name>.md   # cross-cutting: core, security, infra, data
templates/frontend/<concern>.md # frontend layer
templates/backend/<concern>.md  # backend layer
templates/fixture/<name>.md     # test input
```

A fork names its own files.

## 8.10 Context cost

Every rule in a widely resolved file is read on every turn by every project
on that chain. A stack category's context-window tier moves only on
purpose, recorded in `tests/smoke/context-tiers.txt`, and SYS-16 checks it
(QG-02-02). A rule in context costs attention as well as tokens, so a
shorter file is better only when every rule it drops is one the agent did
not need, and the form of each rule matters more than its size (8.12).

The table shows what each root puts in context, as the emitter builds it.
The root file is read on every turn, and the skills load only when their
task starts. The root file's count includes its fact slots.

<!-- generated:spec-context-cost -->
| Root | Every turn, words | Skills | Skill words |
|------|-------------------|--------|-------------|
| `backend-api` | 5730 | 11 | 2714 |
| `backend-auth` | 7784 | 10 | 2094 |
| `backend-caching` | 5389 | 10 | 2094 |
| `backend-concurrency` | 5236 | 10 | 2094 |
| `backend-database` | 5196 | 11 | 2173 |
| `backend-edge` | 8117 | 10 | 2094 |
| `backend-errors` | 6635 | 10 | 2094 |
| `backend-features` | 5247 | 10 | 2094 |
| `backend-grpc` | 8896 | 11 | 2250 |
| `backend-http` | 5663 | 10 | 2094 |
| `backend-jobs` | 5169 | 10 | 2094 |
| `backend-messaging` | 5455 | 11 | 2188 |
| `backend-microservices` | 6852 | 11 | 2853 |
| `backend-monitoring` | 5528 | 10 | 2094 |
| `backend-observability` | 5275 | 10 | 2094 |
| `backend-webhooks` | 8637 | 11 | 2188 |
| `base-agents` | 4797 | 10 | 3189 |
| `base-cicd` | 5085 | 10 | 2214 |
| `base-config` | 5259 | 10 | 2124 |
| `base-containers` | 5138 | 10 | 2194 |
| `base-data-governance` | 5694 | 10 | 2094 |
| `base-data-migration` | 5367 | 11 | 2466 |
| `base-data-modeling` | 5206 | 10 | 2094 |
| `base-data-quality` | 5961 | 11 | 2143 |
| `base-deployment` | 5075 | 10 | 2153 |
| `base-devsecops` | 5383 | 10 | 2094 |
| `base-docs` | 4781 | 10 | 2094 |
| `base-embedded-checks` | 6035 | 11 | 4377 |
| `base-git` | 4781 | 10 | 2094 |
| `base-measurement` | 5508 | 10 | 2094 |
| `base-oop` | 5323 | 10 | 2094 |
| `base-quality` | 4781 | 10 | 2094 |
| `base-quality-gates` | 6014 | 11 | 4134 |
| `base-review` | 4781 | 10 | 2094 |
| `base-security` | 6312 | 10 | 2094 |
| `base-testing` | 4781 | 10 | 2094 |
| `frontend-content` | 5176 | 10 | 2094 |
| `frontend-quality` | 5201 | 10 | 2169 |
| `frontend-ux` | 5283 | 10 | 2094 |
<!-- /generated:spec-context-cost -->

## 8.11 Responsibility levels

Six levels own the decisions around a change, from why a product exists to
the change itself. Upstream is the shared engineering policy, level 4. A
rule belongs to the level that decides it. Preserving data in a migration
is shared policy, choosing the migration tool is a project convention, and
accepting ten minutes of downtime is a requirement. A finding goes to the
level whose decision it corrects, and may touch several, each with its own
approver. An agent may gather the evidence and propose a correction, and
the level's owner approves it.

| Level | Decides | Owner | A finding corrects | Source |
|-------|---------|-------|--------------------|--------|
| 1. Purpose and outcomes | Why the product exists and what success means | Business and product leadership | Product goals and success measures | Chapter 1 |
| 2. Requirements and acceptance | What must work, under which constraints | Product owner and team | Specification and acceptance criteria | Chapter 1, Team |
| 3. Architecture | System boundaries and the major design choices | Technical leadership | Architecture and decision records | Chapter 1, Team |
| 4. Shared engineering policy | The standards, safeguards and evidence every project needs | Upstream maintainer | A template and its checks | ADR-050 |
| 5. Project conventions | Stack, tools, commands and local policy | Fork or project maintainer | A fork template, configuration or context file | ADR-049 |
| 6. Task execution | Implementing, testing, reviewing and explaining a change | Agents and developers | Code and regression tests | Chapter 1 |

## 8.12 Template quality

A template is a list of rules an agent reads and applies on the next turn.
A good one states each rule once, briefly, as an instruction, and leaves
reasons and history to `docs/rationale/`, one file per template and one
heading per section ID. `tools/score_templates.py` measures that form on
prose only, leaving out fenced code, tables and section directives. Each
criterion scores 100 at its good value and 0 at its bad one, linearly
between, and a file's score is the weighted mean.

| Criterion | Metric | Good | Bad | Weight | Why it matters to an agent |
|-----------|--------|------|-----|--------|----------------------------|
| Atomic rules | Median words per bullet | ≤ 15 | ≥ 35 | 2 | A short rule is one signal; a long one carries several the agent must separate |
| No long rules | Share of bullets over 40 words | ≤ 2 % | ≥ 30 % | 2 | A rule that needs a paragraph is a rule plus its explanation |
| Rules, not essays | Share of prose words in paragraphs | ≤ 10 % | ≥ 35 % | 1.5 | Paragraphs read as context, not as instructions |
| Short lead-ins | Longest paragraph, words | ≤ 40 | ≥ 120 | 1 | A long lead-in pushes the rules it introduces out of view |
| Plain sentences | Mean words per sentence | ≤ 15 | ≥ 22 | 1 | Long sentences hide the condition a rule depends on |
| One statement per rule | Share of bullets with three or more sentences | ≤ 2 % | ≥ 20 % | 1.5 | The extra sentences are rationale, which belongs in prose docs |
| Instructions | Share of top-level bullets opening with an imperative or carrying an obligation word | ≥ 75 % | ≤ 40 % | 1 | A bullet that only describes leaves the agent to infer the rule |
| Verb first | Share of top-level bullets opening with a subject, such as a determiner first, an auxiliary second, or an unbracketed RFC key word within four words | 0 % | 100 % | 0.25 | "Handlers are thin" and "X MUST be" state a fact the agent must turn into an action |
| Whole wraps | Continuation lines holding only a dash or one word, with more of the rule after them | 0 | ≥ 4 | 0.25 | A wrap broken mid-sentence reads as two fragments |
| Decidable | Hedge words per 1,000 words, such as "appropriate", "where possible" and "usually" | ≤ 1 | ≥ 5 | 1 | A hedge lets two agents read the same rule two ways |
| Rules, not history | Dates, "measured in" and "seen during" per 1,000 words | 0 | ≥ 1 | 0.5 | An anecdote is evidence for a rule, not a rule |
| Retrievable sections | Prose lines in the longest section | ≤ 40 | ≥ 200 | 1 | A heading is a retrieval cue; a section too long to hold weakens it |

A failure severe enough that no average should hide it caps the score.

| Severe failure | Cap |
|----------------|-----|
| A ticket or decision-record number cited in template text | 50 |
| A single bullet over 150 words | 60 |

The bands are calibrated on the corpus, not set up front. "Good" sits near
the median of the templates outside `core/`, and "bad" near the corpus's
90th percentile. `--calibrate` prints the distributions, and the planted
cases of `--self-test` hold the scorer to its intent, so short imperative
rules score 85 or above and essay-like rules 40 or below.

`tests/baselines/template-quality.txt` records each template's score, and
CI runs `--check` as a ratchet (QG-04-02). It fails a template scoring
below its row, an upstream template scoring under 95 with or without a
row, a new template scoring under 70 with no row, and a row naming no
template. A change that improves a template re-records its row with
`--update`. A fork records its own templates in
`tests/baselines/fork-template-quality.txt`, so recording them never edits
the upstream file, and they answer to their own rows and the 70 floor.

The scores measure form, not usefulness or correctness. A short,
imperative, wrong rule scores well, and so does a rule shortened by
dropping the condition it applies under or its main exception. A rule is
shortened by splitting it, never by dropping either. The scores sit beside
review and the efficacy benchmark, not in place of them.
