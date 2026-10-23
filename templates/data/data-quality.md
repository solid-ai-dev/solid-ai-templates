# Base — Data Quality
[ID: base-data-quality]
[DEPENDS ON: templates/data/data-modeling.md]

Rules for projects where content or data accuracy matters as much as
code quality. Applies to catalogues, reference datasets, published
content, and any project that declares data as a first-class concern.

## Data sourcing
[ID: data-quality-sourcing]

- Trace every data point to a named source (URL, publication,
  manufacturer spec sheet) (MUST)
- Record the source alongside the data — not in a separate document
- Prefer primary sources (manufacturer, official docs) over aggregators
- Document the conflict and the chosen value with rationale when
  multiple sources conflict
- Never fabricate or estimate values without marking them as estimates

## Completeness tracking
[ID: data-quality-completeness]

- Define a completeness score for each entry: fields populated / total
  fields (e.g. `14/14`)
- Track completeness at the entry level, not just the collection level
- Make incomplete entries queryable (MUST): add a `completeness` or
  `dataStatus` field
- Set a minimum completeness threshold for publishing (e.g. 80%)
- Never show entries below the threshold in user-facing views
  (MUST NOT); they MAY exist in the database

## Freshness
[ID: data-quality-freshness]

- Record when each entry was last verified: `lastVerified` date field
- Define a freshness window per collection (e.g. prices: 30 days,
  specs: 12 months)
- Flag entries beyond their freshness window for review (SHOULD)
- Record the capture date beside every time-sensitive value, such as a
  price; never show one without it (MUST)
- Mark discontinued or unavailable items instead of deleting them (MUST)

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

- Document scoring formulas (MUST) — never leave them buried in code
- Keep every input to a score traceable to source data (MUST)
- Make scores reproducible (MUST): same inputs always produce the same
  output
- Define the scoring scale once (e.g. 1–5, step 0.5) and use it
  consistently
- Keep boolean attributes used as filters separate from scoring inputs

## Data changelog
[ID: data-quality-changelog]

- Commit changes to source data with a message explaining what
  changed and why (e.g. "fix: update product weight — publisher
  corrected spec sheet") (MUST)
- When a scoring input changes, note that derived scores will change
- Do not batch unrelated data changes into a single commit — one
  entry or one field correction per commit
- Document the source and method in the commit message for bulk imports
  or migrations

## Identity and deduplication
[ID: data-quality-identity]

- Give every entry a stable unique identifier that does not change when
  other fields are updated (MUST)
- Define what makes two entries "the same"
- Document the identity key (e.g. manufacturer + model name + variant)
- Keep near-duplicates (regional names, revised versions, bundles) as
  distinct entries with a relationship field linking them (MUST)
- Never merge near-duplicates silently; flag them for manual review
- Link a discontinued item that is replaced by a successor to the
  successor via a `replacedBy` field (SHOULD)

## Validation
[ID: data-quality-validation]

- Validate data at ingest time — reject or flag entries that fail
  schema validation
- Use runtime schemas (Zod, JSON Schema, Pydantic) for all data
  collections; a static type, such as a TypeScript interface, validates
  nothing at runtime
- Apply range checks to numeric fields (e.g. weight > 0, price > 0)
- Apply enum checks to constrained fields (e.g. status, category)
- Validate static sites at build time instead of at runtime (MAY);
  validate APIs at runtime

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
