# Backend — Database Conventions
[ID: backend-database]

## Schema changes

- Make every schema change through a migration — never edit the database
  manually
- Commit migrations to source control
- Never regenerate or modify a migration that is already merged
- Write one migration per logical change — do not batch unrelated schema
  changes
- Provide a `down` migration for every `up`; where reversal would lose
  data, say so in the migration and get approval before applying it

## Queries

- Never write raw SQL strings — use an ORM or query builder
- Use parameterised queries if raw SQL is unavoidable — never string
  interpolation
- Never write an unbounded query — always apply a limit or filter
- Avoid `SELECT *` — select only the columns actually needed
- Detect and eliminate N+1 queries — use eager loading (`joinedload`,
  `preload`, `WITH` clauses, `DataLoader`) for related data fetched in a loop
- Prefer indexed columns in `WHERE`, `JOIN ON`, and `ORDER BY` clauses
- Review slow query logs in staging before releasing schema changes

## Indexing

- Add an index for every foreign key — most ORMs do not do this automatically
- Add composite indexes for common multi-column filter + sort combinations
- Avoid over-indexing write-heavy tables — each index adds write overhead
- Use partial indexes for filtered queries on large tables
  (e.g. `WHERE deleted_at IS NULL`)
- Drop unused indexes — check `pg_stat_user_indexes` or equivalent regularly

## Transactions

- Wrap multi-step writes in a transaction — commit only after all writes
  succeed
- Never leave a transaction open across an HTTP request boundary
- Keep transactions short — do not call external services inside a transaction
- Use serialisable isolation only when genuinely required; prefer read
  committed for OLTP workloads

## Connections

- Use a connection pool — never open a new connection per request
- Inject the database session/connection as a dependency — no global DB
  handles
- Set explicit pool size limits from the instance count and the
  database's connection cap (e.g. `pool_size=10`, `max_overflow=5` for one
  instance)
- Monitor pool exhaustion — alert when pool wait time exceeds threshold

## Soft deletes

- Use soft deletes (`deleted_at` timestamp) only when audit history is
  required; otherwise use hard deletes
- If using soft deletes, add a partial index on `deleted_at IS NULL` and
  filter all queries by default — never return deleted rows to callers
- Keep an append-only audit log table instead of soft deletes (MAY)

## Testing
[EXTEND: base-testing]

- Reset state between test runs — truncate tables or wrap each test in a
  transaction rolled back after completion
- Do not substitute a different database engine in tests (e.g. SQLite
  instead of PostgreSQL) — behaviour differences cause false passes
- Never run schema migrations against a production database inside a test
  suite
