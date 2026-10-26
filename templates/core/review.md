# Base — Peer Review

[ID: base-review]

How a change is reviewed, and how a finding is proven before it is reported.

## Principle

- Peer-review all code before merging (MUST)
- Hold the reviewer accountable for what merges, and the developer for what
  they write
- Put reviews ahead of your own development; a blocked review blocks the
  team

## Priority order

[LOAD: review]

Review in this order, most critical first. `templates/core/quality.md`, and
any language quality template the project carries, is the standard for
items 2 to 4.

1. **Security**: anything exploitable, any credential or licence problem
2. **Correctness**: wrong results, unhandled failures, race conditions
3. **Clarity**: obscure names, deep nesting, high cognitive complexity,
   boolean flag parameters
4. **Conventions**: deviations from the project's agreed patterns

The order above is by area; weigh each finding separately.

- Label each finding a demonstrated defect, a deviation from a policy the
  project adopted, or a suggestion
- Block a merge only on a defect or a policy deviation; leave a
  suggestion to the author

## MUST checklist

- [ ] No credential, token or sensitive value appears in a committed file
- [ ] Every failure path is handled; no silent catch, no swallowed exception
- [ ] Every new dependency carries a licence the project's policy allows
- [ ] Significant logic and architectural decisions are documented
- [ ] Existing documentation matches the code after the change
- [ ] Every changed section was re-read whole, not only the changed line
- [ ] Every claim changed text makes about itself, such as a count or "all",
      was checked by counting with a tool
- [ ] Input from outside the process, such as a URL parameter, is
      validated as untrusted before it is destructured, indexed or used as
      a key
- [ ] A refactor preserves behaviour on every path: each case, direction and
      mode, including null handling, sort order and boundary values

## SHOULD checklist

- [ ] Each non-trivial function has a unit test per relevant variant
- [ ] Coverage does not fall
- [ ] Lint errors and warnings do not rise
- [ ] Each third-party dependency is necessary, understood and maintained
- [ ] No new abstraction without two call sites, and no new dependency
      without a documented reason

## CI signals

- Read the log of a red check before calling the pull request green or red
- Separate an infrastructure failure (the check could not run) from a diff
  failure (it ran and found something), and say which in the merge decision
- File a separate task for an infrastructure failure, and note it in the
  merge decision
- Never retry until green without saying so (MUST NOT)
- Never bypass a failing check by skipping hooks or by an admin merge
  unless the maintainer explicitly accepts the risk (MUST NOT)

## Structure audit

- Run a structure audit, which checks project completeness rather than
  changed files, after a new project setup, a framework or stack migration,
  a new major layer, and before a release milestone
- Verify every MUST in the base templates (the standard documents, a
  `.gitignore`) and in the project's layer and stack templates
- Verify each sub-clause of a MUST separately; a rule requiring examples and
  their output is two checks

## Picking up an issue

[LOAD: start-issue]

- Re-read the target for existing coverage before writing anything; an
  issue describes the tree on its filing date
- Verify everything the issue cites as existing, and run what it proposes
  against the tree before adopting it
- Check the open pull requests and the decisions accepted since the filing
  date for work that already closes or moves it
- Restate the scope before starting when it has moved since filing
- Read what a cited sibling change shipped, not what it proposed
- Resolve each cited version identifier against its source; a superseded
  one still resolves
- Treat a closed classification in the acceptance criteria as a claim:
  sort every member yourself before acting on any

  ```
  criteria: "each check runs on Linux or macOS"
  sorted:   9 Linux, 2 macOS, 1 neither -- it runs only on Windows
  ```

- Name each member that fits no branch, and the branch it fails

## Planning

- Produce a plan before implementing a feature or a non-trivial change: the
  files, the signatures or outline, the edge cases, and the assumptions
- Never write implementation code until the plan is approved (MUST NOT)
- Skip the plan for one-line fixes, typos, changes the requester has
  specified in full, and work whose approach the requester already approved
- Stay inside the approved plan; when a constraint invalidates it, stop and
  re-surface the options

## Verifying a finding

- Label a finding unverified until it is demonstrated (MUST)

### From reading

[LOAD: verify-finding]

- [ ] Reproduce the defect before reporting it: run the path
- [ ] Read a passing test that contradicts the reproduction before blaming
      the code; it may pin a decision

### From a measurement

[LOAD: verify-finding]

- [ ] The tool measures the rule's unit: bytes are not characters
- [ ] The tool measured the claimed scope, not a diff, sample or partition;
      a whole-codebase claim comes from a whole-codebase run (MUST)
- [ ] The mode that produced each kept number is recorded beside it
- [ ] One flagged item was checked by hand
- [ ] Each count carrying a finding was produced twice, by different means
- [ ] A zero was checked by finding one positive by hand
- [ ] The tool fails loudly on unsupported input rather than exiting clean
      (SHOULD)

### From an extraction

[LOAD: verify-finding]

- [ ] An element reported absent was checked against the raw artifact
- [ ] Extracted size was compared with the raw artifact, and known elements
      survived the round trip
- [ ] The claim is scoped to what was inspected: "not verifiable from the
      extract", never "missing"

### From a probe

[LOAD: verify-finding]

- [ ] The probe ran under the conditions the finding is about, such as its
      user, credential and environment
- [ ] A claim the probe cannot make under those conditions is scoped to the
      ones it tested

### From an agent

- Check an agent's finding against the file, commit or document that
  settles it before acting on it or repeating it
- Distinguish a verified negative from a failed lookup, and say which
- Count a finding several agents agree on as one finding
- Correct a finding you passed on that proves wrong, and name what the
  check showed
- Reconcile a finding with a verified record it contradicts before
  changing anything: confirm both read the same artifact, prefer the more
  specific evidence, and record the outcome
- Record a reversal of a documented decision, with its reason, in the
  artifact that documented it
- Give a verifying agent the existing record and ask it to reconcile, not
  re-derive
- Never delete a record because a check "could not confirm" it (MUST NOT)

## Deviations

- Explain a deviation from a SHOULD rule in the pull request
- Land a deviation from a MUST or MUST NOT rule only with a designated
  approver's sign-off and its reason recorded in the pull request (MUST)
- Never waive a MUST or MUST NOT rule yourself; stop and ask the approver
