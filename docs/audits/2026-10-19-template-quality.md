# Template quality review — 2026-10-19

Every template scored against the criteria in
`docs/design/template-content-quality.md`, "Measured criteria", by
`py tools/template_quality.py` at the commit that adds it (#2019). The six
lowest were then read by hand to check the scores track judgement.

## Summary

- Median score 91.7 of 100; five templates score under 50, and all five are
  in `core/`.
- The lowest-scoring files are the ones every project reads: the core tier
  (`quality`, `git`, `docs`, `testing`, `review`) and `quality-gates`, which
  nearly every stack resolves.
- Their failure is one shape: a bullet states a rule, then argues for it,
  recounts how it was found, and qualifies it, so the rule is a sentence
  inside a paragraph.
- The four lowest carry 30,768 prose words between them, against 1,000 to
  3,000 for a typical layer file.
- Outside `core/`, form is good. The weak spots are a few hedge-heavy
  files (`frontend/static-site`, `backend/database`) and principle-style
  bullets that describe rather than instruct (`frontend/ux`).

## Scores

Lowest first. The weakest criteria are those scoring under 60, with their
score (`rule` words per rule, `long` share of long rules, `para` prose in
paragraphs, `maxP` longest paragraph, `sent` sentence length, `multi`
multi-sentence rules, `dir` instructions, `hedge`, `narr` history, `sect`
section size).

| Template | Score | Prose words | Median words / rule | Longest rule | Weakest criteria | Severe |
|---|---|---|---|---|---|---|
| `core/quality-gates.md` | 19.2 | 8,697 | 45 | 160 | rule 0, long 0 | rule over 150 words |
| `core/quality.md` | 23.8 | 10,895 | 36 | 170 | rule 0, long 0 | rule over 150 words |
| `core/git.md` | 27.1 | 2,777 | 30 | 133 | long 0, maxP 0 |  |
| `core/testing.md` | 30.6 | 8,399 | 30 | 130 | long 0, sent 0 |  |
| `core/docs.md` | 40.9 | 3,112 | 28 | 199 | maxP 0, long 14 | rule over 150 words |
| `core/review.md` | 54.7 | 3,070 | 22 | 70 | para 0, maxP 0 |  |
| `core/config.md` | 60.0 | 1,099 | 13 | 162 | dir 53 | rule over 150 words |
| `core/agents.md` | 69.1 | 1,920 | 15 | 81 | para 0, dir 21 |  |
| `security/devsecops.md` | 79.7 | 1,252 | 16 | 89 | long 36, sent 59 |  |
| `core/oop.md` | 83.2 | 599 | 18 | 53 | sent 47, dir 52 |  |
| `data/data-quality.md` | 83.3 | 1,185 | 14 | 51 | maxP 26, para 50 |  |
| `frontend/static-site.md` | 84.0 | 328 | 11 | 26 | dir 0, hedge 0 |  |
| `frontend/content.md` | 85.8 | 532 | 19.5 | 34 | narr 0 |  |
| `infra/cicd.md` | 86.8 | 666 | 10 | 82 | hedge 50, dir 56 |  |
| `backend/webhooks.md` | 86.9 | 263 | 19 | 27 | sent 46, para 53 |  |
| `infra/containers.md` | 86.9 | 820 | 14.5 | 93 | sent 48 |  |
| `frontend/quality.md` | 88.0 | 504 | 17.5 | 35 | hedge 26, dir 49 |  |
| `backend/edge.md` | 89.7 | 493 | 17 | 32 | — |  |
| `backend/features.md` | 90.9 | 442 | 19 | 28 | dir 54 |  |
| `backend/concurrency.md` | 91.7 | 426 | 17 | 67 | — |  |
| `backend/errors.md` | 91.7 | 398 | 21 | 29 | sent 56 |  |
| `backend/database.md` | 92.0 | 396 | 12 | 25 | hedge 0 |  |
| `backend/microservices.md` | 93.5 | 703 | 18 | 29 | — |  |
| `frontend/ux.md` | 93.5 | 660 | 11 | 40 | dir 19 |  |
| `backend/api.md` | 94.9 | 605 | 10 | 63 | dir 39 |  |
| `infra/deployment.md` | 95.4 | 962 | 14 | 26 | dir 49 |  |
| `backend/http.md` | 96.0 | 519 | 10 | 63 | — |  |
| `backend/grpc.md` | 96.1 | 485 | 14 | 27 | dir 52 |  |
| `security/security.md` | 96.2 | 1,334 | 14 | 76 | — |  |
| `backend/jobs.md` | 97.2 | 415 | 14 | 21 | — |  |
| `backend/messaging.md` | 97.5 | 649 | 17 | 31 | — |  |
| `backend/observability.md` | 97.7 | 502 | 12 | 32 | — |  |
| `backend/quality.md` | 98.3 | 448 | 13 | 25 | — |  |
| `backend/auth.md` | 98.4 | 450 | 15 | 26 | — |  |
| `backend/monitoring.md` | 98.5 | 277 | 13 | 22 | — |  |
| `data/data-migration.md` | 99.8 | 351 | 13 | 26 | — |  |
| `backend/caching.md` | 100.0 | 434 | 13 | 23 | — |  |
| `data/data-governance.md` | 100.0 | 355 | 11 | 22 | — |  |
| `data/data-modeling.md` | 100.0 | 348 | 12 | 20 | — |  |

## The six lowest, read by hand

| Template | Score | What the reading found | Example |
|---|---|---|---|
| `core/quality-gates.md` | 19.2 | Each rule carries its derivation: why a control can mislead, what the failure looks like, which artifact it reads. The rule is the first clause of a 100-word bullet | Line 984: "The step that plants a break MUST itself be verified", then 150 words on why |
| `core/quality.md` | 23.8 | Check specifications are written as prose bullets: scope, exemptions, implementation hints and edge cases in one run-on item | Line 1269: the comment-layout check, 170 words in one bullet |
| `core/git.md` | 27.1 | Pull-request rules argue from CI internals and past incidents; one section ("Off-limits paths") is 685 words of prose around one check | Line 23: "A check reading the change under review is confirmed where it ships", 133 words |
| `core/testing.md` | 30.6 | Sections named for a lesson ("A remedy naming another check is a claim about that check") hold an essay on it; 34 sections, many single-rule | Line 215: the host-state rule, 130 words with "This is a distinct class… and more severe" |
| `core/docs.md` | 40.9 | The writing-style and generated-files rules restate the rule with the counter-examples a detector needs | Line 283: the generated-figures rule, 199 words |
| `core/review.md` | 54.7 | Checklists are sound; the issue-verification section is three paragraphs of narrative before any rule | Line 125: "An issue is written against the tree as it stood on the filing date…" |

The scores agree with the reading in every case: the files score low for
the reasons a reader finds them hard. None of the six is wrong; each is
correct reasoning in the wrong form for an agent's context.

## Where the scorer and judgement part

| Case | Score says | Reading says | Disposition |
|---|---|---|---|
| Checklist items (`- [ ] …`) | Not instructions | An instruction to check | Fixed before recording: a checklist item counts as one |
| `frontend/ux.md` principle bullets ("Consistency — same patterns throughout") | Low on instructions | Terse but vague | Kept: the criterion is right |
| `frontend/content.md` history | An example date in a JSON-LD rule read as history | An example | Accepted: weight 0.5; one false positive |
| A short, wrong rule | Scores well | Wrong | Out of scope: the scorer measures form, not correctness |

## Rewrite order (3.x)

Rewrites keep every section ID, so each is compatible under the 3.x freeze.
Each moves a rule's reasoning to the prose docs and leaves the rule:

1. `core/quality.md` and `core/quality-gates.md`: the largest, and both in
   nearly every chain
2. `core/testing.md` and `core/git.md`: core tier, read on every turn
3. `core/docs.md` and `core/review.md`
4. `core/config.md` (one 162-word rule caps it) and `core/agents.md`

The ratchet holds every file at today's score, so a rewrite can only raise
it. Re-record with `--update` in the rewrite's pull request.
