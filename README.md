# SOLID-AI Templates

Ready-made coding rules that help your AI agents make the same choices
your team would. Hand over routine coding and review to the agents, and
keep your team on design and testing.

## Features

- Engineering standards for solo developers and small teams, like large
  companies have
- The same rules for every team member and every project
- Ready-made rules for testing, security, Git, CI/CD and APIs
- Ready-made checks for the rules, run as pre-commit hooks
- Skip, adapt or override the rules
- New rules never change your project without your say

## Quick setup

1. Open your project in your agent and paste:

   ```text
   Clone https://github.com/solid-ai-dev/solid-ai-templates next to this
   project. Read its templates/manifest.yaml, propose the templates that
   fit this project, and ask me to confirm before going on.

   Then write AGENTS.md and CLAUDE.md for this project:
   - Load every file in the manifest's core: list
   - Load the chosen templates and every file their [DEPENDS ON] lines name
   - Follow templates/core/agents.md for the output
   ```

2. Review the result before you commit it.

## Use the checks only

A project can run the shipped checks without the templates. Add them to
`.pre-commit-config.yaml`, pinned to a released tag, and list the hooks it
wants. The hooks ship from 3.0.0, which is not tagged yet; until it is,
pin a commit of `main` as `rev:`.

```yaml
repos:
  - repo: https://github.com/solid-ai-dev/solid-ai-templates
    rev: v3.0.0
    hooks:
      - id: find-unfenced-checks
      - id: find-bare-suppressions
```

<!-- generated:readme-hooks -->
| Hook | What it does | Runs | Rules and arguments |
|------|--------------|------|---------------------|
| `find-unfenced-checks` | Find checks stated outside a fenced block | On each commit | [core/embedded-checks.md](templates/core/embedded-checks.md) |
| `compile-embedded-checks` | Compile the Python checks embedded in Markdown | On each commit | [core/embedded-checks.md](templates/core/embedded-checks.md) |
| `find-line-continuations` | List line continuations in embedded checks | On each commit | [core/embedded-checks.md](templates/core/embedded-checks.md) |
| `find-bare-suppressions` | Find lint suppressions that name no rule | On each commit | [core/quality-gates.md](templates/core/quality-gates.md) |
| `report-test-edits` | Report changes that edit an existing test | On request, after committing | [core/quality-gates.md](templates/core/quality-gates.md) |
| `check-ascii-identifiers` | Check Python identifiers are ASCII | On each commit | [core/quality.md](templates/core/quality.md) |
| `find-import-bans` | Find imports that cross a declared boundary | On each commit | [core/quality.md](templates/core/quality.md) |
| `report-off-limits-paths` | Report committed changes touching off-limits paths | On request, after committing | [core/git.md](templates/core/git.md) |
<!-- /generated:readme-hooks -->

Run the commit hooks on each commit with `pre-commit install`, and in CI
with `pre-commit run --all-files`. Run a hook marked on request after
committing, in CI or by hand, since it reads the committed change:

```bash
pre-commit run report-test-edits --hook-stage manual --all-files
```

A hook that finds nothing to check prints `not applicable: <reason>` and
passes; read it as nothing checked, not as a pass. The linked template
holds each hook's rules and the arguments a project sets.

## Documentation

| Read | For |
|------|-----|
| [Migrating from 2.x](docs/migrations/v3.md) | Moving a 2.x project or fork to 3.0 |
| [Specification](docs/spec.md) | How the templates compose: goals, building blocks, rules, quality, risks |
| [Adapt the rules](docs/playbook.md#61-sync-with-upstream-as-a-fork) | Fork the templates and keep your changes across updates |
| [Changelog](CHANGELOG.md) | What changed in each release |
| [Contributing](CONTRIBUTING.md) | Setup, and what a change must carry |
| [Playbook](docs/playbook.md) | Step-by-step procedures |
| [Decisions](docs/decisions/) | Why the design is what it is |
| [Security](SECURITY.md) | Reporting a vulnerability |
| [Issues](https://github.com/solid-ai-dev/solid-ai-templates/issues/new/choose) | Defects, proposals, questions |

## License

[MIT](LICENSE). Use, copy and adapt the templates and tools for any
purpose, including in closed and commercial projects, keeping the copyright
notice. Releases before 3.0.0 remain under CC BY 4.0.

## Author

Written by [Branimir Georgiev](https://github.com/braboj) at
[Imbra](https://imbra.io). Imbra also offers an extended set of templates,
with stacks, platforms and process rules, on request.
