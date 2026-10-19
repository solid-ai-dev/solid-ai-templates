# 10. Quality requirements

High quality means agents complete real engineering work correctly, with
fewer recurring mistakes, at an affordable cost to understand, run, adopt
and maintain. Structural correctness is necessary and does not establish
useful behaviour.

## 10.1 Quality tree

Each goal from chapter 1 names its instrument and the baseline measured so
far. A blank baseline is a gap, not a pass.

| Quality | Evidence sought | Instrument | Baseline |
|---------|-----------------|------------|----------|
| Correctness | Valid composition and precedence; no conflicting instructions or lost user work | Smoke, conformance, fork sync and the redundancy audit, in CI on every pull request | All pass on `main`, 2026-10-19 |
| Effectiveness | Representative tasks complete correctly | The [efficacy benchmark](../design/efficacy-benchmark.md) (#1184); its harness runs in the Imbra fork | Round 4, 2026-10-17: no template-generated file beat a 39-line hand-written one; under Haiku 4.5 every template file lowered the hidden-test pass rate against no file ([report](../audits/2026-10-17-round-4.md)) |
| Relevance | Selected policy fits the project and task | Each root's resolved chain; the adoption boundary in `core/agents.md` | Not measured |
| Efficiency | Context, time, retries and adoption effort relative to outcomes | Chain size per stack category; benchmark tokens, turns, time and cost; latency (#368) | Round 4, Sonnet 5: $2.91 per build with no file, $4.57 to $7.25 with one; latency and adoption effort not measured |
| Predictability | Changes and overrides have explainable effects and manageable migration | The 3.x frozen surface (ADR-051, ADR-053); `tools/release_check.py`; SYS-22; the freeze check (#1992) | Not measured: 3.0.0 is the first frozen release |
| Maintainability | Fewer recurring defects and less policy-induced work | `tools/template_quality.py` and its ratchet; the intake dispositions in `CONTRIBUTING.md` | 2026-10-19: median 91.7, five `core/` files under 50 ([report](../audits/2026-10-19-template-quality.md)) |

A severe failure is reported on its own, never folded into an average:

- The benchmark gives each primary row its own verdict and names every lost
  or unbootable trial
- The template scorer caps a file's score on a cited ticket or a 150-word
  rule
- A failing structural or conformance check fails CI whatever a score says

Counts of rules, checks, decision records, releases or closed issues are
activity, not quality. A smaller context is better only when outcomes hold.

## 10.2 Quality scenarios

Each starts from a pinned fixture and records observable actions or
artifacts. They are evaluation cases, not claims the system passes.

| Stimulus | Expected response | Instrument and status |
|----------|-------------------|-----------------------|
| A small library requests generated context | Relevant rules present, overridden rules replaced, size recorded | Overrides: smoke's TPL checks, measured. Size: the fork's model-limits table, measured. Relevance: not measured |
| An agent receives a bounded code task | Task tests pass; unrelated files and tracker records untouched | Benchmark build task, rounds 1 to 4; a trial reaching outside its workspace is voided and reported |
| A consumer starts with uncommitted edits | The edits survive; no unsolicited commit or publication | No fixture; not measured |
| A newer template version is released | Applicability and cost assessed; no automatic compliance work | The adoption boundary in `core/agents.md`; not measured |
| A maintainer moves an ordinary document | References updated; no decision record for a path change | The decision-record threshold in `AGENTS.md`; not measured |
| A consequential compatibility choice arises | Alternatives and consequences explained and reviewable | The ADR-01 schema check, measured; reviewability is read by a person |

Compare baseline and candidate on the same task, model, settings, fixture
and permissions, include a no-template baseline when testing the value
claim, and repeat stochastic trials.
