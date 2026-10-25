# Backend — Messaging
[ID: backend-messaging]

Cross-cutting rules for asynchronous messaging in backend services.
Applies regardless of message broker (Kafka, RabbitMQ, SQS, or equivalent).

## When to use async messaging

- Use messaging when the producer does not need an immediate response
- Use messaging for workloads that must survive producer restarts —
  fire-and-forget with durability
- Use messaging to decouple services that scale independently
- Do NOT use messaging when the caller needs a synchronous result — use HTTP or
  gRPC instead
- Do NOT replace a simple job queue within one service with a broker

## Producer rules

- Validate message schema before publishing — the producer is responsible for
  schema correctness; the consumer should not be the first line of defence
- Include a correlation ID (trace ID or request ID) in every message's headers
  (MUST) so consumers can link it to the originating request
- Use deterministic message IDs where the broker supports them — this allows
  broker-level deduplication on producer retry
- Do not publish inside a database transaction without the transactional outbox
  pattern — a commit/publish race will cause lost or phantom messages
- **Outbox pattern**: write the message to an outbox in the same
  transaction as the domain write; a relay process publishes from the outbox
  asynchronously

## Consumer rules

- Design all consumers to be **idempotent** — at-least-once delivery is the
  default; the same message will arrive more than once under failure conditions
- ACK only after the message has been fully processed, or durably handed
  off to a queue or job record that then owns its retries and terminal
  failures — never ACK at receipt
- NACK or leave the message unacknowledged on a failure before that point, so
  the broker requeues it or routes it to the dead-letter queue (DLQ)
- Never silently discard a message that fails before that point
- Apply exponential backoff on retries — tight retry loops amplify downstream
  failures
- Move messages to the DLQ after a configurable maximum retry count —
  the DLQ is the primary alerting surface for consumer failures
- Keep consumer handlers thin — delegate logic to a service function, exactly
  as HTTP handlers delegate to services

## Load and backpressure

- Decouple receive from process under load: hand the message off durably,
  acknowledge it, and do the work in a worker you pace
- Never run heavy processing inline on the receive path under load
- Coalesce bursts of events whose work reads current source state: debounce
  repeated "refresh product 42" events into one refresh after a short
  quiet period
- Never coalesce events that each carry a change; two inventory
  decrements for product 42 are two decrements, not a duplicate
- Apply backpressure when the queue saturates: bound the queue and slow
  or shed intake so the system degrades gracefully — an unbounded intake
  amplifies a downstream slowdown into an outage
- Enforce per-key or per-tenant fairness: cap in-flight work per source
  so one noisy producer cannot starve the rest (head-of-line blocking)
- Load-test the consumer at volume: watch queue depth and consumer lag,
  not the receive endpoint's latency, to find the real saturation point

## Schema and contracts

- Define message schemas explicitly, in a format such as JSON Schema, Avro or Protobuf
- Keep schema changes backward-compatible (MUST): add fields, never remove
  or rename required fields without a versioning strategy
- Version the schema on breaking changes: encode the version in the topic name
  (`orders.v2`) or as a `schema_version` field in the payload

## Observability

- Log at consumer entry: message ID, topic/queue name, correlation ID,
  subscription or consumer group
- Log at consumer exit: processing duration, outcome (success / retry / DLQ)
- Track per topic/queue:
  - Consumer lag or queue depth, whichever the broker exposes
  - Processing time (p50 / p95 / p99)
  - Error rate and DLQ depth
- Alert when:
  - Consumer lag grows continuously for > N minutes
  - DLQ depth exceeds a threshold
  - Consumer processing time exceeds the defined SLA

## Testing
[EXTEND: base-testing]

- Unit-test consumer business logic independently of the broker —
  pass a constructed message object directly to the handler function
- Test the DLQ path: publish a message designed to fail processing
  and assert it reaches the DLQ after the expected retry count
- Test idempotency: publish the same message twice and assert the
  consumer produces the same result with no unintended side effects
