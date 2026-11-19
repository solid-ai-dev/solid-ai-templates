---
id: SAIT-SMK-SYS-29-001A
title: No frozen ID or path leaves the tree inside the major
product: sait
type: smoke
area: SYS
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-11-16
author: Branimir Georgiev
product-version: "3.x"
tags: [templates, compatibility, fork, frozen-surface]
---

## Short description

> **Given** the newest 3.x release tag reachable from HEAD
> **When** the manifest and every template are compared with their state
> at that tag
> **Then** every template ID, template path, section ID, core-tier member
> and task kind present there is still present, because a fork extending
> a renamed ID fails only after it merges

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every planted case yields exactly its owed findings, and no frozen element present at the baseline is missing from the tree |
| FAILED | A template ID, a template's path, a section ID in its file, the core tier or a task kind differs from the baseline |
| FAILED | A planted case or the planted repository yields findings or a refusal other than those it owes |
| FAILED | The clone is shallow, or no tag at all is reachable from HEAD |
| FAILED | No planted case was run |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | — |

## Steps

### Prerequisites

- Repository cloned with its full history and tags
- Python 3 and git

### Setup

— (operates on the working tree and the newest `v3.*` tag reachable from
HEAD, the baseline SYS-24 reads)

### Execution

1. Compare each later side in `FROZEN_CASES` with the planted frozen
   manifest and texts, and compare the findings with those the case owes
2. Build a throwaway repository whose base commit, tagged `v3.0.0`, holds
   the planted manifest and texts, and whose HEAD renames a section ID;
   run the comparison the real run uses
3. Take the baseline: the newest tag matching `v3.<minor>.<patch>` that
   HEAD contains. With none, nothing is frozen yet
4. Read the manifest and each entry's file at the baseline and in the
   working tree, and leave out the baseline's fixture entries
5. Report each entry ID missing, each entry whose file changed, each
   `[ID:]` missing from the file that held it, a changed `core:` list and
   each task kind missing

### Assertions

1. Assert no change, an added section, template and task kind, a
   deprecated template and a renamed fixture yield no finding -- the
   controls that what chapter 8.7 allows passes
2. Assert a renamed section ID, a section moved to another file, a
   renamed template ID, a renamed template file, a template joining the
   core and a removed task kind each yield one finding naming it
3. Assert, through git, that a section ID renamed behind a `v3.0.0` tag is
   found
4. Assert no real element is missing from the tree
5. Assert the planted case count is non-zero, per ADR-034

### Negative controls

1. **The defect that motivated the check.** Renaming a section ID that
   only a fork extends passed upstream smoke and fork sync; the fork failed
   only after merging. Renaming `base-git` in `core/git.md` now fails here
2. **A deprecation.** An entry marked `deprecated` keeps its ID and file,
   so it passes; a check that read deprecation as removal would block
   what chapter 8.8 prescribes

## Related

- The spec, chapter 8.7, "Frozen surface"
- The spec, chapter 8.8, "Deprecation"
- ADR-051 -- IDs and paths are frozen inside a major
- SYS-24, which checks that a new ID splits no frozen section
