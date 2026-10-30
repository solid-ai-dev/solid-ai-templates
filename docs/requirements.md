# Requirements

What upstream must do, by capability, and how well, by quality goal and its
ISO/IEC 25010:2023 characteristic. Terms
are defined in the [glossary](architecture/12-glossary.md), and chapter 1
of the [specification](spec.md) gives the capabilities and quality goals.

| Convention | Rule |
|------------|------|
| IDs | `FR-<capability>-<n>` or `QG-<goal>-<n>`; cite a requirement by its ID |
| Numbering | A new requirement takes the next free number. A removed or moved ID is never reused, and the Removed table names where it went |
| Source | Where the requirement is stated today. A filled cluster moves the text here, and the source cites the ID |
| Checked by | The check that enforces it, short form; `docs/tests/index.md` gives the full ID. A dash is a gap, and "partial" names the part a check covers |

Status: skeleton. Each cluster holds a few requirements until its fill
(#2390).

## Functional requirements

### 01. Shared rules

| ID | Requirement | Source | Checked by |
|----|-------------|--------|------------|
| FR-01-01 | The system shall state each rule as a plain imperative, or with an RFC 2119 keyword where strength matters. | Chapter 8.9 | - |
| FR-01-02 | The system shall give a section an ID when something references it, unique across all templates. | Chapter 8.1 | SYS-02 |
| FR-01-03 | The system shall name another file's section in prose only where that file is in every chain carrying the rule. | Chapter 8.4 | SYS-11 |

### 02. Layers

| ID | Requirement | Source | Checked by |
|----|-------------|--------|------------|
| FR-02-01 | The system shall keep rules shared by one kind of project under `frontend/` or `backend/`, extending base templates without editing them. | Chapter 5.2 | - |
| FR-02-02 | The system shall resolve the security tier for every stack category except library and embedded. | Chapter 8.5 | SYS-15 |

### 03. Manifest

| ID | Requirement | Source | Checked by |
|----|-------------|--------|------------|
| FR-03-01 | The system shall register every template in one manifest entry, with an ID unique across all layers. | `AGENTS.md` 2.3 | SYS-03, MNF-01 |
| FR-03-02 | The system shall seed the core tier, `core:` then `fork_core:`, into every chain without a declaration. | Chapter 5.3 | - |
| FR-03-03 | The system shall reach an opt-in template only when a stack's `depends_on` names it. | Chapter 5.3 | - |
| FR-03-04 | The system shall treat the manifest's `depends_on` as authoritative where a template's dependency line disagrees with it. | Chapter 8.1 | SYS-04 |

### 04. Composition

| ID | Requirement | Source | Checked by |
|----|-------------|--------|------------|
| FR-04-01 | The system shall resolve a root to an ordered file list, base then layer then stack, depth-first and deduplicated. | Chapter 6.1 | - |
| FR-04-02 | Where several templates name one section ID, the system shall apply the higher level, in the order base, layer, stack, interview answers. | Chapter 8.2 | - |
| FR-04-03 | The system shall apply an override, then every extension of the same ID on top of it. | Chapter 8.3 | - |
| FR-04-04 | The system shall refuse a chain that overrides one ID twice. | Chapter 8.3 | TPL-10 |

### 05. Context generation

| ID | Requirement | Source | Checked by |
|----|-------------|--------|------------|
| FR-05-01 | The system shall let an agent generate a context file by reading Markdown, with no build step between the fork and the file. | Chapter 6.1 | - |
| FR-05-02 | The system shall have the agent write the file to the output contract in `templates/core/agents.md`. | Chapter 6.1 | - |
| FR-05-03 | The system shall send a conflict the rules cannot settle to the user, and record the answer in the generated file. | Chapter 8.3 | - |
| FR-05-04 | The system shall produce a context file that any agent reading Markdown can use, written to the file each agent reads. | `templates/core/docs.md`, "Output file by agent" | - |

### 06. Context file and task skills

| ID | Requirement | Source | Checked by |
|----|-------------|--------|------------|
| FR-06-01 | The system shall load a heading without a load directive on every turn, and give its subheadings its load. | Chapter 8.1, ADR-058 | - |
| FR-06-02 | The system shall load every rule of a template that guards data, credentials or authentication on every turn. | Chapter 8.1, ADR-058 | SYS-25 |
| FR-06-03 | The system shall build the root file and the skills from the resolved chain, leaving out overridden rules and the sections the project declines, and copy each remaining rule's text unchanged. | ADR-058 |SYS-26, partial, on a planted fixture |
| FR-06-04 | The system shall list each skill in the root file with the task that triggers it. | ADR-058 | SYS-26 |
| FR-06-05 | The system shall reference a section marked `check` by its command and pass condition, never by copying the script body. | ADR-058 |SYS-26, partial, on a planted fixture |
| FR-06-06 | The system shall build byte-identical files from the same input. | ADR-058 | SYS-26 |

### 07. Shipped checks

| ID | Requirement | Source | Checked by |
|----|-------------|--------|------------|
| FR-07-01 | The system shall state each mechanically checkable rule with its command in a fence and its pass condition beside it. | Chapter 8.9, ADR-031 | - |
| FR-07-02 | The system shall ship a check script over 15 lines as a hook listed in `.pre-commit-hooks.yaml`. | `AGENTS.md` 2.4, ADR-055 | - |
| FR-07-03 | The system shall have every check exit 0 on a pass, 1 on a failure and 3 when it does not apply. | Chapter 8.7 | - |

### 08. Fork extension

| ID | Requirement | Source | Checked by |
|----|-------------|--------|------------|
| FR-08-01 | The system shall let a fork stay current by merging upstream, never by copying files. | Chapter 8.6 | - |
| FR-08-02 | The system shall keep a fork's entries under `stacks:`, `platform:` and keys of its own, never under `core:`, `base:`, `backend:` or `frontend:`. | Chapter 8.6 | SYS-20 |
| FR-08-03 | The system shall let a `fork_core:` entry depend only on core-tier IDs. | Chapter 8.6 | SYS-21 |
| FR-08-04 | The system shall let a project take its rules from upstream, or from a fork for its stacks, by clone or as a submodule pinned to a released tag. | Playbook, "Vendor the templates in a project" | - |

### 09. Versioned releases

| ID | Requirement | Source | Checked by |
|----|-------------|--------|------------|
| FR-09-01 | The system shall not remove, rename or change the meaning of a frozen element in a 3.x release, except for a security fix. | Chapter 8.7, ADR-051 | SYS-24, partial, for section splitting only |
| FR-09-02 | The system shall keep a deprecated template resolving until the next major, naming a live replacement. | Chapter 8.8 | SYS-22 |
| FR-09-03 | The system shall change nothing in an existing context file when a project moves its pin. | Chapter 6.5 | - |

### 10. Self-checks

| ID | Requirement | Source | Checked by |
|----|-------------|--------|------------|
| FR-10-01 | The system shall run smoke, conformance and fork sync on every pull request and on every push to `main`. | `AGENTS.md` 3.1 | CI |
| FR-10-02 | The system shall merge each change into a simulated fork that appends a stack, and pass smoke there. | Chapter 6.4 | fork sync |

## Quality requirements

### 01. Functional suitability

| ID | Subcharacteristic | Requirement | Source | Checked by |
|----|-------------------|-------------|--------|------------|
| QG-01-01 | Functional correctness | Smoke, conformance, fork sync and the redundancy audit shall pass on `main`. | Chapter 10.1 | CI |
| QG-01-02 | Functional appropriateness | An agent given a generated file shall complete representative tasks at least as well as without one. | Chapter 1.3 | Efficacy benchmark |

### 02. Performance efficiency

| ID | Subcharacteristic | Requirement | Source | Checked by |
|----|-------------------|-------------|--------|------------|
| QG-02-02 | Resource utilization | A change that shrinks the context shall count as better only where outcomes hold. | Chapter 10.1 | - |

### 03. Flexibility

| ID | Subcharacteristic | Requirement | Source | Checked by |
|----|-------------------|-------------|--------|------------|
| QG-03-02 | Replaceability | Every release shall pass the changelog cut and SemVer step checks. | Chapter 5.6 | `check_release.py` |

### 04. Maintainability

| ID | Subcharacteristic | Requirement | Source | Checked by |
|----|-------------------|-------------|--------|------------|
| QG-04-02 | Modifiability | No template shall score below its baseline. | Chapter 10.1 | score ratchet |

### Removed

| ID | Now |
|----|-----|
| QG-02-01 | QG-01-02, when the goals took their ISO names |
| QG-03-01 | QG-02-02, when the goals took their ISO names |
| QG-04-01 | QG-03-02, when the goals took their ISO names |
| QG-05-01 | QG-04-02, when the goals took their ISO names |
