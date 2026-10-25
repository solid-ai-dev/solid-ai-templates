# Base — CI/CD and Delivery
[ID: base-cicd]

## Principle

- Give every project an automated pipeline (MUST)
- Leave no manual step between a merged change and a released artifact:
  humans approve, machines execute

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

## Pipeline stages

- Build, lint, test and security-scan (SAST, secret detection, SCA) every
  change before it merges (MUST)
- Package the release artifact once, after those stages pass; every later
  stage and environment uses that artifact, never a rebuild
- Build every artifact the project ships in the pipeline, never by hand
- Fail fast: a failed stage stops the pipeline (MUST)
- Never test against production
- Release only from a revision that passed every stage
- Treat the stage count, their order beyond these and the release trigger
  as the project's choice

## Infrastructure as code

- Define all infrastructure in code (MUST)
- Never change any environment by hand; route all changes through the
  pipeline
- Put IaC changes through the same review process as application code

## Deployment

- Document and test a rollback procedure (MUST)
- Deploy the artifact by an immutable reference, such as a content digest
  (SHOULD)
- Skip a deploy step whose secret is absent on a fork or contributor
  branch, and let it succeed (MUST) rather than hard-fail

## Release record

On a release tag, the pipeline MUST create a durable release record, not
only publish artifacts. For the release job:

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
