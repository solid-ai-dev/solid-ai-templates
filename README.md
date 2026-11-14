# SOLID-AI Templates

AI coding agents write code whose quality varies by agent, by session
and by the context they are given. Each project writes its own agent
instructions, and they drift, contradict one another and go unchecked.

SOLID-AI Templates are shared engineering rules that a tool turns into an
`AGENTS.md` and task skills for your project, so every agent and every
session works to the same standards. Made for solo developers and small
teams.

Part of [solid-ai-dev](https://github.com/solid-ai-dev), alongside
orchestrators, skills and a benchmark that measures what the rules change.

## Features

- Rules for testing, security, Git, CI/CD and APIs, composed into your
  agent files
- Pre-commit hooks that enforce the rules a script can check, such as
  comment layout, import bans and ASCII identifiers
- Add your own stacks, platforms and process rules in a fork, and keep
  merging upstream's updates

## Quick setup

Paste this into your agent, opened in your project:

```text
Clone https://github.com/solid-ai-dev/solid-ai-templates at its latest
release tag (3.0.0 or later) next to this project. List its roots with
../solid-ai-templates/tools/resolve_chain.py --roots, propose the ones
that fit this project, and wait for me to confirm.

Then build this project's AGENTS.md and skills from those roots:
../solid-ai-templates/tools/resolve_chain.py --emit . <roots> --mirror .claude/skills
Fill the {{...}} placeholders in AGENTS.md from this repository and ask
me for any you cannot find. Write a CLAUDE.md that holds @AGENTS.md.
```

Review the files before you commit them. 3.0.0 is not tagged yet; until
it is, have the agent clone `main` and pin a commit.

## Documentation

| Read | For |
|------|-----|
| [Migrating from 2.x](docs/migrations/v3.md) | Moving a 2.x project or fork to 3.0 |
| [Specification](docs/spec.md) | How the templates compose: goals, building blocks, rules, quality, risks |
| [Pre-commit hooks](docs/hooks.md) | Run the shipped checks, with or without the templates |
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
