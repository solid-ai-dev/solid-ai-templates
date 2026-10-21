# Base — CI/CD and Delivery

[ID: base-cicd]

## Principle

Every project MUST have an automated pipeline. No manual steps between a
merged PR and a deployed artifact — humans approve, machines execute.

## Quality gates

- The lint, test and security-scan stages run the project's own gates.
  Which gates run, and at which thresholds, is the project's choice
- Each gate reports what it inspected, and fails on an empty or
  implausibly small input rather than passing over nothing

## Patterns

- Select the patterns the project's workflow needs (MAY): gate job, path
  filtering, fan-out/fan-in, artifact promotion, caching, matrix builds,
  auto-merge, deploy previews
- Build every image the project ships in the pipeline, never by hand

## Pipeline stages

- Build, lint, test and security-scan (SAST, secret detection, SCA) every
  change before it merges (MUST)
- Package the deployable artifact once, after those stages pass; every
  later stage uses that artifact
- Fail fast: a failed stage stops the pipeline (MUST)
- Scan the running application (DAST) before a build reaches production
- Deploy to production only from a revision that passed every stage
- The stage count, their order beyond these and the deploy trigger are the
  project's choice

## Environment separation

- Never test against production; test in an environment that mirrors it
- Environment-specific configuration injected via environment variables —
  never baked into the artifact
- Promote the same artifact through environments — never rebuild per environment

## Infrastructure as code

- All infrastructure MUST be defined in code (Terraform, Pulumi, etc.)
- No manual changes to any environment — all changes go through the pipeline
- IaC changes follow the same review process as application code
- Destroy and recreate environments from IaC to verify correctness periodically

## Deployment strategy

- MUST support zero-downtime deployments — use rolling updates or blue/green
- MUST have a documented and tested rollback procedure
- Health check endpoint MUST return healthy before traffic is routed to a
  new instance
- Deploy small and often — large infrequent deployments increase risk
- Deploy the artifact by its immutable reference, an image digest or tag
  (SHOULD); never rebuild it in the deploy step
- A deploy step whose secret (a deploy-hook URL or token) is absent on
  forks or contributor branches MUST skip and still succeed, keeping the
  workflow green rather than hard-failing

## Release record

On a release tag, the pipeline MUST create a durable release record on
the forge, not only publish artifacts. The release job:

- runs only on tag pushes, so a manual run on a branch is skipped
- is **independent** of the publish/deploy jobs — the record captures
  the source at the tag; an artifact hiccup MUST NOT erase it
- is **idempotent** — skip if the record already exists, so a re-run
  is safe
- holds write permission at **job** scope only

## Pipeline as code

- Pipeline definitions MUST live in the repository alongside the application
  code
- Pipeline changes follow the same review process as application code
- Shared pipeline logic MUST be extracted into reusable templates — never
  copy-paste pipeline stages across repositories
