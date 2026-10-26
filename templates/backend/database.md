# Backend — Database Conventions
[ID: backend-database]

## Schema changes

- Make every schema change through a migration committed to source
  control — never edit the database manually
- Never regenerate or modify a migration that is already merged
- Write one migration per logical change — do not batch unrelated schema
  changes
- Provide a `down` migration for every `up`; where reversal would lose
  data, say so in the migration and get approval before applying it

## Queries

- Parameterise every query that takes a value; never build a query by
  string interpolation
- Bound every query an interactive request runs with a limit or
  pagination; a filter alone is no bound, since a filter on a flag can
  still match millions of rows
- Stream or batch a deliberate export or batch scan, never load it whole
- Select only the columns or fields the code uses — never every column by
  default
- Fetch related data for a set of rows in one query or batch, never one
  query per row in a loop (N+1)

## Indexing
[LOAD: migrate-data]

- Index every foreign key column — not every engine does so automatically
- Add composite indexes for common multi-column filter + sort combinations
- Avoid over-indexing write-heavy tables — each index adds write overhead
- Drop unused indexes — check the engine's index usage statistics
  regularly

## Transactions

- Wrap multi-step writes in a transaction — commit only after all writes
  succeed
- Never leave a transaction open across a request boundary
- Keep transactions short — do not call external services inside a transaction
- Use an isolation level stronger than the engine's default only when
  genuinely required

## Connections

- Use a connection pool — never open a new connection per request
- Inject the database session/connection as a dependency — no global DB
  handles
- Set the pool size explicitly from the instance count and the
  database's connection cap, so all instances together stay under it
- Monitor pool exhaustion — alert when pool wait time exceeds threshold

## Soft deletes

- Use soft deletes (`deleted_at` timestamp) only when audit history is
  required; otherwise use hard deletes
- If using soft deletes, filter deleted rows out of every query by
  default — never return deleted rows to callers
- Keep an append-only audit log table instead of soft deletes (MAY)

## Testing
[EXTEND: base-testing]

- Reset state between test runs — truncate tables or wrap each test in a
  transaction rolled back after completion
- Do not substitute a different database engine in tests, such as an
  in-memory one — behaviour differences cause false passes
- Never run schema migrations against a production database inside a test
  suite
