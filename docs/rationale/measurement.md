# Rationale: measurement

Why the rules in `templates/core/measurement.md` say what they say. The
template states each rule as one instruction; the reasoning is here, one
heading per section ID.

## quality-expensive-compute

An unconverged result handed back as valid feeds a wrong number straight
downstream, and nothing errors. Firing the escalation only on failure keeps
the path that already converges byte-identical. A speed knob that shifts the
numbers, left on by default, silently perturbs the canonical output.

A library's fixed memory default is not the box the job runs on; an
estimated intermediate that spills or refuses gives a diagnosable error
where an OOM gives a crash. A tmpfs scratch path is memory under another
name.

Discarding the reusable state of a paid-for computation forces a full
re-run for the next question about the same input. A wrapper or proxy
around the engine can swallow the checkpoint parameter silently, which is
why the round-trip is tested through it.

## quality-calibration

Calibration is silently invalidated three ways: by suspect ground truth, by
a threshold tuned to mask a broken measurement, and by reference values
produced by the same actor that runs the tool. A value a calibrated pipeline
cannot justify is worse than a gap.

Calibrating against data an earlier, buggy version of the pipeline produced
bakes its bugs into the new gate. When the reference set flips to verified
values, reasoning that cites the old values keeps steering the code long
after the data is corrected; the sweep is one grep at a well-defined moment.

An absence because extraction failed is a defect; an absence because the
source has no value is the correct answer. Conflating them sends a
maintainer to fix a correct absence. A derived quantity computed outside its
domain is indistinguishable from a measurement and pollutes every downstream
aggregate, and the consumer cannot recover the condition from the value, so
the check sits at emission.

Coarsening the acceptance metric to a bucketed score, or dropping a label
only the visible artifact reads, is right for the score and corrupts the
table a user looks at.

The threshold is the cheaper thing to change, but only once the measurement
is sound; tuning an unvalidated threshold on first disagreement hides the
original guess. The order applies wherever measurements meet thresholds: CI
gates, performance budgets, decision boundaries, agreement scores.

Unverified reference values an agent produced can dominate a metric
silently; the coverage caveat keeps them visible. Changing a calibrated
parameter on "this might help" burns time and risks regressing unrelated
calibrated anchors.

A false-positive rate says how often a verdict is wrong and nothing about
what a wrong verdict destroys. Where the cheap tier returns a sentinel
instead of its body, the result is destroyed when the heuristic fires, and
the fallback's availability becomes part of the heuristic's correctness. An
optional dependency absent from a default install is the common deployment,
so "nothing" is a data-loss failure mode. No tuning finds this: it is a
property of the control flow.

A rule that survives every case its own author wrote is fitted to that set,
not measured against it. "The evidence does not exist yet" reads as a
non-answer unless stated as the deliverable.

Showing the candidate output beside a reading task biases the reading toward
the candidate and turns calibration into a self-confirming loop. Assisted
annotation, where a person corrects predictions they are shown, is a fair
way to build ground truth at volume, but its accepted values carry the same
bias, so they never stand in for an independent reading of that predictor.

## measurement-source-silence

A stored default such as `absent boolean = false` and source silence are not
the same thing; treating them as equal floods the report with false
mismatches that bury real errors. The stored-default convention and the
verification semantics pull in opposite directions, and the naive
implementation looks correct until it meets real data.

## Citing the software

A repository URL or project domain can move, lapse or be rebranded, and
every citation pointing at it rots. A persistent identifier resolves to an
archived, immutable snapshot, so the domain stays free to change.
