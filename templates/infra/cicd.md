# Base — CI/CD and Delivery
[ID: base-cicd]

## Principle

Every project MUST have an automated pipeline. No manual steps between a
merged PR and a deployed artifact — humans approve, machines execute.

## Quality gates

- Run the project's own gates in the lint, test and security-scan stages
- Treat which gates run, and at which thresholds, as the project's choice
- Make each gate report what it inspected
- Fail a gate on an empty or implausibly small input rather than pass over
  nothing

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
- Treat the stage count, their order beyond these and the deploy trigger as
  the project's choice

## Environment separation

- Never test against production; test in an environment that mirrors it
- Inject environment-specific configuration via environment variables;
  never bake it into the artifact
- Promote the same artifact through environments — never rebuild per
  environment

## Infrastructure as code

- Define all infrastructure in code (MUST) — Terraform, Pulumi or similar
- Never change any environment by hand; route all changes through the
  pipeline
- Put IaC changes through the same review process as application code
- Destroy and recreate environments from IaC to verify correctness
  periodically

## Deployment strategy

- Support zero-downtime deployments (MUST); use rolling updates or
  blue/green
- Document and test a rollback procedure (MUST)
- Route traffic to a new instance only after its health check endpoint
  returns healthy (MUST)
- Deploy small and often — large infrequent deployments increase risk
- Deploy the artifact by its immutable reference, an image digest or tag
  (SHOULD); never rebuild it in the deploy step
- Skip a deploy step whose secret (a deploy-hook URL or token) is absent on
  forks or contributor branches, and let it succeed (MUST); this keeps the
  workflow green rather than hard-failing

## Release record

On a release tag, the pipeline MUST create a durable release record on
the forge, not only publish artifacts. For the release job:

- Run it only on tag pushes, so a manual run on a branch is skipped
- Keep it **independent** of the publish/deploy jobs — the record captures
  the source at the tag
- Never let an artifact hiccup erase the release record (MUST NOT)
- Make it **idempotent** — skip if the record already exists, so a re-run
  is safe
- Grant it write permission at **job** scope only

## Pipeline as code

- Keep pipeline definitions in the repository alongside the application
  code (MUST)
- Put pipeline changes through the same review process as application code
- Extract shared pipeline logic into reusable templates (MUST); never
  copy-paste pipeline stages across repositories
