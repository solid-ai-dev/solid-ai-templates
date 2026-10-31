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
wants:

```yaml
repos:
  - repo: https://github.com/solid-ai-dev/solid-ai-templates
    rev: v3.0.0
    hooks:
      - id: find-unfenced-checks
      - id: find-bare-suppressions
```

<!-- generated:readme-hooks -->
| Hook | What it does |
|------|--------------|
| `find-unfenced-checks` | Find checks stated outside a fenced block |
| `compile-embedded-checks` | Compile the Python checks embedded in Markdown |
| `find-line-continuations` | List line continuations in embedded checks |
| `find-bare-suppressions` | Find lint suppressions that name no rule |
| `report-test-edits` | Report changes that edit an existing test |
| `check-ascii-identifiers` | Check Python identifiers are ASCII |
| `find-import-bans` | Find imports that cross a declared boundary |
| `report-off-limits-paths` | Report committed changes touching off-limits paths |
<!-- /generated:readme-hooks -->

Run them on each commit with `pre-commit install`, and in CI with
`pre-commit run --all-files`. A hook that finds nothing to check prints
`not applicable: <reason>` and passes; read it as nothing checked, not as
a pass. `templates/core/quality-gates.md` describes each hook's arguments.

## Documentation

| Read | For |
|------|-----|
| [Migrating from 2.x](docs/migrating-to-v3.md) | Moving a 2.x project or fork to 3.0 |
| [Specification](docs/spec.md) | How the templates compose: goals, building blocks, rules, quality, risks |
| [Adapt the rules](docs/playbook.md#sync-with-upstream-as-a-fork) | Fork the templates and keep your changes across updates |
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
