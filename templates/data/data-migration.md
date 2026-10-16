# Base — Data Migration
[ID: base-data-migration]
[DEPENDS ON: templates/data/data-modeling.md]

Rules for migrating data between schemas, systems, or formats.
Covers versioned migrations, bulk transfers, and rollback strategies.

---

## Migration versioning
[ID: data-migration-versioning]

- Every migration MUST have a unique, monotonically increasing
  version identifier (timestamp or sequence number)
- Migrations MUST be idempotent — running the same migration
  twice produces the same result
- Store applied migration versions in a dedicated tracking table
  or file
- Never edit a migration that has been applied to any environment
  — create a new migration instead
- Migration files MUST be committed to version control alongside
  the code that depends on the schema change

---

## Migration structure
[ID: data-migration-structure]

- Each migration MUST contain both `up` (apply) and `down`
  (rollback) steps
- The `up` step describes the desired state change
- The `down` step MUST reverse the `up` step exactly — if
  reversal is impossible (e.g. dropping a column with data),
  document this and require manual approval
- Keep migrations small — one concern per migration
- Separate schema migrations (DDL) from data migrations (DML)
  — they have different risk profiles and rollback strategies

---

## Pre-migration checks
[ID: data-migration-prechecks]

- Validate that the current schema matches the expected starting
  state before applying a migration
- Estimate the impact: row count, lock duration, downtime window
- For large tables, test the migration on a production-sized
  dataset to measure duration and resource usage
- Back up the affected tables or database before applying
  destructive migrations

---

## Zero-downtime migrations
[ID: data-migration-zero-downtime]

- Prefer expand-and-contract pattern for breaking changes:
  1. **Expand** — add new column/table, deploy code that writes
     to both old and new
  2. **Migrate** — backfill existing data from old to new
  3. **Contract** — remove old column/table after all readers
     have switched
- Never rename a column in a single step — add new, migrate,
  drop old
- Never add a NOT NULL column without a default — it locks the
  table and breaks existing inserts
- Use online DDL tools (pt-online-schema-change, gh-ost) for
  large table alterations in MySQL/MariaDB

---

## Rollback strategy
[ID: data-migration-rollback]

- Every migration plan MUST include a rollback procedure
- Test the rollback procedure before applying the migration
  to production
- Define a rollback window — the period after deployment during
  which rollback is feasible
- If a migration is not reversible, document the recovery plan
  (restore from backup, manual data fix)
- After the rollback window closes, the migration is considered
  permanent
