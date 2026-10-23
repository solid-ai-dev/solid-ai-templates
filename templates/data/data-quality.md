# Base — Data Quality
[ID: base-data-quality]
[DEPENDS ON: templates/data/data-modeling.md]

Rules for projects where content or data accuracy matters as much as
code quality. Applies to catalogues, reference datasets, published
content, and any project that declares data as a first-class concern.

## Data sourcing
[ID: data-quality-sourcing]

- Every data point MUST trace to a named source (URL, publication,
  manufacturer spec sheet)
- Record the source alongside the data — not in a separate document
- Prefer primary sources (manufacturer, official docs) over aggregators
- When multiple sources conflict, document the conflict and the chosen
  value with rationale
- Never fabricate or estimate values without marking them as estimates

## Completeness tracking
[ID: data-quality-completeness]

- Define a completeness score for each entry: fields populated / total
  fields (e.g. `14/14`)
- Track completeness at the entry level, not just the collection level
- Incomplete entries MUST be queryable — add a `completeness` or
  `dataStatus` field
- Set a minimum completeness threshold for publishing (e.g. 80%)
- Entries below the threshold MAY exist in the database but MUST NOT
  appear in user-facing views

## Freshness
[ID: data-quality-freshness]

- Record when each entry was last verified: `lastVerified` date field
- Define a freshness window per collection (e.g. prices: 30 days,
  specs: 12 months)
- Entries beyond their freshness window SHOULD be flagged for review
- Record the capture date beside every time-sensitive value, such as a
  price; never show one without it (MUST)
- Discontinued or unavailable items MUST be marked, not deleted

## Exact vs estimated values
[ID: data-quality-precision]

- Distinguish exact values (from specs or measurements) from estimates
  (derived, rounded, or interpolated)
- Use a naming convention or field suffix to mark estimates (e.g.
  `weightEstimated: true` or `~` prefix in display)
- Default to realistic/pessimistic estimates — never optimistic
- Document the estimation method when not obvious

## Explicit absence over invented values
[ID: data-quality-explicit-absence]

- Mark explicit absence (`null`, `None`, `?`, unread) where a source shows
  no value; never extrapolate one from neighbouring values
- Apply the rule to every artifact a verification step consumes: extractor
  and sensor output, curated ground truth, test fixtures, mock data
- Treat an invented value as a defect: a verification step takes it as a
  real target, so it mis-tunes thresholds and produces false verdicts

## Data research workflow
[ID: data-quality-research]

Gathering facts from external sources (official pages, lab reviews,
retailers, scraped documents, public APIs) can introduce errors later
validation cannot detect.

### Source-conflict resolution

- Let the most authoritative source (official publisher, manufacturer
  spec sheet, primary documentation) win on any contested field
- Treat every unverified field of a record as suspect once a secondary
  source is provably wrong on one; never cherry-pick its other figures
- Leave a field unresolved and flagged rather than overwrite it with a
  contradicted source — a known gap beats a confidently wrong value
- Record the conflict, the chosen value and the rationale beside the
  entry when two sources of equal authority disagree

### Full-record audit, not target-field audit

- Cross-check every field when verifying a record against a source, not
  only the fields that prompted the check
- Expect copy-derived records to keep stale values in fields nobody
  re-checked, such as a "v2" entry with the v1 release date

## Scoring and derived fields
[ID: data-quality-scoring]

- Scoring formulas MUST be documented — not buried in code
- All inputs to a score MUST be traceable to source data
- Scores MUST be reproducible: same inputs always produce the same
  output
- Define the scoring scale once (e.g. 1–5, step 0.5) and use it
  consistently
- Keep boolean attributes used as filters separate from scoring inputs

## Data changelog
[ID: data-quality-changelog]

- Changes to source data MUST be committed with a message explaining
  what changed and why (e.g. "fix: update product weight — publisher
  corrected spec sheet")
- When a scoring input changes, note that derived scores will change
- Do not batch unrelated data changes into a single commit — one
  entry or one field correction per commit
- For bulk imports or migrations, document the source and method in
  the commit message

## Identity and deduplication
[ID: data-quality-identity]

- Every entry MUST have a stable unique identifier that does not
  change when other fields are updated
- Define what makes two entries "the same" — document the identity
  key (e.g. manufacturer + model name + variant)
- Near-duplicates (regional names, revised versions, bundles) MUST
  be distinct entries with a relationship field linking them
- Never merge near-duplicates silently — flag for manual review
- Discontinued items that are replaced by a successor SHOULD link
  to the successor via a `replacedBy` field

## Validation
[ID: data-quality-validation]

- Validate data at ingest time — reject or flag entries that fail
  schema validation
- Use runtime schemas (Zod, JSON Schema, Pydantic) for all data
  collections; a static type, such as a TypeScript interface, validates
  nothing at runtime
- Range checks for numeric fields (e.g. weight > 0, price > 0)
- Enum checks for constrained fields (e.g. status, category)
- Build-time validation is acceptable for static sites — runtime
  validation for APIs

## Agent-assisted ground-truth validation
[ID: data-quality-hitl]

Where a human must validate each ground-truth value but the volume makes
manual entry a bottleneck:

- Never let the agent write authoritative values; it would grade its own
  output
- Have the agent run the extractor or model and emit a prediction file,
  every value labelled NOT GROUND TRUTH
- Have the human scan each value against the source, accept what is right
  and overwrite what is not
- Mark every value validated this way as assisted, not independent
- Never calibrate the producing model against assisted values; capture
  that reading blind, before any prediction is opened
- Let the agent transcribe only the human-validated values into the
  ground-truth structure, so the calibration set never becomes its own
  predictions
