---
id: SAIT-SMK-SYS-24-001A
title: A new section ID never splits a frozen section
product: sait
type: smoke
area: SYS
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-10-25
author: Branimir Georgiev
product-version: "3.x"
tags: [templates, compatibility, fork, frozen-surface]
---

## Short description

> **Given** the newest 3.x release tag reachable from HEAD
> **When** each template is compared with its text at that tag
> **Then** every line a section held there -- a heading, a rule, a line of
> an example -- that the tree still carries sits in the same section,
> because a section runs to the next `[ID:]` and an ID inserted inside it
> shrinks what a fork's OVERRIDE replaces

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every planted case yields exactly its owed findings, and no template moves a frozen line into another section |
| FAILED | A line present at the baseline and in the tree sits under a different section ID |
| FAILED | The planted fixture exemption keeps the fixture's file or drops the template's |
| FAILED | A planted text or a planted repository yields findings or a refusal other than those it owes |
| FAILED | The clone is shallow, or no tag at all is reachable from HEAD |
| FAILED | No planted text or no planted repository was run |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | — |

## Steps

### Prerequisites

- Repository cloned with its full history and tags
- Python 3, PyYAML and git

### Setup

— (operates on the working tree and the newest `v3.*` tag reachable from
HEAD)

### Execution

1. Compare each planted text in `SPLIT_CASES` with the planted base text,
   and compare the findings with those the case owes
2. For each case in `TAG_CASES`, build a throwaway repository whose base
   commit holds the base text under the case's tags and whose HEAD inserts
   an ID above a frozen heading, and run the comparison the real run uses
3. Drop the files of manifest entries marked `fixture`, which chapter 8.7
   leaves outside the frozen surface; check the same on planted entries
4. Take the baseline: the newest tag matching `v3.<minor>.<patch>` that
   HEAD contains. With none, nothing is frozen yet
5. For each template present at the baseline, map every content line --
   any line with a letter or digit, other than a directive or a fence
   delimiter -- to the section holding it, on both sides, and report each
   line one section lost and another gained, grouped into one finding per
   pair of sections. A heading followed only by blank and directive lines
   before an `[ID:]` belongs to that ID
6. Report the planted counts, the fixture files exempt, the templates
   compared, and the baseline

### Assertions

1. Assert a section appended after the last frozen line, a reworded
   heading and a heading-like line in a fence yield no finding — the
   controls that what chapter 8.7 allows passes
2. Assert an ID inserted above a frozen heading, an ID inserted between a
   frozen heading and its rule, and a frozen heading moved under a later ID
   each yield one finding naming both IDs, the count of lines moved and
   the first of them
3. Assert, through git, that a split behind a `v3.0.0` tag is found, that a
   repository holding only an earlier major's tag finds nothing, and that a
   repository with no tag is refused
4. Assert the planted fixture entry's file is exempt and the template's
   is kept
5. Assert no real template yields a finding
6. Assert the planted counts are non-zero, per ADR-034; the templates
   compared may be zero until 3.0.0 is tagged

### Negative controls

1. **The defect that motivated the check.** Adding
   `[ID: base-git-off-limits]` inside `core/git.md` shrank `base-git` while
   smoke and fork sync stayed green. With a `v3.0.0` tag on HEAD in a
   scratch clone, the same insertion fails, naming the lines it moved
2. **A split between two rules.** A heading-only comparison passed a new
   heading and ID inserted before the last bullet of `core/git.md`, which
   moves that rule out of `base-git`. The same insertion now fails, naming
   the bullet
3. **The fixture frozen.** An ID added under the fixture's "General
   testing rules" heading failed with two findings, though the fixture is
   test input; it now passes
4. **A clone without tags.** It reads as "nothing released" and would pass
   every split; the planted tagless repository owes a refusal instead

## Related

- The spec, chapter 8.7, "Frozen surface": a minor adds a section ID only
  on new content
- The spec, chapter 8.1: a section runs from its tags to the next `[ID:]`
- ADR-051 — section IDs are frozen inside a major
