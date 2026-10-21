# Base — DevSecOps

[ID: base-devsecops]

Surface vulnerabilities and legal exposure during development, in every
build, review and release, never after deployment.

## SAST

- Run a static security analysis step in every pipeline run (MUST)
- Stop the build on a failed scan until each finding is fixed or formally
  accepted as a false positive (MUST)
- Document every accepted false positive with a written justification
  (MUST)

## SCA

- Track every dependency for known vulnerabilities and licence risks
  (MUST)
- Run SCA on every deployment to QA, staging and production (MUST)
- Never merge a dependency whose licence is unacceptable (MUST NOT)

## SBOM

- Generate a software bill of materials per release (MUST)
- Describe what a consumer installs, not what CI built with: install the
  artifact into a clean environment and scan that (MUST)
- Assert the component set before attaching the SBOM: it matches the
  declared runtime dependency closure, and a library with no runtime
  dependencies lists exactly one component (MUST)
- Generate it reproducibly where the tool supports it, so anyone can
  rebuild the SBOM for a tag and compare it byte for byte
- Attach it to the per-tag release record, never only to a CI artifact
  that expires
- Upload it from a non-blocking job that tolerates a missing release or
  SBOM, so a scan failure never blocks or erases the release

```bash
set -e -o pipefail
SBOM=<sbom.json>
count=$(jq '(.components // []) | length' "$SBOM")
echo "components: $count"
jq -r '(.components // [])[].name' "$SBOM" | sort
[ "$count" -gt 0 ]
```

Pass condition: the listed names equal the declared runtime dependency
closure, the library alone where it has none. A count of zero exits
non-zero: the document carries no components, not a product without
dependencies. A document jq cannot parse or read exits non-zero too.

## Scan by actionability

- Block the merge on findings you own: SCA over your own dependencies,
  such as `pip-audit`, `npm audit` or `govulncheck` (MUST)
- Report, without blocking, findings you cannot fix at will: image and
  base-layer scans such as Trivy or Grype, published with an SBOM
- Keep a scan that runs only on a tag or release job advisory, and off the
  deploy's dependency path
- Track the base image with a dependency bot, so an available base update
  arrives as a pull request rather than a standing finding

## Secret detection

- Run secret detection in CI, and reject any commit carrying credentials,
  tokens or API keys automatically (MUST)
- Scan the full history from a full-depth checkout, not only the tip
  (MUST)
- Run the scanner as a pre-commit hook as well as in CI
- Never put a sensitive value in anything committed, including commit
  messages, issue comments and documentation (MUST NOT)
- Fetch runtime secrets from a vault at startup; never write them to disk
  or commit them (MUST NOT)

## Licence compliance

- Verify a dependency's licence before adding it
- Get explicit approval before using a copyleft licence such as GPL or
  AGPL
- Document and justify every dependency with a non-standard or ambiguous
  licence
- Ship a third-party notice file inside every artifact that redistributes
  dependencies, such as an image, bundle, installer or fat jar
- Guard the notice with a test that derives the required entries from the
  dependency manifest

## DAST

- Run DAST against staging or QA after every deployment (MUST)
- Never run DAST against production (MUST NOT)
- Complete the automated DAST scans before any production release (MUST)
- Block the release on a critical finding, and treat it as an incident
  (MUST)
- Track lower-severity findings to resolution within a defined timeframe
  (MUST)

## IaC scanning

- Scan all infrastructure code (Terraform, Dockerfiles, Helm charts,
  Kubernetes manifests) for misconfigurations in CI (MUST)
- Fail the build on a failed IaC scan, as for SAST (MUST)
- Detect overprivileged roles, exposed ports, unencrypted storage,
  hardcoded values and `latest` image tags
- Review IaC findings in the pull request that introduces the change
  (MUST)

## Dependency hygiene

- Keep dependencies up to date, and remove unused ones promptly
- Prefer actively maintained, widely adopted dependencies
- Pin third-party CI steps to an immutable reference such as a commit SHA,
  with the version in a comment so the update bot still bumps them
