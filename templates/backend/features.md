# Backend — Feature Flags
[ID: backend-features]

## Purpose

A flag decouples deployment from release: code ships disabled, and the flag
decides when and for whom it activates.

- Use a flag for a progressive rollout, an A/B experiment, a kill switch
  for a risky change, or incomplete work deployed in steps
- Never use flags as permanent configuration; they are a temporary release
  mechanism
- Keep an ops kill switch for as long as its subsystem runs; it is the one
  permanent flag

## Rules

- Give every flag an owner at creation
- Give every flag but a kill switch a removal date; never merge one
  without it
- Give a kill switch a review date instead, and test that it still
  disables its subsystem
- Remove the flag and its dead branch as soon as the rollout completes
- Never nest flags; one gated on another creates untestable combinations
- Keep the flagged path small: wrap the decision point, not the function
- Evaluate flags at runtime, not at startup
- Never cache a flag value beyond one request unless the evaluation cost is
  measured and justified

## Flag types

| Type | Controls | Example |
|------|----------|---------|
| **Release** | Whether a feature is visible at all | New checkout flow for 0% → 100% of users |
| **Experiment** | Which variant a user sees | Button colour A vs B |
| **Ops / kill switch** | Emergency disable of a subsystem | Disable background sync |
| **Permission** | Access for a specific user, role, or tenant | Beta access for select accounts |

## Targeting and rollout strategy

- Roll out by percentage of requests or users, raising it while watching
  error rate and latency
- Target cohorts (user IDs, tenant IDs, roles) before a general rollout
- Enable a canary instance or region before expanding
- Keep each user on one variant for an experiment's duration: hash the
  user ID, never draw per request

## Evaluation

- Evaluate a flag at the feature's entry point, never deep inside domain
  logic
- Return the same response shape in both flag states
- Treat the flag-off path as the production default until the rollout is
  complete and the flag is removed

## Observability

- Log the flag name and evaluated variant on every flagged request, as
  structured properties
- Emit error rate and latency per variant, to catch a regression the new
  path introduces
- Alert if flag evaluation fails, and apply the flag's declared failure
  policy — never fall silently to a variant the policy does not name

## Tooling

- Serve flags from a flag service or SDK, or from configuration the
  application reloads at runtime; never from the application database
- Keep a flag's targeting rules in one place, never split across
  environment variables and code
- Declare each flag's failure policy for a provider outage: the safe
  default, or refusing traffic where the provider is a deliberate required
  dependency
