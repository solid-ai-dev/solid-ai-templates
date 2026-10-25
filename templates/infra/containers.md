# Base — Containers
[ID: base-containers]

## Image build

- Use official, minimal base images (e.g. `alpine`, `slim`, `distroless`)
- Pin base images to a specific version tag; never use `latest`
- Use multi-stage builds: build in one stage, copy only the final artifact
  into a minimal runtime image
- Exclude dev dependencies, build tools, and test files from the final image
- Copy only what is needed; exclude everything else with the build's ignore
  file, such as `.dockerignore`

## Runtime security

- Run containers as a non-root user (MUST): create and switch to a
  dedicated application user in the image build
- Set the container's root filesystem to read-only; mount writable
  storage only at the paths the application writes
- Never run containers in privileged mode unless absolutely required and
  explicitly justified
- Drop all Linux capabilities and add back only those required
- Do not store secrets in environment variables baked into the image;
  inject them at runtime from a secret vault

## Resource management

- Define CPU and memory limits for every container, and requests where
  the orchestrator schedules by them (MUST)
- Set requests to the typical workload; set limits to the safe maximum
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
- Put a redistributed dependency's licence notice in the image at a path
  no mount can shadow, such as `/licenses/`

## Runtime version coherence

The base image pins the runtime version that ships, and the packaging
floor declares the oldest one supported; a bump that no CI job follows
ships a runtime no gate tested.

- Run a CI job on the runtime version the base image tag or digest ships
  (MUST)
- Run a CI job on the packaging metadata floor (`requires-python`,
  `engines`, equivalent) where it differs from the base image (MUST)
- Move a version in one coordinated change
- Reject a base-image or floor bump that no CI job runs; what is tested
  MUST be what ships

## Deployment

- Define how containers are deployed, such as the orchestrator's
  resources, as code; never apply it by hand in production
- Route traffic to a container only after its readiness check passes (MUST)
- Never bind-mount the source into a container in CI or production, where
  the image is the artifact a mount would shadow
