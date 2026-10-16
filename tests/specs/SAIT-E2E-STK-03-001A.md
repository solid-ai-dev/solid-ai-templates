---
id: SAIT-E2E-STK-03-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567818
title: Full interview produces a correct CLAUDE.md for a Django project
product: sait
type: e2e
area: STK
priority: p1
status: ready
environment: [local]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [e2e, output, django, python]
---

## Short description

> **Given** `INTERVIEW.md` and `stack/python-django.md` are attached to an agent
> **When** the agent conducts the interview with a defined set of answers
> **Then** the agent produces a `CLAUDE.md` containing Django-specific rules
> alongside base and python-service rules

## Results

| Result | Condition |
|--------|-----------|
| PASSED | Output contains Django-specific rules (ORM, migrations, DRF, admin, pytest-django); base rules present; python-service rules present |
| FAILED | Django-specific rules absent; output indistinguishable from a generic Python service |
| SKIPPED | No agent available |
| BLOCKED | `SAIT-INT-TPL-01-001A` is failing |
| ERROR | Agent fails to load template files or produce output |

## Steps

### Prerequisites

- Repository cloned locally
- Claude Code available

### Setup

1. Open Claude Code
2. Attach `INTERVIEW.md`, `stack/python-django.md`, `core/agents.md`
3. Interview answers:
   - Project name: CatalogService
   - Framework: Django 5.x + DRF
   - Database: PostgreSQL via Django ORM
   - Auth: JWT via djangorestframework-simplejwt
   - Output: CLAUDE.md

### Execution

1. Ask the agent to run the interview and generate `CLAUDE.md`
2. Provide the prepared answers

### Assertions

1. Assert `## Stack` lists Django 5.x, DRF, pytest-django
2. Assert ORM rules present (no raw SQL, use select_related/prefetch_related)
3. Assert migration rules present (commit every migration, never edit applied)
4. Assert authentication section references `djangorestframework-simplejwt`
5. Assert testing section references `@pytest.mark.django_db`
6. Assert base git conventions present

### Teardown

1. Delete generated `CLAUDE.md`

## Related

- Related procedures: `SAIT-E2E-STK-01-001A`