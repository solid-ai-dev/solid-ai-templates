# 11. Risks and technical debt

The risks below could make the templates cost a project more than they
return, even when the system works as designed. Each mitigation in place
rests on a requirement or a decision where one exists, and a risk with no
mitigation shows a dash.

## 11.1 Risks

| # | Risk | What it looks like | Mitigation in place | Source |
|---|------|--------------------|---------------------|--------|
| R01 | Attention dilution | Relevant rules are buried even when the window holds the chain | Context tiers (SYS-16); the template-quality ratchet | QG-02-02, QG-04-02 |
| R02 | Literalism | Hundreds of MUSTs drive overengineering or irrelevant work | Rule language reserves MUST for what matters; the scorer flags long rules | FR-01-01, QG-04-02 |
| R03 | False confidence | Green structural checks read as evidence that agents do better | Chapter 10 keeps effectiveness separate; the benchmark measures it | QG-01-02 |
| R04 | Recursive governance | Rules about checks, audits and releases create more surfaces than they retire | A decision record is owed only for the composition model | - |
| R05 | Backlog exhaustion | The tracker becomes an inventory, not a set of commitments | Intake dispositions; only a milestone means scheduled | ADR-024 |
| R06 | Product displacement | Keeping policy consistent takes the time meant for adopters | - | - |
| R07 | Supply chain | Remote policy changes behaviour without review | A project pins a released tag of upstream or a fork, and moving the pin changes no context file | FR-08-04, FR-09-03 |
| R08 | Overcompression | A shorter file drops load-bearing policy | Compression is judged on agent outcomes, not bytes | QG-02-02 |
| R09 | Lost downstream learning | Consumer observations are discarded instead of weighed | Issue forms ask for the outcome and evidence | - |

## 11.2 Technical debt

| Area | Debt | Source |
|------|------|--------|
| Policy | Oversized high-reach templates; too many absolute rules; local incidents generalised globally; procedures mixed into persistent policy | QG-04-02 |
| Composition | File paths act as identity. An agent writing an inline or hybrid file applies overrides and settles conflicts itself; only the emitter, still proposed, does it in a tool | ADR-058, proposed |
| Validation | Extensive structural checks, thin evidence that agents follow the rules | QG-01-02 |
| Documentation | Large audit and journal surfaces; decision records out of proportion to product capability | - |
| Product | The emitter runs from a clone of the templates; no stable project configuration exists, and no tool shows what a release changes in a project's files. The declaration block is a target | ADR-053, ADR-058, proposed |
