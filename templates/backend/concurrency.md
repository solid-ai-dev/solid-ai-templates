# Backend — Concurrency
[ID: backend-concurrency]

Rules for multi-threading, multi-processing and async I/O; a stack
template extends this one with its language's rules.

## When to use what

| Workload | Recommended model | Avoid |
|---|---|---|
| I/O-bound (network, disk, DB) | Async / non-blocking I/O or thread pool | Blocking the main thread |
| CPU-bound (compute, encoding) | Separate processes | Threads in runtimes with a GIL |
| Mixed I/O + CPU | Async for I/O, process pool for CPU | Single-threaded blocking |
| True parallelism required | Language with native threading (e.g. Go) or multiprocessing | Green threads for CPU work |

Default to async for I/O-bound services. Reach for processes only when
CPU-bound work cannot be offloaded to a background job or worker process.

## Shared state

- Avoid shared mutable state — prefer immutable data structures or
  message passing (queues, channels)
- If shared state is unavoidable, protect every access with a lock;
  document which lock guards which data
- Never hold a lock while performing I/O — risk of deadlock and contention
- Prefer fine-grained locks over a single global lock

## Structured concurrency

- Never start a thread, goroutine, or async task without a clear owner
  and a clear shutdown path
- Use structured concurrency primitives (e.g. `errgroup`, `asyncio.TaskGroup`,
  `ExecutorService`) over fire-and-forget
- Propagate cancellation explicitly — pass a cancellation token or context
  as the first argument to any function that may block
- On shutdown, stop admitting new work, let in-flight work drain until
  the drain deadline, then cancel what remains — do not rely on OS cleanup
- Wait for cancelled work only for a bounded cancellation period, then
  release resources even when some of it ignores cancellation
- Exit by one hard deadline covering draining, cancelling and releasing,
  whatever is still running then

## Pitfalls

- Acquire locks in one consistent order, so no two threads deadlock
  waiting on each other
- Add backoff or a tiebreaker where threads can livelock, yielding to each
  other without progress
- Run a race detector in tests (e.g. `go test -race`, ThreadSanitizer) to
  catch outcomes that depend on scheduling
- Bound queue sizes and schedule fairly where the runtime allows, so
  low-priority work never starves
- Pass request context (request ID, user identity) explicitly in pools
  and async code; never store it in thread-locals

## Observability

- Log the concurrency model in use at service startup (thread pool size,
  event loop policy, worker count)
- Track the thread, goroutine or task count as a metric; unbounded growth
  is a leak
- Alert on deadlock symptoms: requests timing out uniformly across all
  endpoints with no error in logs

## Testing

- Run tests with the race detector enabled in CI — do not rely on
  code review alone to catch data races
- Write stress tests for any code that shares state: run N goroutines /
  threads concurrently and assert invariants hold
- Prove statelessness with disjoint inputs: fire parallel requests whose
  expected-output sets do not overlap, and assert every response falls
  within its own request's set
- Test cancellation paths: assert that cancelling a context or token
  terminates the operation promptly and cleans up resources
