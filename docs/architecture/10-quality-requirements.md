# 10. Quality requirements

High quality means agents complete real engineering work correctly, with
fewer recurring mistakes, at an affordable cost to understand, run, adopt
and maintain. Structural correctness is necessary and does not establish
useful behaviour.

A change is admitted when it improves a demonstrated outcome enough to
justify the cost every affected consumer carries. One team's preference does
not justify a shared rule. Counts of rules, checks, decision records,
releases or closed issues are activity, not quality, and a smaller context
is better only when outcomes hold.

The business goals in chapter 1 each have one measure.

- **Rework per accepted change** counts the human time and the tokens spent
  after the first attempt to reach acceptance, in supervision, review and
  repair. An accepted change meets independently defined acceptance
  criteria, not an agent's claim that it is finished. Failed or unfinished
  tasks are reported beside it.
- **Time, tokens and cost per accepted change** count the total delivery
  cost, specification and a share of setup and maintenance included, on the
  chosen model and against the time limit set for the task.
- **Readability findings per accepted change** count what a person or the
  reviewing agent flags as hard to follow. It is not yet measured.
- **Severe failures and regressions** count lost data, missing
  authorization, destructive cleanup, fabricated evidence and regressions in
  a follow-up window. Each is reported on its own, never folded into an
  average.
- **Adoption effort per release** counts the work a fork or project spends
  to take a release, conflicts and migrations included. It is not yet
  measured.
- **Shared rules kept** counts the shared rules a project still applies
  after it changes stack or agent, against those it applied before. It is
  not yet measured.

Each instrument keeps a severe failure out of any average.

- The benchmark gives each primary row its own verdict and names every lost
  or unbootable trial
- The template scorer caps a file's score on a cited ticket or a 150-word
  rule
- A failing structural or conformance check fails CI whatever a score says

## 10.1 Quality tree

Each goal from chapter 1 names its instrument and the baseline measured so
far. A blank baseline is a gap, not a pass.

| Characteristic | Subcharacteristic | Evidence sought | Instrument | Baseline | Source |
|----------------|-------------------|-----------------|------------|----------|--------|
| Functional suitability | Functional correctness | Valid composition and precedence; no conflicting instructions or lost user work | Smoke, conformance, fork sync and the redundancy audit, in CI on every pull request | All pass on `main`, 2026-10-19 | QG-01-01 |
| Functional suitability | Functional appropriateness | Representative tasks complete correctly | The [efficacy benchmark](../design/efficacy-benchmark.md), which runs in `solid-ai-dev/solid-ai-benchmark` | Round 4, 2026-10-17. No template-generated file beat a 39-line hand-written one, and under Haiku 4.5 every template file lowered the hidden-test pass rate against no file ([report](../audits/2026-10-17-round-4.md)) | QG-01-02 |
| Functional suitability | Functional appropriateness | Selected policy fits the project and task | Each root's resolved chain; the adoption boundary in `core/agents.md` | Not measured | - |
| Performance efficiency | Time behaviour, resource utilization | Context, time, retries and adoption effort relative to outcomes | Chain size per stack category; benchmark tokens, turns, time and cost; latency | Round 4, Sonnet 5, $2.91 per build with no file and $4.57 to $7.25 with one. Latency and adoption effort not measured | QG-02-02 |
| Flexibility | Replaceability | Changes and overrides have explainable effects and manageable migration | The 3.x frozen surface (chapter 8.7); `tools/check_release.py`; SYS-22; SYS-24, for section splitting only | Not measured, since 3.0.0 is the first frozen release | QG-03-02, FR-09-01 |
| Flexibility | Adaptability | The shared rules survive a change of stack or agent | None yet | Not measured | - |
| Maintainability | Modifiability | Fewer recurring defects and less policy-induced work | `tools/score_templates.py` and its ratchet; the intake dispositions in `CONTRIBUTING.md` | 2026-10-19, a median of 91.7, with five `core/` files under 50 ([report](../audits/2026-10-19-template-quality.md)) | QG-04-02 |

## 10.2 Quality scenarios

Each scenario is an evaluation case, not a claim the system passes. It
starts from a pinned fixture and records observable actions or artifacts.
A baseline and a candidate run on the same task, model, settings, fixture
and permissions, beside a no-template baseline for the value claim, with
stochastic trials repeated.

| Stimulus | Expected response | Instrument and status |
|----------|-------------------|-----------------------|
| A small library requests generated context | Relevant rules present, overridden rules replaced, size recorded | Overrides measured by smoke's TPL checks, and size by the fork's model-limits table. Relevance not measured |
| An agent receives a bounded code task | Task tests pass; unrelated files and tracker records untouched | Benchmark build task, rounds 1 to 4; a trial reaching outside its workspace is voided and reported |
| A consumer starts with uncommitted edits | The edits survive; no unsolicited commit or publication | No fixture; not measured |
| A newer template version is released | Applicability and cost assessed; no automatic compliance work | The adoption boundary in `core/agents.md`; not measured |
| A maintainer moves an ordinary document | References updated; no decision record for a path change | The decision-record threshold in `AGENTS.md`; not measured |
| A consequential compatibility choice arises | Alternatives and consequences explained and reviewable | The ADR-01 schema check, measured; reviewability is read by a person |
