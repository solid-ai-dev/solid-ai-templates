# Backend — Feature Flags
[ID: backend-features]

## Purpose

Feature flags decouple deployment from release. Code ships to production
disabled; the flag controls when and for whom it activates. Use them for:

- Rolling out a new feature progressively (canary, percentage, cohort)
- Running A/B experiments without a separate deployment
- Providing a kill switch for a risky change without a rollback
- Hiding incomplete work that must be deployed incrementally

Do not use feature flags as a permanent configuration system — they are a
temporary release mechanism.

## Rules

- Every flag has an owner and a removal date set at creation time — flags
  without a removal date are not allowed to merge
- Remove the flag and its dead branch as soon as the rollout is complete —
  stale flags are technical debt
- Never nest feature flags — a flag that only activates when another flag
  is also active creates untestable combinations
- Keep the flagged code path as small as possible — wrap the decision point,
  not the entire function
- Flags are evaluated at runtime, not at startup — never cache a flag value
  for longer than one request lifecycle unless the evaluation cost is measured
  and justified

## Flag types

| Type | Controls | Example |
|------|----------|---------|
| **Release** | Whether a feature is visible at all | New checkout flow for 0% → 100% of users |
| **Experiment** | Which variant a user sees | Button colour A vs B |
| **Ops / kill switch** | Emergency disable of a subsystem | Disable background sync |
| **Permission** | Access for a specific user, role, or tenant | Beta access for select accounts |

## Targeting and rollout strategy

- **Percentage rollout**: enable for N% of requests or users; increase
  gradually while monitoring error rate and latency
- **Cohort targeting**: enable for specific user IDs, tenant IDs, or roles
  before a general rollout
- **Canary**: enable for one instance or region before expanding
- Stick users to their assigned variant for the duration of an experiment —
  use a consistent hash on user ID, not a random value per request

## Evaluation

- Evaluate flags at the entry point of the feature — handler or service layer,
  never deep inside domain logic
- Return the same response shape for both flag states — diverging response
  shapes on a flag boundary creates API instability
- Treat the flag-off path as the production default until the rollout is
  complete and the flag is removed

## Observability

- Log which variant was evaluated for every flagged request — include the
  flag name and variant in the structured log properties
- Emit a metric per flag variant — track error rate and latency separately
  for each variant to detect regressions introduced by the new path
- Alert if flag evaluation fails — a broken provider must not silently
  default to the wrong variant; fail to the safe default and alert

## Tooling

- Serve flags from a flag service or SDK, or from configuration the
  application reloads at runtime; never from the application database
- Keep a flag's targeting rules in one place, never split across
  environment variables and code
- Define each flag's value when its provider is down: the safe default, or
  refusing traffic where the provider is a deliberate required dependency
