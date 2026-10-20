---
id: SAIT-SMK-ADR-01-001A
uuid: b1c2d3e4-f5a6-7890-abcd-ef1234567890
title: ADR frontmatter matches the ADR-010 schema
product: sait
type: smoke
area: ADR
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-06-02
author: Branimir Georgiev
product-version: "2.x"
tags: [adr, frontmatter, governance, schema]
---

## Short description

> **Given** the repository is cloned and all files under `docs/decisions/`
> matching `NNN-*.md` are present
> **When** each file's YAML frontmatter is parsed
> **Then** the frontmatter conforms to the schema introduced in
> `docs/decisions/010-adr-governance.md` — `id`, `status`, `date`,
> `category`, `supersedes`, and `superseded_by` are all present, valid,
> and internally consistent

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every `docs/decisions/NNN-*.md` file has frontmatter that satisfies all 8 rules below |
| FAILED | Any ADR violates one or more rules (specific failure named in the diagnostic) |
| SKIPPED | PyYAML is not installed |
| BLOCKED | — |
| ERROR | File system is inaccessible |

## Rules enforced

For every file in `docs/decisions/` matching the pattern `NNN-*.md`
(where `NNN` is 3 digits and the rest is kebab-case):

1. **Frontmatter present** — file begins with `---` … `---` block that
   parses as a YAML mapping
2. **id is a quoted string matching the filename** — `id: "NNN"` where
   `NNN` matches the leading digits of the filename. MUST be a string
   so YAML 1.1 does not parse leading-zero values as octal (e.g. `010`
   as integer 8). Unquoted integer ids fail with an explicit "quote it
   as `NNN`" diagnostic
3. **status in closed set** — one of `Proposed`, `Accepted`,
   `Superseded`, `Rejected`, `Withdrawn`
4. **date in YYYY-MM-DD form** — must match `\d{4}-\d{2}-\d{2}`
5. **category in closed set** — one of `composition`, `templates`,
   `tooling`, `process`, `release`
6. **supersedes and superseded_by present as lists** — empty lists
   allowed; missing field or non-list type fails
7. **Reciprocal-link consistency** — if ADR-X lists ADR-Y in
   `supersedes`, then ADR-Y MUST list ADR-X in `superseded_by`, and
   vice versa
8. **Status-link consistency** — if `superseded_by` is non-empty,
   `status` MUST be `Superseded`

`docs/decisions/template.md` and any non-numbered files are skipped.

## Steps

### Prerequisites

- Repository cloned locally
- PyYAML installed (`pip install pyyaml`)

### Setup

1. Change to the repository root

### Execution

1. Run the smoke runner:
   ```bash
   py tests/run.py smoke ADR-01
   ```

### Assertions

1. Assert exit code 0 and no failures reported for ADR-01

### Teardown

— (read-only check, no teardown required)

## Notes

ADR-010 (`docs/decisions/010-adr-governance.md`) introduced the schema
with three statuses; the status set gained `Rejected` and `Withdrawn` in
issue #1901. Where the two differ, this check and the rules above govern,
and ADR-010 stands as history (`AGENTS.md`, "Decision records").

The `id: "NNN"` quoting requirement is not in ADR-010's prose body
(which is immutable per the rule it defines) but is documented in
`docs/decisions/template.md` and enforced by this check. Future ADR
authors who copy template.md get the quoting right by default.

## Related

- Origin of the schema: `docs/decisions/010-adr-governance.md`
- Canonical example: `docs/decisions/template.md`
- Related procedures: `SAIT-SMK-SYS-02-001A` (similar schema-enforcement
  pattern for `[ID: ...]` declarations)
