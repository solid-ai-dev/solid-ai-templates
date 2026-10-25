# Base — Data Migration
[ID: base-data-migration]
[DEPENDS ON: templates/data/data-modeling.md]

Rules for migrating data between schemas, systems, or formats.
Covers versioned migrations, bulk transfers, and rollback strategies.

## Migration versioning
[ID: data-migration-versioning]

- Give every migration a unique identifier and a fixed position in the
  order of application (MUST)
- Make every migration idempotent (MUST); running the same migration
  twice produces the same result
- Store applied migration versions in a dedicated tracking table,
  collection or file
- Never edit a migration that has been applied to any environment;
  create a new migration instead
- Commit migration files to version control alongside the code that
  depends on the schema change (MUST)

## Migration structure
[ID: data-migration-structure]

- Make a migration's reversal undo its forward change exactly where
  reversal is possible (MUST)
- Keep migrations small: one concern per migration
- Separate schema migrations from data migrations; they have different
  risk profiles and rollback strategies

## Pre-migration checks
[ID: data-migration-prechecks]

- Validate that the current schema matches the expected starting
  state before applying a migration
- Estimate the impact: record count, lock duration, downtime window
- For large tables, test the migration on a production-sized dataset to
  measure duration and resource usage
- Back up the affected data or database before applying destructive
  migrations

## Zero-downtime migrations
[ID: data-migration-zero-downtime]

- Prefer the expand-and-contract pattern for breaking changes:
  1. **Expand** — add the new field or table, deploy code that writes
     to both old and new
  2. **Migrate** — backfill existing data from old to new, and verify it
  3. **Switch** — deploy code that reads and writes only the new one,
     then wait until no old reader or writer runs: no instance of the
     previous deployment, background job or scheduled task
  4. **Contract** — remove the old field or table; a dual writer still
     running fails on it
- Never rename a field in a single step; add new, migrate, drop old
- Never add a required field without a default to data in use; existing
  records lack it, and writes from code that does not set it break
- Add such a field as optional, backfill it, then make it required
- Alter a large table without holding a lock for the whole alteration,
  such as through the database's online schema-change tooling

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

- Assert, after a bulk migration whose destination keys derive from the
  source, that the written keys equal the keys derived independently from
  the source of truth (MUST)
- Treat per-record validation as blind to a partial migration: an orphan
  key and a missing entry are each individually valid
