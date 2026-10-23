# Rationale: containers

Why the rules in `templates/infra/containers.md` say what they say. The template
states each rule as one instruction; the reasoning and the worked examples
are here, one heading per section, named by ID where the section has one.

## testing-container-e2e

Hardcoding Docker and a fixed sleep breaks on rootless Podman, in CI
without Docker, and on a slow start. Ryuk and similar reapers assume a
privileged Docker. Local multi-service composition belongs to the Docker Compose
section of the same template.
