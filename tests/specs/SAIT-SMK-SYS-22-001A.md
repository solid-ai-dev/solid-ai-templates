---
id: SAIT-SMK-SYS-22-001A
title: A deprecation names a live replacement
product: sait
type: smoke
area: SYS
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-10-18
author: Branimir Georgiev
product-version: "3.x"
tags: [tooling, manifest, compatibility, deprecation]
---

## Short description

> **Given** a manifest entry carrying `deprecated: <replacement-id>`
> **When** smoke reads the manifest
> **Then** the field names an entry that exists and is not itself
> deprecated, because from 3.0 a template is deprecated rather than removed
> inside a major, and the field is where a project finds what replaces it

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every planted case yields the findings it owes, and no real entry names a missing or deprecated replacement |
| FAILED | A real entry's `deprecated` names no ID, an ID no entry carries, or an entry that is deprecated too |
| FAILED | A planted case yields findings other than those it owes |
| FAILED | No planted case was run |
| SKIPPED | — |
| BLOCKED | PyYAML is not installed |
| ERROR | — |

## Steps

### Prerequisites

- Repository cloned locally
- Python 3 and PyYAML

### Setup

— (operates on `templates/manifest.yaml` and the planted manifests)

### Execution

1. For each manifest in `DEPRECATION_CASES`, collect the deprecation
   findings and compare them with those the case owes
2. Collect the findings for `templates/manifest.yaml`
3. Report the planted-case count and the count of deprecated entries in the
   manifest, which may be zero

### Assertions

1. Assert a live replacement yields no finding
2. Assert a replacement no entry carries yields one finding naming it
3. Assert a replacement that is deprecated too yields one finding
4. Assert a field that is not a string yields one finding
5. Assert the real manifest yields no finding
6. Assert the planted-case count is non-zero, per ADR-034

### Negative controls

1. **A broken real deprecation.** `deprecated: base-gone` on `base-oop`
   fails with "base-oop names base-gone, which no entry carries"
2. **The second-retirement branch removed.** With the deprecated-too test
   disabled, the planted case owing that finding fails

## Related

- ADR-051 rule 5: how a deprecation is marked
- The spec, chapter 8.7, "Deprecation": the field and the CHANGELOG's `Deprecated` section
