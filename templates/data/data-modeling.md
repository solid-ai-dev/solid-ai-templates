# Base — Data Modeling
[ID: base-data-modeling]

Rules for schema design, naming, normalization, and relationships. A rule
that names a relational store applies there only; the rest apply to
relational databases, document stores and static data files alike.

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
- Use third normal form (3NF) by default in a relational store —
  denormalize only when measured read performance requires it
- Never hold several values in one relational column, as comma-separated
  values or a JSON array — use a related table
- Replace repeated groups of fields (e.g. `phone1`, `phone2`, `phone3`)
  with a child table or a list
- Document the rationale when intentionally denormalizing

## Relationships
[ID: data-modeling-relationships]

- Define relational foreign keys explicitly — do not rely on
  application-level enforcement alone
- Set each foreign key's cascade behavior deliberately:
  - `CASCADE` for strong ownership (delete parent → delete children)
  - `SET NULL` for weak references
  - `RESTRICT` when orphans indicate a bug
- Use a junction table keyed by both references for a relational
  many-to-many (MUST)
- Keep a record in a document or data file apart, referenced by key,
  unless it has no life outside its parent
- Document a self-referencing relationship's (e.g. `parent_id`) maximum
  depth and cycle prevention strategy (MUST)

## Schema evolution
[ID: data-modeling-evolution]

- Run every schema change through a versioned migration (MUST); never
  change a production schema by hand
- Prefer additive changes (new column, new table); they stay compatible
  only when old writers still succeed, so add a column nullable or with a
  default, never NOT NULL without one on a populated table
- Give every destructive change (drop column, rename) a migration plan:
  add new → migrate data → drop old (MUST)
- Include both up and down steps in every migration (MUST); where the
  down step cannot restore the data, say so and get approval before
  applying it
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
