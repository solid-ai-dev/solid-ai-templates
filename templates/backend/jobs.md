# Backend — Background Jobs
[ID: backend-jobs]

Rules for background job processing, task queues, and scheduled work.
Applies with any queue or scheduler.

## When to use background jobs

- Move into a job any work that need not complete before the request's
  response
- Do NOT use jobs to paper over a slow synchronous path; fix the root cause
  first

## Idempotency

- Make every job idempotent (MUST): safe to execute more than once with the
  same input and produce the same outcome
- Use a deduplication key (e.g. `job_id`, `event_id`) to detect and skip
  duplicate executions
- Design for at-least-once delivery; the queue may deliver a message more
  than once, especially after a worker crash

## Retry and failure handling

- Give every job a retry limit (MUST); infinite retries will fill the queue
- Use exponential backoff with jitter between retries
- Move the job to a dead-letter queue or failed-job store (DLQ) after the
  retry limit is exhausted
- Never silently drop failed jobs
- Alert on DLQ depth; a growing DLQ is a silent production incident

## Separation of concerns

- Keep job handlers thin (MUST); delegate all business logic to service
  functions
- Use the same service functions in jobs as in request handlers, with no
  parallel logic paths (SHOULD)

## Scheduling

- Define scheduled jobs (cron-style) in code rather than configuring them
  manually in the infrastructure (MUST); this is schedule-as-code
- Document the expected frequency and maximum acceptable latency for each
  scheduled job
- Ensure only one instance of a scheduled job runs at a time; use a
  distributed lock or a leader-election mechanism

## Observability

- Emit a structured log entry at job start (INFO) and job completion (INFO)
- Log every failure at ERROR with full context: job type, ID, attempt
  number, payload summary, error message and stack trace
- Track job duration, queue depth, and failure rate as metrics
- Alert if queue depth exceeds a threshold that indicates worker starvation

## Testing
[EXTEND: base-testing]

- Unit test the service function the job delegates to, not the job handler
  itself
- Integration test the happy path end-to-end: enqueue → execute → assert
  side effect
- Test the retry path: assert that a transient failure triggers a retry
- Test the DLQ path: assert that a permanent failure ends up in the DLQ
