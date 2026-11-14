# SOLID-AI Templates

AI coding agents write code whose quality varies by agent, by session
and by the context they are given. Each project writes its own agent
instructions, and over a long-running project they drift, contradict
one another and go unchecked.

SOLID-AI Templates are shared engineering rules that a tool turns into an
`AGENTS.md` and task skills for your project, so every agent and every
session works to the same standards. Made for solo developers and small
teams.

Part of [solid-ai-dev](https://github.com/solid-ai-dev), alongside
orchestrators, skills and a benchmark that measures what the rules change.

## Features

| What you get | How |
|--------------|-----|
| Same standards for every agent and session | One `AGENTS.md`, built by a tool from shared rules for testing, security, Git, CI/CD and APIs |
| Rules that keep up | Move to a newer templates release and rebuild your files; the project facts you filled in are kept |
| Checked, not only written | Some rules ship with a script that checks them; installed as [pre-commit hooks](docs/hooks.md), they stop a commit that breaks one, such as an import across a declared boundary |
| A lean context | By default, each task's procedures sit in a skill that loads only when that task starts; for an agent without skills, they go into `AGENTS.md` |
| Your own rules on top | Add stacks, platforms and process rules in a fork, and keep merging upstream's updates |

## Quick setup

Paste this into your agent, opened in your project:

```text
Clone https://github.com/solid-ai-dev/solid-ai-templates at its latest
release tag (3.0.0 or later; until 3.0.0 is tagged, clone main and pin
the commit) next to this project. List its roots with
../solid-ai-templates/tools/resolve_chain.py --roots, propose the ones
that fit this project, and wait for me to confirm.

Then build this project's AGENTS.md and skills from those roots:
../solid-ai-templates/tools/resolve_chain.py --emit . <roots>
If you read skills from a folder other than .agents/skills, add
--mirror <that folder>.

If you cannot load a SKILL.md file on demand when a task starts, add
--inline-skills, so each task's procedures go into AGENTS.md instead.

Fill the {{...}} placeholders in AGENTS.md from this repository and ask
me for any you cannot find. If your context file is not AGENTS.md, write
it so it points to AGENTS.md.

Finally, check the result and report each item: no {{ left in AGENTS.md,
the commands under Commands run, every skill in the Skills table has its
file, and your context file points to AGENTS.md.
```

Read the agent's report and the files before you commit them.

## Documentation

To use the templates in your project:

| Document | Use it to |
|----------|-----------|
| [Pre-commit hooks](docs/hooks.md) | Run the shipped checks, with or without the templates |
| [Adapt the rules](docs/playbook.md#61-sync-with-upstream-as-a-fork) | Fork the templates and keep your changes across updates |
| [Migrating from 2.x](docs/migrations/v3.md) | Move a 2.x project or fork to 3.0 |
| [Changelog](CHANGELOG.md) | See what changed in each release |

To work on the templates themselves:

| Document | Use it to |
|----------|-----------|
| [Contributing](CONTRIBUTING.md) | Set up, and learn what a change must carry |
| [Specification](docs/spec.md) | Learn how the templates compose |
| [Decisions](docs/decisions/) | Learn why the design is what it is |
| [Playbook](docs/playbook.md) | Follow a step-by-step procedure |

To report a problem:

| Document | Use it to |
|----------|-----------|
| [Issues](https://github.com/solid-ai-dev/solid-ai-templates/issues/new/choose) | Report a defect, propose a change, ask a question |
| [Security](SECURITY.md) | Report a vulnerability |

## License

[MIT](LICENSE). Use, copy and adapt the templates, tools and hooks for
any purpose, including in closed and commercial projects, keeping the
copyright and licence notice.

## Author

Written by [Branimir Georgiev](https://github.com/braboj) at
[Imbra](https://imbra.io). Imbra also offers an extended set of templates,
with stacks, platforms and process rules, on request.
