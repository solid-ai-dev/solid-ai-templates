---
id: SAIT-SMK-TPL-09-001A
title: No empty [ID:] sections
product: sait
type: smoke
area: TPL
priority: p1
status: ready
environment: [local, ci]
automatable: yes
created: 2026-05-07
author: Branimir Georgiev
product-version: "2.x"
tags: [structure, id-tag, content, quality]
---

## Short description

> **Given** the repository is cloned and all template files are present
> **When** every `[ID: ...]` tagged section in every template is checked
> **Then** each section contains at least one line of non-metadata content

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Every `[ID:]` section has content |
| FAILED | One or more `[ID:]` sections are empty |
| SKIPPED | — |
| BLOCKED | — |
| ERROR | File system is inaccessible |

## Steps

### Prerequisites

- Repository cloned locally

### Setup

1. Change to the repository root

### Execution

1. For each template file, find all `[ID: ...]` tags
2. For each tag, scan subsequent lines until the next `[ID:]` tag
3. Skip blank lines and metadata lines (`[DEPENDS ON:]`,
   `[EXTEND:]`, `[OVERRIDE:]`)
4. Check if at least one content line exists (text, bullet,
   heading, table, code block)

### Assertions

1. Assert every `[ID:]` section has at least one content line

### Teardown

— (read-only check, no teardown required)

## Notes

An empty `[ID:]` section is a placeholder that provides no rules
to the agent. Sub-headings count as content since they introduce
rule groups within the section.

## Related

- Related procedures: `SAIT-SMK-TPL-08-001A`, `SAIT-INT-TPL-02-001A`
