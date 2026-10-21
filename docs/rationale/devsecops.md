# Rationale: devsecops

Why the rules in `templates/security/devsecops.md` say what they say. The
template states each rule as one instruction; the reasoning is here, one
heading per section.

## Dependency hygiene

A tag can be moved to point at different code, so a step pinned to a tag
runs whatever the tag names today. A commit SHA cannot move.

## Licence compliance

Approving a licence does not discharge the obligation that attaches when the
dependency is redistributed inside an artifact handed to users; a permissive
or weak-copyleft dependency shipped that way carries an attribution duty of
its own. Hand-maintained attribution rots, which is why the notice is
derived from the manifest under test.

## Secret detection

A secret committed and later deleted still lives in old commits, so a
shallow checkout scans only the part of history that is already clean. A
pre-commit hook catches the secret before it exists in any commit at all.

## SAST

A scan that does not stop the build is a report nobody reads. An accepted
false positive without a written reason is indistinguishable from an
ignored true one.

## SCA

A licence problem merged is a legal exposure shipped; it is cheapest to
refuse at the pull request.

## Scan by actionability

The block-or-inform decision turns on one question: can the finding be
fixed before release? A vulnerable dependency you own has a fix you can
apply. A CVE in a base layer you do not control does not, and failing the
build on it blocks every release until upstream moves. A scan that runs only
on a tag cannot be tried on a pull request, so a hard failure first appears
mid-release.

## SBOM

SCA scans the dependencies for risk and gates the merge; the SBOM is the
release artifact listing those same dependencies for whoever installs the
product. They share a subject and differ in duty, so each has its own
section.

Every generator's most convenient mode reads an environment, and in CI the
environment at hand is the build environment, the one that just ran the
tests. Its SBOM names lint tools, test runners and build plugins the
consumer never installs. A misdirected SBOM is worse than none: it is
schema-valid and passes every check, and a CVE in a lint tool reads as a CVE
in the product. The tell is size: a library with no runtime dependencies has
one component, and the build-environment SBOM for one such library held
dozens. The shape is not specific to one ecosystem: a `node_modules` tree
after an install carries devDependencies, and a Go build cache carries
test-only modules.

A reproducible SBOM can be regenerated and compared byte for byte, which is
stronger provenance than an embedded timestamp. A CI artifact expires with
run retention, so the durable copy belongs on the release. The upload job
reaches forward to the release, never the reverse, so its failure cannot
undo one.

## DAST

Dynamic testing exercises a running system, so it needs one; production is
not a test target.
