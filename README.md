# SOLID-AI Templates

Ready-made coding rules your AI agent turns into your project's
`AGENTS.md` and `CLAUDE.md`.

## Features

- Engineering standards for solo developers and small teams, like large
  companies have
- The same rules for every team member and every project
- Ready-made rules for testing, security, Git, CI/CD and APIs
- Skip, adapt or override the rules
- New rules never change your project without your say

## Quick setup

1. Fork this repository on GitHub and clone your fork.

2. List the templates, then build the one your project needs into a single
   file (Python 3 and PyYAML):

   ```bash
   pip install pyyaml
   python3 tools/resolve.py --roots                 # lists the templates
   python3 tools/resolve.py backend-api --concat > chain.md
   ```

   No Python? Give your agent the files in the manifest's `core:` list,
   then the template you picked and the files it names as dependencies.

3. Give your agent `chain.md` and `templates/core/agents.md`, and ask it to
   write `AGENTS.md` and `CLAUDE.md` for your project. Review the result
   before you commit it.

## Documentation

| Read | For |
|------|-----|
| [Specification](docs/spec.md) | How the templates compose: goals, building blocks, rules, quality, risks |
| [Changelog](CHANGELOG.md) | What changed in each release |
| [Migrating from 2.x](docs/migrating-to-v3.md) | Moving a 2.x project or fork to 3.0 |
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
