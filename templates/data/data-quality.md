# Base — Data Quality
[ID: base-data-quality]
[DEPENDS ON: templates/data/data-modeling.md]

Rules for projects where content or data accuracy matters as much as
code quality. Applies to catalogues, reference datasets, published
content, and any project that declares data as a first-class concern.

## Data sourcing
[ID: data-quality-sourcing]

- Trace every data point to a named source (URL, publication, dataset)
  (MUST)
- Record the source alongside the data — not in a separate document
- Prefer primary sources (the publisher, official docs) over aggregators
- Record the conflict, the chosen value and its rationale beside the entry
  when sources conflict
- Never fabricate or estimate values without marking them as estimates

## Completeness tracking
[ID: data-quality-completeness]

- Track completeness at the entry level, not just the collection level
- Make incomplete entries queryable (MUST), such as by a completeness or
  status field

## Freshness
[ID: data-quality-freshness]

- Record the date each entry was last verified
- Define a freshness window per collection (e.g. prices: 30 days,
  reference figures: 12 months)
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
- Apply the rule to every artifact a verification step consumes, such as
  tool output, curated ground truth, test fixtures and mock data
- Treat an invented value as a defect: a verification step takes it as a
  real target, so it mis-tunes thresholds and produces false verdicts

## Data research workflow
[ID: data-quality-research]

Gathering facts from external sources (official pages, reviews, scraped
documents, public APIs) can introduce errors later validation cannot
detect.

### Source-conflict resolution

- Let the most authoritative source (the official publisher, primary
  documentation) win on any contested field
- Treat every unverified field of a record as suspect once a secondary
  source is provably wrong on one; never cherry-pick its other figures
- Leave a field unresolved and flagged rather than overwrite it with a
  contradicted source — a known gap beats a confidently wrong value

### Full-record audit, not target-field audit

- Cross-check every field when verifying a record against a source, not
  only the fields that prompted the check
- Expect copy-derived records to keep stale values in fields nobody
  re-checked, such as a "v2" entry with the v1 release date

## Derived values
[ID: data-quality-scoring]

- Document every formula that derives a value, such as a score (MUST);
  never leave one buried in code
- Keep every input to a derived value traceable to source data (MUST)
- Make derived values reproducible (MUST): same inputs always produce the
  same output

## Data changelog
[ID: data-quality-changelog]

- Record with every change to source data what changed and why, such as
  in its commit message (MUST)
- When an input to a derived value changes, note that the value will
  change
- Do not batch unrelated data changes into a single change

### Recording a bulk import
[LOAD: migrate-data]

- Record the source and method of a bulk import or migration with it

## Identity and deduplication
[ID: data-quality-identity]

- Give every entry a stable unique identifier that does not change when
  other fields are updated (MUST)
- Define and document the identity key that makes two entries "the same"
- Keep near-duplicates (regional names, revised versions) as distinct
  entries with a relationship field linking them (MUST)
- Never merge near-duplicates silently; flag them for manual review
- Link a discontinued entry replaced by a successor to that successor
  (SHOULD)

## Validation
[ID: data-quality-validation]

- Validate data at ingest time — reject or flag entries that fail
  schema validation
- Validate every data collection against an executable schema; a static
  type declaration validates nothing at runtime
- Apply range checks to numeric fields (e.g. weight > 0, price > 0)
- Apply enum checks to constrained fields (e.g. status, category)
- Validate data built into an artifact at build time instead of at
  runtime (MAY); validate data received while running at runtime

## Independent reference values
[ID: data-quality-hitl]

- Never let the producer of a value write the reference value it is
  checked against; it would grade its own output
