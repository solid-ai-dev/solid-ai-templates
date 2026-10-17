---
id: "052"
status: Accepted
date: 2026-10-17
category: composition
supersedes: []
superseded_by: []
---

# ADR-052: Hybrid is the delivery floor

## Context

A generated context file delivers each rule one of three ways: copied in
(inline), named as a file to read (reference), or both, with the rules that
matter copied in and the rest named (hybrid). The interview offers all
three, and `agents.md` recommends hybrid without ruling reference out.

| Force | What it shows |
| ----- | ------------- |
| No loading mechanism | A referenced template is not loaded at startup, on relevance, or by any cue. It is read only when the agent decides to open it (#712) |
| A consumer it failed | Under a reference-model file, a project's agent never opened the deferred templates across a session of git, testing and review work. A type-check gate that lived only there was missed and CI went red, and the defer list itself drifted unnoticed (#712) |
| Adherence | In round 3 hybrid adhered to the project's conventions best of every arm: +21.6 pp against no file, where the short inline file read +11.1 pp (#1893) |
| Security under a thin spec | In round 4, with a spec that states the contract and not the defences, hybrid scored highest of every arm on the judge's security and data-protection rows (`docs/audits/2026-10-17-round-4.md`). Rescored with the secret key the spec had omitted, two of its three trials read 0.82 and 1.00 on the security probes; the third was not measured (`rounds/2026-10-16-thin-sensitivity/score-py` in `braboj/tariff-runs`) |
| A cost of length | Under a weaker model in round 4, every template file but the hand-written one lowered task success against no file |
| A gap in the evidence | No round has run a reference-only arm, so the benchmark has not compared reference with hybrid directly |

## Decision

A generated context file delivers rules inline or hybrid, never by reference
alone: a rule whose breaking is silent and that no tool enforces is inlined,
and any other rule may stay a reference.

## Rationale

- A reference has no loading mechanism, so a rule that exists only as a
  reference is a rule the agent may never read; the consumer failure shows
  the cost lands where nothing catches it.
- Placement by damage and enforcement keeps every rule an agent must not miss
  in context, while a rule whose breaking shows itself, or that a test,
  linter or CI step checks, can stay outside it and keep the file short.
- Hybrid is the arm the benchmark reads best on adherence and on security, so
  making it the floor moves generation towards the measured result rather
  than away from it.
- The direct comparison is missing, so the record names the round that
  supplies it and what result would reopen it.

## Design

![How one rule is placed: if breaking it is silent and no test, linter or CI step enforces it, it is inlined; if it fails visibly or a tool enforces it, it may be referenced. Inline and hybrid remain; pure reference is deprecated](../diagrams/delivery-model.png)

1. **The floor** — Generation MUST NOT produce a file that delivers its
   rules by reference alone. Inline and hybrid remain.
2. **Inline the silent, unenforced rules** — A rule MUST be inlined when its
   breaking is silent, showing no error to the agent or the user, and no
   test, linter or CI step enforces it.
3. **Reference the rest** — A rule whose breaking fails visibly, or that a
   test, linter or CI step enforces, MAY be referenced instead of inlined.
4. **Where the rubric lives** — `agents.md` states the rubric, and the
   interview applies it; neither offers the reference model.
5. **Length is a cost, not a cap** — Inlining SHOULD stop at the rules rule 2
   requires. This record sets no size limit.

| Breaking the rule... | Enforced by a tool | Not enforced by a tool |
| -------------------- | ------------------ | ---------------------- |
| fails visibly | MAY reference | MAY reference |
| is silent | MAY reference | MUST inline |

## Alternatives considered

| Alternative | Why not |
| ----------- | ------- |
| Keep three models and recommend hybrid | Reference stays on offer, and the consumer failure is what it produces |
| Inline everything | The weaker-model result shows that length costs; a project vendoring the templates duplicates them |
| Allow reference delivered as a skill | A skill is loaded on demand from its description, which a plain reference is not, but no round has tested one; it is left to a later record |
| Wait for the reference arm before deciding | The missing mechanism is known, and generating reference files meanwhile ships the failure it causes |

## Consequences

| Consequence | Where |
| ----------- | ----- |
| `agents.md` "Choosing a model" states the rubric and drops reference | #712 |
| The interview stops offering the reference model | #712 |
| Skills as a delivery layer are reconsidered against this floor | #414 |
| Round 5 runs a reference-only arm beside hybrid. If it is no worse on adherence and on the judge's security and data-protection rows, this record is reopened | #1957 |
| Whether inlined length needs a bound for weaker models stays open until more than one project and K = 3 measure it | — |

## Compatibility

A project whose context file uses the reference model keeps working: nothing
it names is removed. Its next regeneration produces a hybrid file. The
reference model is listed under `Deprecated` in the CHANGELOG with hybrid as
its replacement, and is removed from the interview and `agents.md` in the
release that implements this record.

## Security

Protects: a security rule whose breaking is silent, such as output escaping,
a CSRF token, or a secret kept out of logs, is always in the agent's context,
where a reference-only file could leave it unread.
