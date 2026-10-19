# 11. Risks and technical debt

## 11.1 Risks

| # | Risk | What it looks like | Mitigation in place |
|---|------|--------------------|---------------------|
| R01 | Attention dilution | Relevant rules are buried even when the window holds the chain | Context tiers (SYS-16); the template-quality ratchet |
| R02 | Literalism | Hundreds of MUSTs drive overengineering or irrelevant work | Rule language reserves MUST for what matters; the scorer flags long rules |
| R03 | False confidence | Green structural checks read as evidence that agents do better | Chapter 10 keeps effectiveness separate; the benchmark measures it |
| R04 | Recursive governance | Rules about checks, audits and releases create more surfaces than they retire | A decision record is owed only for the composition model |
| R05 | Backlog exhaustion | The tracker becomes an inventory, not a set of commitments | Intake dispositions; only a milestone means scheduled |
| R06 | Product displacement | Keeping policy consistent takes the time meant for adopters | — |
| R07 | Supply chain | Remote policy changes behaviour without review | Consumers pin a fork version and adopt changes deliberately |
| R08 | Overcompression | A shorter file drops load-bearing policy | Compression is judged on agent outcomes, not bytes |
| R09 | Lost downstream learning | Consumer observations are discarded instead of weighed | Issue forms ask for the outcome and evidence |

## 11.2 Technical debt

| Area | Debt |
|------|------|
| Policy | Oversized high-reach templates; too many absolute rules; local incidents generalised globally; procedures mixed into persistent policy. The five lowest-scoring `core/` files are #2024 |
| Composition | File paths act as identity; merging and conflict handling depend on the agent, not a tool |
| Validation | Extensive structural checks, thin evidence that agents follow the rules |
| Documentation | Large audit and journal surfaces; ADR density out of proportion to product capability |
| Product | No installed generator, no stable project configuration, no upgrade or diff workflow; the declaration block is a target (chapter 6) |

## 11.3 What the evidence does not cover

The benchmark has run one web application, built in one session, by
strong and weak models. Thin specifications, cheaper models and many
sessions over months are only partly tested, and no round has compared a
reference-only file with a hybrid one. Rounds and their limits are in
`docs/audits/`.
