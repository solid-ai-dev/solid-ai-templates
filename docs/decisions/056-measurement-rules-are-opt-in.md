---
id: "056"
status: Accepted
date: 2026-10-20
category: composition
supersedes: []
superseded_by: []
---

# ADR-056: Measurement rules are opt-in

## Context

`base-quality` is in the core tier, so every chain loads it. It carried
rules that hold only for projects that compute, calibrate or extract values.

| Force | What it shows |
| ----- | ------------- |
| Reach | Measured on `main` on 2026-10-20: the expensive-computation, calibration and source-silence rules were about 2,000 of the 4,805 words in `core/quality.md` |
| Fit | Convergence ladders, memory budgets, reference-set provenance and source silence apply to numerical routines, calibrated pipelines and extractors; a web service or CLI inherits them unused |
| Cost | A rule a project cannot apply still costs context in every chain and reads as policy |
| The freeze | From 3.0.0 the core tier and section IDs are frozen until 4.0.0, so moving sections out of core is cheapest before the tag |

## Decision

The expensive-computation, calibration and source-silence rules move out of
`base-quality` into a new opt-in template, `base-measurement`, that a
project declares through `Extras`.

## Rationale

- A project that computes or calibrates takes the rules by declaring one
  template; every other chain stops carrying them.
- Moving sections keeps their IDs, so a template extending or overriding one
  names the same ID in its new file.
- Doing it before 3.0.0 leaves the frozen core tier holding only rules every
  project needs.

## Design

1. **`base-measurement`**: `templates/core/measurement.md`, depending on
   `base-quality`, outside the core tier
2. **IDs**: `quality-expensive-compute` and `quality-calibration` move with
   their sections; the source-silence rules gain `measurement-source-silence`
3. **`base-quality`** keeps the check-trust rules under
   `quality-cross-validation`: tool trust, self-match, verdicts and readings
4. **Reach**: a project declares `base-measurement` in `Extras`; no stack's
   `depends_on` needs to name it

## Alternatives considered

| Alternative | Why not |
| ----------- | ------- |
| Keep the rules in core, trimmed | Every chain still carries numerical and calibration rules it cannot apply |
| Fold them into `base-data-quality` | That template governs data at rest; these govern computation and measurement, and a numerical project has no data-quality layer to reach them through |
| Drop them | They encode failures that recur in pipelines, and a project that needs them has nowhere else to find them |

## Consequences

| Area | Change |
| ---- | ------ |
| Chains | Every chain loses about 2,000 words of rules most projects do not apply |
| Manifest | Adds `base-measurement` outside the core tier |
| Projects | A project that relied on these rules adds `base-measurement` to `Extras` |
| Migration guide | Lists the move |

## Compatibility

No section ID is renamed or removed; two move to a new file. A template
extending or overriding a moved section resolves it only in a chain that
declares `base-measurement`, so such a template adds it to its
`depends_on`. The change ships in 3.0.0, before the freeze, and the
CHANGELOG lists it under `Changed`.

## Security

None.

## Related

- ADR-054: the earlier split that moved sections to a layer a project takes
  on its own.
- ADR-051: the frozen surface the core tier joins at 3.0.0.
