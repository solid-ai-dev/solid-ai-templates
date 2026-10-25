# Backend — Concurrency
[ID: backend-concurrency]

Rules for threads, processes, async I/O and actors. A stack template
extends this one with its language's rules.

## When to use what

- Never run blocking I/O or long CPU work on a thread that runs an event
  loop or accepts requests
- Hand such work to a worker pool or a separate process
- Never run CPU-bound work on threads the runtime runs one at a time;
  use processes

## Shared state

- Avoid shared mutable state — prefer immutable data structures or
  message passing (queues, channels)
- If shared state is unavoidable, protect every access with a lock;
  document which lock guards which data
- Never hold a lock while performing I/O — risk of deadlock and contention
- Prefer fine-grained locks over a single global lock

## Structured concurrency

- Never start a thread, task, actor or process without a clear owner and
  a clear shutdown path
- Run concurrent work under one scope that waits for, and can cancel,
  all of it; never fire and forget
- Propagate cancellation to every operation that may block, by the
  runtime's own mechanism
- On shutdown, stop admitting new work, let in-flight work drain until
  the drain deadline, then cancel what remains — do not rely on OS cleanup
- Wait for cancelled work only for a bounded cancellation period, then
  release resources even when some of it ignores cancellation
- Exit by one hard deadline covering draining, cancelling and releasing,
  whatever is still running then
- Leave time before that deadline to release resources, and keep the
  deadline inside the grace period the platform allows before a kill

## Pitfalls

- Acquire locks in one consistent order, so no two threads deadlock
  waiting on each other
- Add backoff or a tiebreaker where threads can livelock, yielding to each
  other without progress
- Bound queue sizes and schedule fairly where the runtime allows, so
  low-priority work never starves
- Pass request context (request ID, user identity) explicitly in pools
  and async code; never store it in thread-locals

## Observability

- Log the concurrency model in use at service startup (pool sizes,
  worker count)
- Track live threads, tasks or processes as a metric; unbounded growth
  is a leak
- Alert when work stops completing while the service stays up, the
  symptom of a deadlock

## Testing

- Write stress tests for any code that shares state: run many threads or
  tasks at once and assert invariants hold
- Prove statelessness with disjoint inputs: fire parallel requests whose
  expected-output sets do not overlap, and assert every response falls
  within its own request's set
- Test cancellation paths: assert that cancelling an operation stops it
  promptly and releases its resources
