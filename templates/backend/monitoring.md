# Backend — Monitoring
[ID: backend-monitoring]
[DEPENDS ON: templates/backend/observability.md]

## Key metrics

Monitor at minimum, in every service (MUST):

| Metric | Why |
|--------|-----|
| Latency (p50, p95, p99) | Detect latency degradation |
| Error rate (client and server errors) | Detect functional failures |
| Throughput | Detect traffic spikes and capacity limits |
| Saturation of each resource the service consumes, such as CPU, memory or disk | Detect leaks, exhaustion and scaling needs |

- Add custom metrics for business-critical operations specific to the
  service (e.g. orders processed, jobs queued, messages consumed)

## Thresholds and alerts

- Derive thresholds from observed behaviour over time (MUST)
- Never set thresholds to arbitrary round numbers without a measurement
  baseline (MUST NOT)
- Define a corresponding alert for every failure scenario of the two
  highest severities before the service is promoted to production (MUST)
- Make alerts actionable (MUST); give every alert a clear response procedure

## Dashboards

- Give every service a service health dashboard (MUST)
- Show on the dashboard at minimum: latency, error rate, throughput,
  and resource saturation (MUST)

## Incident response

- Document a post-mortem after resolution for every incident of the two
  highest severities (MUST)
- Include in every post-mortem: timeline, root cause, impact, corrective
  actions (MUST)
- Record whether alerting detected the incident in time; where it did not,
  add or tune an alert as a corrective action — a review that found no
  detection gap adds none
- Track corrective actions to completion (MUST) — not just document them
