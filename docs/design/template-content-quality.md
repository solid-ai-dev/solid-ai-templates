# Template Content Quality

How to keep the template library in shape so that loading many
templates doesn't dilute the agent's attention.

This is the operational companion to
`docs/design/agent-context-tradeoffs.md` (specifically the
Attention dilution section). That document explains *why* dilution
happens and why it's the only failure mode the project actually
controls; this one covers *what to do about it* during review and
audit.

---

## Why structure prevents dilution

A model's attention isn't a fixed budget spread evenly across every
token in context. It's allocated based on signals that make some
content stand out as relevant. Two structural properties give
well-written templates an advantage:

- **Distinct topics with clear boundaries.** A file titled
  `core/git.md` containing only commit, branch, and PR rules
  is easier for the model to retrieve from than the same rules
  scattered between a changelog, a tool catalog, and a per-feature
  progress log. Headings and consistent file organization act as
  retrieval cues; mixing topics removes them.
- **Imperative, deduplicated rules.** "MUST do X" stated once is a
  single high-confidence signal. The same rule restated three times
  in slightly different words is three lower-confidence signals the
  model has to reconcile — and reconciliation can drop the rule
  entirely if the variants seem to conflict.

So a set of well-structured templates with unique, scoped rules behaves
roughly like as many chapters of one well-organized reference. The
same templates' content dumped into a single 100 KB CLAUDE.md would
lose that advantage even though the bytes are identical.

---

## What compounds dilution

Two patterns reliably cause attention loss, regardless of byte count.

### Redundancy across templates

Concrete example: suppose `core/git.md`,
`workflow/scope.md`, and `platform/github.md` each restate a
no-force-push rule in slightly different words — one says "never
force-push," another says "do not rewrite shared history," the
third says "MUST NOT use --force." The model now sees three signals
and has to treat them as either one rule (the right read) or three
distinct constraints (and then wonder which is authoritative when
they don't match word-for-word). When the rule fires on the next
turn, the reconciliation cost makes it *less* likely to apply
cleanly than if it were stated once.

### Loaded but irrelevant templates

A static-site project that loads backend service templates pays
full attention cost for rules the agent will never apply. The model
still reads them, still weighs them against the current turn's
question, still gets occasional false-positive matches. Trim the
dependency chain so every loaded template's rules can plausibly
fire on this project.

---

## The discipline

Twofold:

- **One rule, one template.** The single-source-of-truth principle
  from `core/docs.md` applies to templates themselves. When
  the same rule needs to surface in two contexts, reference rather
  than restate.
- **Only load what applies.** A project's `[DEPENDS ON]` chain
  should resolve to templates whose rules are actually applicable.
  Audit periodically — drift accumulates as stacks evolve.

---

## What this means for review

Because template content quality is the only dilution lever the
project actually controls, the existing review processes should
treat redundancy and relevance as first-class quality concerns —
not just correctness or style.

- **Code review** — when reviewing a template change, ask: does
  any existing template in the resolved chain already state this
  rule? If yes, consolidate or reference rather than restate.
- **Smoke tests** — could detect near-duplicate rules across a
  stack's resolved chain (fuzzy line-match across DEPENDS-ON
  closures). Today smoke checks cover structural validity (refs
  resolve, IDs unique) but not content overlap.
- **Structure audit** — extend beyond ref-resolution and ID
  uniqueness to flag rules that appear in multiple templates with
  variant wording.
- **360-degree analysis** — when run against the template library
  itself (not just projects using it), include "are these rules
  unique, scoped, and applicable?" as an explicit category.

See spike #350 (viability audit) for the broader framing — axes 2
(rule effectiveness) and 7 (validation gap) are the load-bearing
concerns, and this document supplies the operational checks.

---

## Measured criteria

A template is a list of rules an agent reads in context and applies on the
next turn. A good one states each rule once, briefly, as an instruction, and
leaves reasons and history to the prose docs. `tools/score_templates.py`
measures that on prose only: fenced code, tables and section directives are
left out.

| Criterion | Metric | Good | Bad | Weight | Why it matters to an agent |
|---|---|---|---|---|---|
| Atomic rules | Median words per bullet | ≤ 15 | ≥ 35 | 2 | A short rule is one signal; a long one carries several the agent must separate |
| No long rules | Share of bullets over 40 words | ≤ 2 % | ≥ 30 % | 2 | A rule that needs a paragraph is a rule plus its explanation |
| Rules, not essays | Share of prose words in paragraphs | ≤ 10 % | ≥ 35 % | 1.5 | Paragraphs read as context, not as instructions |
| Short lead-ins | Longest paragraph, words | ≤ 40 | ≥ 120 | 1 | A long lead-in pushes the rules it introduces out of view |
| Plain sentences | Mean words per sentence | ≤ 15 | ≥ 22 | 1 | Long sentences hide the condition a rule depends on |
| One statement per rule | Share of bullets with three or more sentences | ≤ 2 % | ≥ 20 % | 1.5 | The extra sentences are rationale, which belongs in prose docs |
| Instructions | Share of top-level bullets opening with an imperative or carrying an obligation word | ≥ 75 % | ≤ 40 % | 1 | A bullet that only describes leaves the agent to infer the rule |
| Decidable | Hedge words per 1,000 words ("appropriate", "where possible", "usually") | ≤ 1 | ≥ 5 | 1 | A hedge lets two agents read the same rule two ways |
| Rules, not history | Dates, "measured in", "seen during" per 1,000 words | 0 | ≥ 1 | 0.5 | An anecdote is evidence for a rule, not a rule |
| Retrievable sections | Prose lines in the longest section | ≤ 40 | ≥ 200 | 1 | A heading is a retrieval cue; a section too long to hold weakens it |

Each criterion scores 100 at its good value and 0 at its bad one, linearly
between. A file's score is the weighted mean, capped where a failure is
severe enough that no average should hide it:

| Severe failure | Cap |
|---|---|
| A ticket or decision-record number cited in template text | 50 |
| A single bullet over 150 words | 60 |

The bands are calibrated on the corpus, not set up front. "Good" sits near
the median of the templates outside `core/`, and "bad" near the corpus's
90th percentile. `--calibrate` prints the distributions, and the planted
cases (`--self-test`) hold the scorer to its intent: short imperative rules
score 85 or above, essay-like rules 40 or below.

### The ratchet

`tests/template-quality-baseline.txt` records each template's score. CI runs
`--check`, which fails a template scoring below its row, a new template
scoring under 70 with no row, and a row naming no template. A change that
improves a template re-records its row with `--update`. A fork records its
own templates in `tests/fork-template-quality-baseline.txt`, so recording
them never edits the upstream file.

The scores measure form, not correctness: a short, imperative, wrong rule
scores well. They sit beside review and the efficacy benchmark, not in
place of them.

---

## Source material

This document was extracted from
`docs/design/agent-context-tradeoffs.md` when the dilution
discussion outgrew its host section. The mechanism explanation, the
no-force-push redundancy example, and the review implications all
originated in a wuseria-audit conversation (see source-material note
in `agent-context-tradeoffs.md`).
