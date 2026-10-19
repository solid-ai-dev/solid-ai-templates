# SOLID-AI Templates

Composable rule templates that an AI coding agent reads to write a
project's `AGENTS.md` and `CLAUDE.md`. Your team's conventions live in one
place and reach every agent on every project.

> **3.0 is the shared engine only.** Stacks, platforms, the process layer
> and the interview live in forks. Coming from 2.x:
> [Migrating to v3](docs/migrating-to-v3.md).

## Use it

- **Use a fork.** [imbra-ai-templates](https://github.com/Imbra-Ltd/imbra-ai-templates)
  carries stacks, platforms and the interview; its README shows how to hand
  them to your agent.
- **Fork it.** Carry your own stacks and process, and stay current by
  merging upstream: [Sync with upstream as a fork](docs/playbook.md#sync-with-upstream-as-a-fork).
- **Build a chain by hand.** Load every file in the `core:` list of
  `templates/manifest.yaml`, then your template and its `[DEPENDS ON]` tree.
  With Python and PyYAML, `python3 tools/resolve.py <root> --concat` does it.
- **Take updates selectively.** A new tag adopts nothing by itself:
  [Adopt a template policy update](docs/playbook.md#adopt-a-template-policy-update).

## Does it help?

Measured, not assumed, and so far mixed: in round 4 of the efficacy
benchmark, a 39-line hand-written file did best, and with a weaker model
every template-generated file lowered the hidden-test pass rate.
[The round-4 report](docs/audits/2026-10-17-round-4.md) has every figure.

## Documentation

| Read | For |
|------|-----|
| [Specification](docs/spec.md) | How the templates compose: goals, building blocks, rules, quality, risks |
| [Changelog](CHANGELOG.md) | What changed in each release |
| [Contributing](CONTRIBUTING.md) | Setup, and what a change must carry |
| [Playbook](docs/playbook.md) | Step-by-step procedures |
| [Decisions](docs/decisions/) | Why the design is what it is |
| [Security](SECURITY.md) | Reporting a vulnerability |
| [Issues](https://github.com/solid-ai-dev/solid-ai-templates/issues/new/choose) | Defects, proposals, questions |

## License

[CC BY 4.0](LICENSE). Use, share and adapt the templates for any purpose,
including commercial use, with attribution.

## Author

[Branimir Georgiev](https://github.com/braboj) — [Imbra.io](https://imbra.io)
