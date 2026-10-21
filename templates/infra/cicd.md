# Base — CI/CD and Delivery

[ID: base-cicd]

## Principle

Every project MUST have an automated pipeline. No manual steps between a
merged PR and a deployed artifact — humans approve, machines execute.

## Quality gates

- Stages 2–4 (lint, test, security scan) run the project's own gates.
  Which gates run, and at which thresholds, is the project's choice
- Each gate reports what it inspected, and fails on an empty or
  implausibly small input rather than passing over nothing

## Patterns

- Use gate job, path filtering, fan-out/fan-in, artifact promotion,
  caching, matrix builds, auto-merge, and deploy preview patterns
- Build every image the project ships in the pipeline, never by hand

## Pipeline stages

A pipeline MUST include, in order:

1. **Build** — compile or package the application
2. **Lint / format check** — fail on style violations
3. **Test** — run unit and integration tests; fail on any failure
4. **Security scan** — SAST, secret detection, SCA
5. **Package** — build the deployable artifact (container image, binary,
   package)
6. **Deploy to staging** — automated deployment to a staging/QA environment
7. **DAST** — automated security scan against the running staging environment
8. **Deploy to production** — triggered manually or on a release tag

Each stage MUST fail fast — a failed stage stops the pipeline immediately.

## Triggers

- Every push to a feature branch: run stages 1–4
- Every merge to `main`: run all stages through staging deployment
- Every release tag: run full pipeline through production deployment

## Environment separation

- MUST maintain at least three environments: development, staging, production
- Never test against production — staging MUST mirror production as closely
  as possible
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
- Trigger deploys with a post-publish hook — after the artifact is
  published, the pipeline SHOULD trigger the deploy by sending the
  artifact's immutable reference (image digest or tag) to the deploy
  target, never rebuilding in the deploy step. This guarantees the
  deployed artifact is the exact one that passed the gates (see
  "Promote the same artifact" under Environment separation)
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
