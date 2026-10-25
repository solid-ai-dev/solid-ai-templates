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

## Service boundaries

- Draw service boundaries on bounded contexts: each service owns one
  domain concept end to end
- Let a service own its data, logic and API; no other service reaches in
- Never share a database between services (MUST NOT); it couples them and
  blocks independent deployment
- Limit shared libraries to cross-cutting infrastructure (logging,
  tracing, HTTP client config) (MUST); never domain logic
- Treat two services that keep changing together as likely one service,
  and review whether to merge them

## Inter-service communication

- Call another service synchronously only when the caller needs its answer
  to continue, such as an auth check or a price lookup
- Prefer async messaging for cross-service workflows; it decouples
  availability and limits cascades
- Give every synchronous call a timeout and a circuit breaker
- Never chain more than two synchronous calls in one request path; each hop
  multiplies latency and failure

## Data management

- Design UX and business logic for eventual consistency; distributed data
  cannot be both consistent and highly available (CAP)
- Copy read-only data across boundaries by events, never by joins across
  service databases

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
- Keep the gateway to edge concerns, such as routing, token validation,
  rate limiting, TLS termination and request logging
- Keep business logic out of the gateway
- Route service-to-service calls around the gateway, over a mutually
  authenticated channel

## Service discovery

- Use a service registry or the platform's discovery; never hardcode
  service URLs in configuration
- Give every service a health check (MUST); the registry routes only to
  healthy instances

## Contract testing

- Test each producer and consumer pair with consumer-driven contract tests
- Never break a published contract without a versioned migration path
  (MUST NOT); a failing contract test blocks the producer's deployment
- Run contract tests in CI on both sides

## Backward compatibility

- Version and deprecate every service API as a public API, by the API
  template's rules
- Read tolerantly: consumers ignore unknown fields
- Enforce event schema compatibility automatically when a schema is
  published (SHOULD)

## Observability

- Propagate the trace context through every service call and message
  (MUST); distributed tracing is mandatory here
- Collect every service's logs and metrics in one place; make the logs
  searchable by trace ID
