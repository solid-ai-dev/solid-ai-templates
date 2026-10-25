# Base — Measurement

[ID: base-measurement]
[DEPENDS ON: templates/core/quality.md]

For a project that computes, calibrates or extracts values: an iterative
numerical routine, a pipeline scored against reference data, an extractor
checked against an external source. Each fails by producing a plausible
answer rather than an error.

## Expensive computations

[ID: quality-expensive-compute]

### Convergence

- Wrap a routine whose convergence flag the caller may ignore in one helper
  that checks the flag (MUST)
- Raise an error naming what did not converge when no retry converges
- Fire any retry or stabilisation only on non-convergence, so a
  converging path is untouched
- Exercise the non-convergence path with a stub that scripts convergence
  per attempt

### Approximations

- Default an output-changing speed knob, such as a lower-rank
  approximation or a coarser grid, to off (MUST)
- Carry it as a per-run field beside the run's other parameters, so the
  run reproduces itself

## Calibration

[ID: quality-calibration]

### Ground truth

- Confirm that committed data used as ground truth was not produced by an
  earlier version of the same pipeline with known or suspected bugs; if it
  was, it is not ground truth
- Build the calibration set from raw artifacts, recording the verified
  value beside each entry
- Prefer a small hand-built set from raw artifacts to a large one carried
  over from a suspect pipeline
- Sweep, in the change that corrects a reference value, every comment,
  guard and threshold whose reasoning cites the old value
- Re-verify each one the sweep finds, or record it as open work

### Honest absence

- Keep an honest absence (null, empty) where the source carries no
  value; never recover a wrong value in its place
- Re-mark a prior expected value at that point as extrapolation, in the
  same change (MUST)
- Distinguish in logs and notes an absence because extraction failed from
  one because the source has no value

### Derived quantities

- Report a derived quantity only where its defining condition holds: a
  non-zero denominator, a minimum sample, a non-degenerate input
- Leave the cell empty where the condition fails; never zero, a
  placeholder or the out-of-domain value
- Check the condition where the value is emitted

### Visible artifacts

- Set the acceptance bar of a user-facing artifact by its strictest
  visible consumer
- Never loosen that bar for a coarser downstream consumer or for
  throughput; blank an ambiguous cell instead

### Thresholds

- Tune the threshold once the measurement is sound; change the
  measurement only when neither step resolves the disagreement
- Treat a threshold never validated against data as a guess

### Reference provenance

- Record on each reference entry who produced it: an agent, a person or
  an external source (MUST)
- Record on each entry whether a person reviewed it (MUST)
- Mark a value an agent produced as unverified until a person reviews it
  (MUST)
- Report verified coverage beside every metric computed against the set,
  such as `verified: 12/40` (MUST)
- Leave synthetic test inputs out of scope; the rule covers reference
  outputs

### Diagnosis

- Probe whether a calibrated or reasoned parameter is the actual
  constraint before changing it
- Trace the value where it is computed, reading real intermediates from a
  real sample

### Detector cost

- Evaluate a heuristic that gates an expensive fallback on what a wrong
  verdict destroys, not only on its false-positive rate (MUST)
- Ask whether a positive verdict discards or holds the cheap result, and
  what the system returns when the fallback cannot run
- Prefer preserving the cheap result, so an unavailable fallback degrades
  to a result plus a warning

### Evidence

- Count as evidence for a rule only the cases captured independently of
  the rule

### Calibration aids

- Render only the reference data and the reading guides in an aid a person
  verifies against (MUST)
- Put the candidate output in a separate, distinctly named artifact,
  opened after the reading is captured
- Leave comparison views opened after the reading out of scope
- Never count a value a person accepted from a shown prediction as an
  independent reading

## Source silence

[ID: measurement-source-silence]

- Return a field from an extractor only when the source states it (MUST)
- Compare a field only when both the stored and the source side carry it;
  source silence skips the comparison (MUST)
- Keep stored-default conventions (`absent = false`, `null = unknown`)
  intact
