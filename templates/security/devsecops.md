# Base — DevSecOps

[ID: base-devsecops]

Surface vulnerabilities and legal exposure during development, in every
build, review and release, never after deployment.

## Dependency hygiene

- Keep dependencies up to date, and remove unused ones promptly
- Pin each third-party CI step to an immutable reference, such as a
  commit SHA, never to a tag that can move

## Licence compliance

- Verify a dependency's licence before adding it
- Get explicit approval before using a copyleft licence such as GPL or
  AGPL
- Document and justify every dependency with a non-standard or ambiguous
  licence
- Track every dependency's licence over time, not only when it is added
  (MUST)
- Ship a third-party notice file inside every artifact that redistributes
  dependencies, such as an image, bundle, installer or fat jar
- Guard the notice with a test that derives the required entries from the
  dependency manifest

## Secret detection

- Run secret detection in CI, and reject any commit carrying credentials,
  tokens or API keys automatically (MUST)
- Scan the full history from a full-depth checkout, not only the tip
  (MUST)
- Run the scanner as a pre-commit hook as well as in CI
- Never put a sensitive value in a commit message, an issue or pull
  request comment, or documentation (MUST NOT)
- Never write a runtime secret to disk or commit it; read it from a
  secret store (MUST NOT)

## SAST

- Run a static security analysis step in every pipeline run (MUST)
- Stop the build on a failed scan until each finding is fixed or formally
  accepted as a false positive (MUST)
- Document every accepted false positive with a written justification
  (MUST)

## IaC scanning

- Scan all infrastructure code (Terraform, Dockerfiles, Helm charts,
  Kubernetes manifests) for misconfigurations in CI (MUST)
- Fail the build on a failed IaC scan, as for SAST (MUST)
- Configure the scanner's policies to cover the project's security
  requirements
- Review IaC findings in the pull request that introduces the change
  (MUST)

## SCA

- Track every dependency for known vulnerabilities (MUST)
- Run SCA on every deployment and every release (MUST)
- Block the merge on a finding in a dependency the project declares
  (MUST)
- Block a fixable critical or high finding in an artifact you ship, such
  as a container image (MUST)
- Report an unfixable finding in a layer you do not control, such as a
  base image, with an SBOM, without blocking
- Keep a scan that runs only on a tag or release job advisory, and off the
  deploy's dependency path

## SBOM

- Generate a software bill of materials per release (MUST)
- Describe what a consumer installs, not what CI built with: install the
  artifact into a clean environment and scan that (MUST)
- Match each SBOM package and version to the delivered package and its
  expected runtime dependency set before attaching it (MUST)
- Generate it reproducibly where the tool supports it, so anyone can
  rebuild the SBOM for a tag and compare it byte for byte
- Attach it to the per-tag release record, never only to a CI artifact
  that expires
- Upload it from a non-blocking job that tolerates a missing release or
  SBOM, so a scan failure never blocks or erases the release

## DAST

- Run DAST after every staging or QA deployment, and complete it before
  promoting that build to production (MUST)
- Never run DAST against production (MUST NOT)
- Block the release on a critical finding, and treat it as an incident
  (MUST)
- Track lower-severity findings to resolution within a defined timeframe
  (MUST)
