# Base — Data Migration
[ID: base-data-migration]
[DEPENDS ON: templates/data/data-modeling.md]

Rules for migrating data between schemas, systems, or formats.
Covers versioned migrations, bulk transfers, and rollback strategies.

## Migration versioning
[ID: data-migration-versioning]

- Give every migration a unique, monotonically increasing version
  identifier (timestamp or sequence number) (MUST)
- Make every migration idempotent (MUST); running the same migration
  twice produces the same result
- Store applied migration versions in a dedicated tracking table
  or file
- Never edit a migration that has been applied to any environment;
  create a new migration instead
- Commit migration files to version control alongside the code that
  depends on the schema change (MUST)

## Migration structure
[ID: data-migration-structure]

- Describe the desired state change in the `up` step
- Make the `down` step reverse the `up` step exactly where reversal is
  possible (MUST)
- Keep migrations small: one concern per migration
- Separate schema migrations (DDL) from data migrations (DML); they
  have different risk profiles and rollback strategies

## Pre-migration checks
[ID: data-migration-prechecks]

- Validate that the current schema matches the expected starting
  state before applying a migration
- Estimate the impact: row count, lock duration, downtime window
- For large tables, test the migration on a production-sized dataset to
  measure duration and resource usage
- Back up the affected tables or database before applying
  destructive migrations

## Zero-downtime migrations
[ID: data-migration-zero-downtime]

- Prefer the expand-and-contract pattern for breaking changes:
  1. **Expand** — add new column/table, deploy code that writes
     to both old and new
  2. **Migrate** — backfill existing data from old to new, and verify it
  3. **Switch** — deploy code that reads and writes only the new one,
     then wait until no old reader or writer runs: no instance of the
     previous deployment, background job or scheduled task
  4. **Contract** — remove the old column/table; a dual writer still
     running fails on it
- Never rename a column in a single step; add new, migrate, drop old
- Never add a NOT NULL column without a default to a table in use; it
  fails on existing rows and breaks inserts from code that does not set it
- Add such a column nullable, backfill it, then constrain it
- Use the database's online schema-change tooling for large table
  alterations

## Rollback strategy
[ID: data-migration-rollback]

- Include a rollback procedure in every migration plan (MUST)
- Test the rollback procedure before applying the migration
  to production
- Define a rollback window: the period after deployment during
  which rollback is feasible
- Document the recovery plan (restore from backup, manual data fix)
  if a migration is not reversible
- Treat the migration as permanent after the rollback window closes

## Post-migration checks
[ID: base-testing-data-validation]

- Assert, after a bulk migration that writes records keyed by a derived
  slug, that the written keys equal the slugs derived independently from
  the source of truth (MUST)
- Treat per-record validation as blind to a partial migration: an orphan
  key and a missing entry are each individually valid
