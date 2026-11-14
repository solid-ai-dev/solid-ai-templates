# Pre-commit hooks

The templates' checks ship as pre-commit hooks. A project can run them with
the templates or without them.

## Setup

1. Add this repository to `.pre-commit-config.yaml`, pinned to a release
   tag, and list the hooks you want:

   ```yaml
   repos:
     - repo: https://github.com/solid-ai-dev/solid-ai-templates
       rev: v3.0.0
       hooks:
         - id: find-unfenced-checks
         - id: find-bare-suppressions
   ```

   The hooks ship from 3.0.0, which is not tagged yet; until it is, pin a
   commit of `main` as `rev:`.

2. Run `pre-commit install`, so the commit hooks run on each commit.
3. Run `pre-commit run --all-files` in CI.

## Hooks

The template linked in each row holds the hook's rules and the arguments a
project sets.

<!-- generated:hooks-table -->
| Hook | What it does | Runs | Rules and arguments |
|------|--------------|------|---------------------|
| `find-unfenced-checks` | Find checks stated outside a fenced block | On each commit | [core/embedded-checks.md](../templates/core/embedded-checks.md) |
| `compile-embedded-checks` | Compile the Python checks embedded in Markdown | On each commit | [core/embedded-checks.md](../templates/core/embedded-checks.md) |
| `find-line-continuations` | List line continuations in embedded checks | On each commit | [core/embedded-checks.md](../templates/core/embedded-checks.md) |
| `find-bare-suppressions` | Find lint suppressions that name no rule | On each commit | [core/quality-gates.md](../templates/core/quality-gates.md) |
| `report-test-edits` | Report changes that edit an existing test | On request, after committing | [core/quality-gates.md](../templates/core/quality-gates.md) |
| `check-ascii-identifiers` | Check Python identifiers are ASCII | On each commit | [core/quality.md](../templates/core/quality.md) |
| `find-import-bans` | Find imports that cross a declared boundary | On each commit | [core/quality.md](../templates/core/quality.md) |
| `report-off-limits-paths` | Report committed changes touching off-limits paths | On request, after committing | [core/git.md](../templates/core/git.md) |
<!-- /generated:hooks-table -->

## Hooks run on request

A hook marked "On request" reads the committed change, so it runs after
committing, in CI or by hand:

```bash
pre-commit run report-test-edits --hook-stage manual --all-files
```

## Output

A hook that finds nothing to check prints `not applicable: <reason>` and
passes. Read it as nothing checked, not as a pass.
