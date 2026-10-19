---
id: SAIT-INT-MNF-01-001A
uuid: a1b2c3d4-e5f6-7890-abcd-ef1234567806
title: All manifest entries reference valid file paths and depend on valid IDs
product: sait
type: int
area: MANIF
priority: p0
status: ready
environment: [local, ci]
automatable: yes
created: 2026-03-22
author: Branimir Georgiev
product-version: "1.x"
tags: [manifest, consistency, dependency-graph]
---

## Short description

> **Given** the repository is cloned and `manifest.yaml` is present
> **When** every entry in `manifest.yaml` is validated against the file system
> and against other entries in the manifest
> **Then** every `file:` path resolves to an existing file and every ID in
> every `depends_on:` list matches a declared `id:` elsewhere in the manifest

## Results

| Result | Condition |
|--------|-----------|
| PASSED | All `file:` paths exist; all `depends_on` IDs resolve to a declared `id:` in the manifest; all IDs are unique |
| FAILED | One or more `file:` paths do not exist; or one or more `depends_on` IDs have no matching declaration; or duplicate IDs exist |
| SKIPPED | `manifest.yaml` is absent from the repository |
| BLOCKED | `SAIT-SMK-SYS-01-001A` is failing |
| ERROR | YAML parser fails; file system is inaccessible |

## Steps

### Prerequisites

- Repository cloned locally
- Shell with a YAML-capable tool (`python3 -c "import yaml"` or `yq`)

### Setup

1. Change to the repository root
2. Confirm `manifest.yaml` is present

### Execution

1. Extract all declared IDs from the manifest:
   ```bash
   python3 -c "
   import yaml
   m = yaml.safe_load(open('manifest.yaml'))
   ids = []
   for section in m.values():
       if isinstance(section, list):
           for entry in section:
               ids.append(entry['id'])
   print('\n'.join(ids))
   "
   ```
2. Extract all `file:` paths and check they exist:
   ```bash
   python3 -c "
   import yaml, os
   m = yaml.safe_load(open('manifest.yaml'))
   for section in m.values():
       if isinstance(section, list):
           for entry in section:
               path = entry.get('file','')
               exists = os.path.exists(path)
               print(f'{\"OK\" if exists else \"MISSING\"}: {path}')
   "
   ```
3. Extract all `depends_on` references and cross-check against declared IDs:
   ```bash
   python3 -c "
   import yaml
   m = yaml.safe_load(open('manifest.yaml'))
   ids = set()
   refs = []
   for section in m.values():
       if isinstance(section, list):
           for entry in section:
               ids.add(entry['id'])
               for dep in entry.get('depends_on', []):
                   refs.append((entry['id'], dep))
   for src, dep in refs:
       if dep not in ids:
           print(f'DANGLING: {src} depends on {dep} (not declared)')
   "
   ```

### Assertions

1. Assert no `MISSING` lines appear in the file path check
2. Assert no `DANGLING` lines appear in the depends_on cross-check
3. Assert no duplicate IDs appear in the extracted ID list

### Teardown

— (read-only check, no teardown required)

## Notes

The three scripts above can be combined into a single validation script
and added to CI as a pre-merge check.

## Related

- Related procedures: `SAIT-SMK-SYS-01-001A`, `SAIT-SMK-SYS-02-001A`
- Implements: SPEC.md §Inheritance model, manifest.yaml
