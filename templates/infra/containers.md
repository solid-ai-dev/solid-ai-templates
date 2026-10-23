# Base — Containers
[ID: base-containers]

## Dockerfile conventions

- Use official, minimal base images (e.g. `alpine`, `slim`, `distroless`)
- Pin base images to a specific version tag; never use `latest`
- Use multi-stage builds: build in one stage, copy only the final artifact
  into a minimal runtime image
- Exclude dev dependencies, build tools, and test files from the final image
- Make each `RUN` instruction do one logical thing (SHOULD)
- Chain related commands with `&&` to minimise layers (SHOULD)
- Copy only what is needed; use `.dockerignore` to exclude everything else

## Runtime security

- Run containers as a non-root user (MUST): create and switch to a
  dedicated application user in the Dockerfile
- Set the filesystem to read-only where possible (`--read-only`)
- Never run containers in privileged mode unless absolutely required and
  explicitly justified
- Drop all Linux capabilities and add back only those required
- Do not store secrets in environment variables baked into the image;
  inject them at runtime from a secret vault

## Resource management

- Define CPU and memory limits for every container, and requests where
  the orchestrator schedules by them (MUST)
- Set requests to the typical workload; set limits to the safe maximum
- Never set memory limit lower than memory request
- Monitor resource usage and adjust limits based on observed behaviour;
  do not guess

## Image hygiene

- Scan all images for vulnerabilities in CI before pushing to a registry
- Never push an image with **fixable** critical or high vulnerabilities
  to staging or production
- Treat an unfixable upstream or base-layer CVE as advisory, not a
  release blocker; publish it with an SBOM
- Tag images with the git commit SHA or release version; never rely on
  mutable tags in staging or production
- Remove unused images from the registry regularly
- Put a redistributed dependency's licence notice at a stable path a bind
  mount cannot shadow, such as `/licenses/`, after the dependency layer

## Runtime version coherence

The base image pins the runtime version that ships, and the packaging
floor declares the oldest one supported; a bump that no CI job follows
ships a runtime no gate tested.

- Run a CI job on the runtime version the base image tag or digest ships
  (MUST)
- Run a CI job on the packaging metadata floor (`requires-python`,
  `engines`, equivalent) where it differs from the base image (MUST)
- Set the static type-checker's target version to the packaging floor
- Add jobs for other supported versions as a compatibility matrix (MAY)
- Move a version in one coordinated change
- Reject a base-image or floor bump that no CI job runs; what is tested
  MUST be what ships

## Docker Compose (if applicable)

Use a Compose file when one image is not enough: several services, such
as an app with its datastore, or a toolchain impractical to install on the
host.

- Define each service, its image or build context, ports, and
  dependencies (`depends_on`) in the Compose file
- Keep the Compose file at the repo root alongside the `Dockerfile`
- Run `docker compose build` then `docker compose run --rm <service>`
  (or `up`) for local dev
- Pass `--rm` to clean up the one-off container, so repeated runs do not
  accumulate stopped containers
- Bind-mount the source for local dev so edits are live without a rebuild
- Do NOT bind-mount in CI or production; there the image is the artifact,
  and a mount would shadow it with host files
- Use Compose to orchestrate local and single-host multi-service dev;
  leave the production orchestrator to the project's choice

## Orchestration (if applicable)

- Define the orchestrator's resources as code; never apply them by hand in
  production
- Route traffic to a container only after its readiness check passes (MUST)
