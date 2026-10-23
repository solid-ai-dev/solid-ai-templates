# Backend — Caching
[ID: backend-caching]

Cross-cutting caching rules for any backend service. Applies regardless of
cache technology (Redis, Memcached, in-process).

## When to cache

- Cache data that is expensive to compute or retrieve and changes infrequently
- Do NOT cache data that MUST be real-time (e.g. account balances, stock levels)
- Do NOT cache secrets, credentials, tokens, or PII — even temporarily
- Prefer no cache over a stale cache for safety-critical or financial data

## Patterns

- Use cache-aside (lazy loading) as the default pattern for read-heavy
  workloads: read from cache first; on miss, load from source, populate
  cache, return result
- Use write-through, writing to cache and source together on every update,
  to shorten the stale window when write latency is acceptable
- Expect write-through never to close the stale window; the two writes are
  not atomic
- Avoid write-behind, writing to cache immediately and persisting to source
  asynchronously, unless throughput requirements justify the added
  complexity and risk
- Never cache at more than one layer for the same data — multiple caches
  create inconsistency and make invalidation impossible to reason about

## Keys

- Namespace keys as `<service>:<entity>:<id>` — e.g. `users:profile:42`
- Include a version segment when the cached schema changes:
  `users:v2:profile:42`
- Document the key schema — undocumented keys become orphaned entries
- Never construct keys from unvalidated user input — risk of cache poisoning

## TTL and expiry

- Give every cached entry a TTL (MUST) — no indefinite caching
- Set TTL based on acceptable staleness, not convenience
- Use shorter TTLs (seconds–minutes) for frequently changing data;
  longer TTLs (hours–days) for reference data
- Use cache tags or explicit invalidation for data that must expire on write,
  not just on timeout

## Invalidation

- Invalidate cache entries on write, not only on TTL expiry
- State the stale window each cached key tolerates
- Set the key's TTL no longer than that window; the TTL is the bound
- Expect no atomic invalidation across a separate cache and database: an
  outbox consumer can lag, and a pub/sub subscriber can miss a message
- Invalidate through an outbox or pub/sub to cut typical staleness, never
  as the bound
- Bypass the cache for data that tolerates no stale window
- Prefer targeted invalidation (`DEL users:profile:42`) over broad flush
  (`FLUSHDB`) — a cache flush is an outage in disguise
- Document which code path owns invalidation for each cache key

## Resilience

- Never let a cache failure crash the application (MUST NOT)
- Treat the cache as an optional acceleration layer, not a required
  dependency
- On cache miss or error, fall through to the source of truth
- Use circuit breakers or timeouts on cache calls — a slow cache is
  worse than no cache
- Protect against cache stampede (thundering herd): use probabilistic early
  expiry, a mutex/lock on population, or a background refresh

## Observability

- Instrument cache hit rate, miss rate, and eviction rate
- Alert if hit rate drops significantly below baseline — the drop indicates
  misconfigured TTL or an invalidation bug
- Log cache errors at WARN level; log stampede events at INFO

## Testing
[EXTEND: base-testing]

- Use an in-memory fake in unit tests for cache key construction and TTL
  logic (MAY)
- Test the fallback path: assert that a cache miss or error still
  returns correct data from the source
