# Backend — Caching
[ID: backend-caching]

Cross-cutting caching rules for any backend service. Applies regardless of
cache technology (in-process, Redis, Memcached, CDN).

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
- Cache the same data at one layer (SHOULD); several caches drift apart
  and make invalidation hard to reason about
- Where a second layer earns its place, such as a CDN in front of an
  application cache, let one layer own invalidation and give the others
  short TTLs

## Keys

- Namespace every key by service and entity, such as `users:profile:42`,
  so entries from different owners never collide
- Include a version segment when the cached schema changes, such as
  `users:v2:profile:42`
- Document the key schema — undocumented keys become orphaned entries
- Never construct keys from unvalidated user input — risk of cache poisoning

## TTL and expiry

- Give every cached entry a TTL (MUST) — no indefinite caching
- State the stale window each cached key tolerates
- Set the key's TTL no longer than that window; the TTL bounds an entry's
  age, not how stale its value was when cached

## Invalidation

- Invalidate cache entries on write, not only on TTL expiry
- Populate the cache from the source of truth, never a lagging replica
- Guard a write-back on a miss against a concurrent invalidation, such as
  with a version check, or count that race in the stale window
- Expect no atomic invalidation across a separate cache and database: an
  outbox consumer can lag, and a pub/sub subscriber can miss a message
- Treat asynchronous invalidation, such as an outbox or pub/sub, as cutting
  typical staleness, never as the bound
- Prefer targeted invalidation of the affected keys over a broad flush — a
  cache flush is an outage in disguise
- Document which code path owns invalidation for each cache key

## Resilience

- Never let a cache failure crash the application (MUST NOT)
- Treat the cache as an optional acceleration layer, not a required
  dependency
- On cache miss or error, fall through to the source of truth
- Use circuit breakers or timeouts on cache calls — a slow cache is
  worse than no cache
- Protect against cache stampede (thundering herd), such as with
  probabilistic early expiry, a lock on population, or a background refresh

## Observability

- Instrument cache hit rate, miss rate, and eviction rate
- Alert if hit rate drops significantly below baseline — the drop indicates
  misconfigured TTL or an invalidation bug
- Log cache errors at WARN level

## Testing
[EXTEND: base-testing]

- Use an in-memory fake in unit tests for cache key construction and TTL
  logic (MAY)
- Test the fallback path: assert that a cache miss or error still
  returns correct data from the source
