---
id: SAIT-INT-TPL-07-001A
title: EXTEND sections do not duplicate parent rules
product: sait
type: integration
area: TPL
priority: p2
status: ready
environment: [local, ci]
automatable: yes
created: 2026-05-06
author: Branimir Georgiev
product-version: "2.x"
tags: [extend, duplication, similarity]
---

## Short description

> **Given** all template files are present
> **When** every `[EXTEND: <parent-id>]` section's bullet points are compared
> against the parent section's bullet points using Jaccard word similarity
> **Then** no child bullet has >= 0.7 similarity to any parent bullet

## Results

| Result | Condition |
|--------|-----------|
| PASSED | No child bullet exceeds the similarity threshold against any parent bullet |
| FAILED | One or more child bullets are near-duplicates of parent rules |
| SKIPPED | PyYAML not installed |
| ERROR | File system is inaccessible |

## Steps

### Prerequisites

- Repository cloned locally
- `pyyaml` installed

### Setup

1. Build an ID-to-file map from all template files

### Execution

1. For each `[EXTEND: <parent-id>]` directive, extract bullet points
   from the child section and the parent section
2. For each child bullet, compute Jaccard word similarity against
   each parent bullet (words = lowercase tokens of 3+ characters)
3. Flag any pair with Jaccard >= 0.7

### Assertions

1. Assert no flagged pairs exist

### Teardown

None.

## Related

- Context: issue #284, discovered via #275
- Complements: `SAIT-SMK-TPL-04-001A` (ID existence)
- Complements: `SAIT-INT-TPL-06-001A` (chain reachability)
