# Base — Data Modeling
[ID: base-data-modeling]

Rules for schema design, naming, normalization, and relationships.
Applies to relational databases, document stores, and static data
files alike.

---

## Naming conventions
[ID: data-modeling-naming]

- Table and collection names MUST be lowercase, plural, snake_case
  (e.g. `order_items`, `user_roles`)
- Column and field names MUST be lowercase snake_case
  (e.g. `created_at`, `unit_price`)
- Boolean columns MUST use `is_`, `has_`, or `can_` prefix
  (e.g. `is_active`, `has_discount`)
- Foreign keys MUST follow `<referenced_table_singular>_id`
  (e.g. `user_id`, `order_id`)
- Junction tables MUST combine both table names alphabetically
  (e.g. `products_tags`, not `tags_products`)
- Index names MUST follow `ix_<table>_<columns>`; unique index
  `ux_<table>_<columns>`

---

## Normalization
[ID: data-modeling-normalization]

- Default to third normal form (3NF) — denormalize only when
  measured read performance requires it
- Every table MUST have a primary key — prefer surrogate keys
  (`id`) for internal use, natural keys for external-facing APIs
- No multi-valued columns — use a related table instead of
  comma-separated values or JSON arrays in relational stores
- Repeated groups of columns (e.g. `phone1`, `phone2`, `phone3`)
  signal a missing child table
- Document the rationale when intentionally denormalizing

---

## Relationships
[ID: data-modeling-relationships]

- Define foreign keys explicitly — do not rely on application-level
  enforcement alone
- Choose cascade behavior deliberately:
  - `CASCADE` for strong ownership (delete parent → delete children)
  - `SET NULL` for weak references
  - `RESTRICT` when orphans indicate a bug
- Many-to-many relationships MUST use a junction table with
  composite primary key
- Self-referencing relationships (e.g. `parent_id`) MUST document
  maximum depth and cycle prevention strategy

---

## Schema evolution
[ID: data-modeling-evolution]

- Schema changes MUST go through versioned migrations — never
  apply DDL manually in production
- Additive changes (new column, new table) are safe — prefer them
- Destructive changes (drop column, rename) require a migration
  plan: add new → migrate data → drop old
- Every migration MUST be reversible — include both up and down
  steps
- Test migrations against a production-like dataset before deploying

---

## Data types
[ID: data-modeling-types]

- Use the most specific type available — `DATE` not `VARCHAR` for
  dates, `DECIMAL` not `FLOAT` for money
- Store timestamps in UTC — convert to local time at the
  presentation layer
- Store monetary values as integers (cents) or `DECIMAL` — never
  floating point
- Use `UUID` or `ULID` for distributed ID generation — auto-increment
  is acceptable for single-database systems
- Text fields MUST have a documented maximum length — unbounded text
  invites abuse and complicates indexing
