# Base — Data Modeling
[ID: base-data-modeling]

Rules for schema design, naming, normalization, and relationships, in any
store: a relational database, a document store or a static data file.

## Naming conventions
[ID: data-modeling-naming]

- Use one naming convention per store for every table or collection,
  field, key and index; record it in the project's context file
- Name a boolean field as a predicate (e.g. `is_active`, `has_discount`)
- Name a reference field after the record it points to (e.g. `user_id`)

## Normalization
[ID: data-modeling-normalization]

- Give every table or collection a primary key — prefer surrogate keys for
  internal use, natural keys for external-facing APIs
- Store each fact in one place by default — duplicate it only when
  measured read performance requires it
- Never pack several values into one string field, such as
  comma-separated values — use a list or a related record
- Replace repeated groups of fields (e.g. `phone1`, `phone2`, `phone3`)
  with a child table or a list
- Document the rationale when intentionally denormalizing

## Relationships
[ID: data-modeling-relationships]

- Never rely on application code alone to keep references valid
- Enforce valid references with the store's own constraint where it has
  one, else with a check that every reference resolves
- Decide for every reference what deleting its target does:
  - delete the referencing records for strong ownership
  - clear the reference for a weak one
  - refuse the delete when an orphan indicates a bug
- Keep a record apart, referenced by key, unless it has no life outside
  its parent
- Document a self-referencing relationship's (e.g. `parent_id`) maximum
  depth and cycle prevention strategy (MUST)

## Schema evolution
[ID: data-modeling-evolution]

- Run every schema change through a versioned migration (MUST); never
  change a production schema by hand
- Prefer additive changes, such as a new field, table or collection
- Keep an additive change compatible with old writers: add a field
  optional or with a default, never required without one where records
  exist
- Give every destructive change (drop or rename a field) a migration plan:
  add new → migrate data → drop old (MUST)
- Include both up and down steps in every migration (MUST)
- Say so where a down step cannot restore the data, and get approval
  before applying that migration
- Test migrations against a production-like dataset before deploying

## Data types
[ID: data-modeling-types]

- Use the most specific type the store offers — a date type, not a
  string, for dates
- Store timestamps in UTC — convert to local time at the
  presentation layer
- Store monetary values as integers in minor units or as a decimal type —
  never floating point
- Use `UUID` or `ULID` for distributed ID generation — auto-increment
  is acceptable for single-database systems
- Document a maximum length for every text field (MUST); unbounded text
  invites abuse and complicates indexing
