# Backend — Monitoring
[ID: backend-monitoring]
[DEPENDS ON: templates/backend/observability.md]

## Key metrics
Every service MUST monitor at minimum:

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
- Thresholds MUST be derived from observed behaviour over time — MUST NOT
  be set to arbitrary round numbers without a measurement baseline
- Every P1 and P2 failure scenario MUST have a corresponding alert defined
  before the service is promoted to production
- Alerts MUST be actionable — every alert must have a clear response procedure

### Example thresholds
- CPU > 75% sustained for 10 minutes → alert
- Response time p95 > 500ms sustained over 50 requests in 2 minutes → alert
- Disk usage > 90% sustained for 15 minutes → alert
- Error rate > 1% sustained for 2 minutes → alert

## Dashboards
- Every service MUST have a service health dashboard
- Dashboard MUST show at minimum: error rate, response time, throughput,
  and resource usage
- Dashboards MUST be defined as code — no manually created dashboards in
  shared environments
- Non-technical dashboards (business KPIs, MAU) are encouraged alongside
  technical dashboards

## Status page
- Maintain a status page for user-facing services to communicate outages
  and planned maintenance
- The status page MUST be hosted outside the primary infrastructure — it
  must remain available during an infrastructure incident
- Update the status page manually during incidents — automation is not
  recommended as it can mask or misreport the true state
- Use the status page proactively to reduce duplicate incident reports from
  affected users

## Incident response
- P1/P2 incidents MUST have a post-mortem documented after resolution
- Post-mortem MUST include: timeline, root cause, impact, corrective actions
- Record whether alerting detected the incident in time; where it did not,
  add or tune an alert as a corrective action — a review that found no
  detection gap adds none
- Corrective actions MUST be tracked to completion — not just documented
