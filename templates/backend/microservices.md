# Backend — Microservices
[ID: backend-microservices]
[DEPENDS ON: templates/backend/api.md, templates/backend/http.md, templates/backend/messaging.md]

Rules for projects explicitly built as a microservices architecture.
Do not apply this template to a monolith or a single-service project.

## When to use microservices

- Start with a modular monolith; extract a service only for a proven reason
- Extract for independent scaling, independent deployment cadence, a
  different technology, or a team boundary (Conway's Law)
- Never extract because it feels cleaner or more modern; the operational
  cost is real and front-loaded
- Treat two or three services as a distributed monolith in waiting, and
  apply these rules only to an intentionally service-oriented system

## Service boundaries

- Draw service boundaries on bounded contexts: each service owns one
  domain concept end to end
- Let a service own its data, logic and API; no other service reaches in
- Never share a database between services (MUST NOT); it couples them and
  blocks independent deployment
- Limit shared libraries to cross-cutting infrastructure (logging,
  tracing, HTTP client config) (MUST); never domain logic
- Merge two services that keep changing together

## Inter-service communication

Choose the style by the interaction:

| Interaction | Style | Example |
|---|---|---|
| Request needs an immediate response | Synchronous (REST or gRPC) | Auth check, price lookup |
| Caller does not need to wait | Asynchronous (events/messages) | Order placed, user registered |
| Streaming or bidirectional | gRPC streaming | Live feed, file upload |

- Prefer async messaging for cross-service workflows; it decouples
  availability and limits cascades
- Give every synchronous call a timeout and a circuit breaker
- Never chain more than two synchronous calls in one request path; each hop
  multiplies latency and failure

## Data management

- Give each service its own schema and storage; never reach into another
  service's database
- Design UX and business logic for eventual consistency; distributed data
  cannot be both consistent and highly available (CAP)
- Copy read-only data across boundaries by events, never by joins across
  service databases
- Use the outbox pattern so a database write and its event publish are
  atomic

## Distributed transactions

- Avoid two-phase commit; it is fragile and does not compose with async
  systems
- Use a saga for a multi-service workflow that must stay consistent:
  - Choreography, each service reacting to events, for short workflows
  - Orchestration, one orchestrator issuing compensations, for complex or
    long-running ones
- Define a compensating action for every saga step, beside its forward
  action (MUST)

## API gateway

- Give external clients one entry point, an API gateway; never expose
  internal service URLs
- Route, validate auth tokens, rate-limit, terminate TLS and log requests
  at the gateway
- Keep business logic out of the gateway
- Route internal calls around the gateway, through a mesh or direct mutual
  TLS

## Service discovery

- Use a service registry or the platform's discovery; never hardcode
  service URLs in configuration
- Give every service a health check (MUST); the registry routes only to
  healthy instances

## Contract testing

- Test each producer and consumer pair with consumer-driven contract tests
  (e.g. Pact)
- Never break a published contract without a versioned migration path
  (MUST NOT); a failing contract test blocks the producer's deployment
- Run contract tests in CI on both sides

## Backward compatibility

- Version and deprecate every service API as a public API, by the API
  template's rules
- Read tolerantly: consumers ignore unknown fields
- Add fields; never remove or rename one without a major version bump
- Hold event schemas to the same rules; enforce compatibility on publish
  with a schema registry (SHOULD)

## Observability

- Propagate the `traceparent` header from every service (MUST);
  distributed tracing is mandatory here
- Aggregate every service's logs on one platform, searchable by trace ID
  in under 30 seconds
- Expose metrics per service, and correlate them on one central dashboard
- Define an SLO for each public-facing service; alert on SLO burn rate,
  not just on errors
