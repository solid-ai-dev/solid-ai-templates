# Backend — Monitoring
[ID: backend-monitoring]
[DEPENDS ON: templates/backend/observability.md]

## Key metrics

Monitor at minimum, in every service (MUST):

| Metric | Why |
|--------|-----|
| CPU usage | Detect resource saturation and scaling needs |
| Memory usage | Detect leaks and container limit violations |
| Disk usage | Prevent storage exhaustion |
| Response time (p50, p95, p99) | Detect latency degradation |
| Error rate (4xx, 5xx) | Detect functional failures |
| Throughput (requests/sec) | Detect traffic spikes and capacity limits |

Add custom metrics for business-critical operations specific to the service
(e.g. orders processed, jobs queued, messages consumed).

## Thresholds and alerts

- Derive thresholds from observed behaviour over time (MUST)
- Never set thresholds to arbitrary round numbers without a measurement
  baseline (MUST NOT)
- Define a corresponding alert for every P1 and P2 failure scenario before
  the service is promoted to production (MUST)
- Make alerts actionable (MUST); give every alert a clear response procedure

### Example thresholds

- CPU > 75% sustained for 10 minutes → alert
- Response time p95 > 500ms sustained over 50 requests in 2 minutes → alert
- Disk usage > 90% sustained for 15 minutes → alert
- Error rate > 1% sustained for 2 minutes → alert

## Dashboards

- Give every service a service health dashboard (MUST)
- Show on the dashboard at minimum: error rate, response time, throughput,
  and resource usage (MUST)
- Define dashboards as code (MUST) — no manually created dashboards in
  shared environments
- Add non-technical dashboards (business KPIs, MAU) alongside technical
  dashboards (SHOULD)

## Status page

- Maintain a status page for user-facing services to communicate outages
  and planned maintenance
- Host the status page outside the primary infrastructure (MUST); it must
  remain available during an infrastructure incident
- Update the status page manually during incidents — automation is not
  recommended as it can mask or misreport the true state
- Use the status page proactively to reduce duplicate incident reports from
  affected users

## Incident response

- Document a post-mortem for every P1/P2 incident after resolution (MUST)
- Include in every post-mortem: timeline, root cause, impact, corrective
  actions (MUST)
- Record whether alerting detected the incident in time; where it did not,
  add or tune an alert as a corrective action — a review that found no
  detection gap adds none
- Track corrective actions to completion (MUST) — not just document them
