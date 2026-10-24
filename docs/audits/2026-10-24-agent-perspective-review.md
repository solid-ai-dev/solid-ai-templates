# Template review from an agent's perspective — 2026-10-24

## Purpose and scope

Assess how well the templates help an agent deliver consistent B+ engineering
work across projects and teams, and identify concrete improvements.

- Reviewed revision: `c9d36785`.
- Coverage: all 39 production templates and both test fixtures.
- Perspective: an agent interpreting, applying and verifying the instructions.
- Deliverable: findings and recommendations; no template changes.
- Evidence: direct reading, composition metadata, the repository's form scorer,
  and existing evaluation documentation.

The scores below are review judgments, not measured predictions of generated-code
quality. Textual ambiguities are observable in the reviewed files. Their effects
on downstream agent behavior remain hypotheses until exercised in trials.

## Overall assessment

**Overall score: 7/10 against the goal of consistent B+ output.**

The engineering guidance is strong, especially its verification discipline.
The main weaknesses are applicability, proportionality and deciding when the
requested result is complete. Many individual rules are clear; their combination
can still require interpretation or impose unnecessary work.

| Quality goal | Score | Assessment |
|---|---:|---|
| Engineering guidance | 8 | Broad, concrete coverage of common failure modes |
| Verification discipline | 9 | Strong protection against false confidence |
| Clarity and consistency | 7 | Clear individual rules; ambiguous combinations remain |
| Applicability across projects | 6 | Some specialized practices become universal obligations |
| Attention and execution cost | 6 | Considerable material competes with the actual task |
| Calibration to good enough | 6 | Strong requirements; weaker stopping and proportionality guidance |

The overall score is the equal-weight mean of these judgments. A severe defect
must still be reported separately; the average does not excuse one.

### Measurements and limits

The review session runs the form scorer in its default all-template mode:

```bash
py tools/score_templates.py
```

Result: 39 templates scored, median 100.0/100, none below 50. This is a writing-form
measurement. The scorer's [design](../design/template-content-quality.md) explicitly
states that it does not establish correctness or usefulness.

The five universal core files contain approximately 8,000 whitespace-delimited
words. A direct non-whitespace-token count gives 8,028 words and a line count gives
1,195 lines, including examples and checks. This describes the source corpus,
not the size of every generated consumer context. A second split-based count
agrees at the rounded level; trailing empty elements explain its small difference.

The smoke invocation cannot start because PyYAML is missing:

```bash
py tests/run.py smoke
```

No smoke check runs, so this review claims no structural pass. It also claims no
new conformance or efficacy result.

The existing [round-4 efficacy report](2026-10-17-round-4.md) contains mixed results,
limited trials and a documented setup confound. It predates this revision and
does not establish the effectiveness of the current text.

## Guidance to preserve

### Tests that demonstrate the actual property

[Testing](../../templates/core/testing.md) tells the agent to verify that a guard
is used, not merely that the guard works; pair a negative assertion with a positive
control; and distinguish a value's provenance from its coincidentally correct
value. These directly counter plausible but ineffective agent tests.

Keep these rules and their concrete examples through any rewrite.

### Trustworthy checks and completion claims

[Quality gates](../../templates/core/quality-gates.md) requires evidence about the
inputs reached, the subject inspected, the timing of the check and its response
to planted violations. It also rejects brittle automation of subjective judgments.

This is among the library's strongest contributions. Preserve both the controls
and the distinction between an automatic verdict and a human reading.

### Concrete operational boundaries

- [Messaging](../../templates/backend/messaging.md) distinguishes coalescing
  repeated refresh requests from losing separate inventory decrements.
- [Webhooks](../../templates/backend/webhooks.md) requires durable storage before
  acknowledgement.
- [Data migration](../../templates/data/data-migration.md) waits for old readers
  and writers before removing the old schema.

These examples reduce implementation ambiguity. Prefer this form when improving
other rules: identify the decision and demonstrate the relevant boundary.

### Honest evidence and restrained architecture

[Measurement](../../templates/core/measurement.md) separates missing source values
from extraction failure and prevents predictions from becoming their own ground
truth. [OOP](../../templates/core/oop.md) explains when a class is unnecessary.

Preserve both. They counter tendencies to invent plausible evidence and introduce
unnecessary structure.

### Useful shared defaults

Security boundaries, configuration precedence, rendered frontend verification,
accessibility checks and runtime-version coherence give teams common expectations.
Keep deliberate organization conventions. Improve their conditions and exceptions
where needed, rather than making every choice optional.

## Improvement priorities

### 1. Make B+ an operational completion standard

The [quality requirements](../architecture/10-quality-requirements.md) already
describe useful outcomes. Carry a concise task-level version into generated
context so it guides implementation and completion.

| Dimension | Required outcome |
|---|---|
| Functionality | Requested behavior works through its actual entry point |
| Correctness | Relevant boundaries, failure paths and compatibility requirements are covered |
| Security and data | Applicable security and data-integrity guarantees survive the change |
| Maintainability | Implementation fits the project and introduces only necessary complexity |
| Verification | Evidence demonstrates the change; unavailable checks are disclosed |
| Scope | Unrelated behavior and existing user work remain intact |
| Delivery | Necessary documentation and operational instructions agree with the result |

Treat these as separate requirements. Excellent naming or documentation cannot
compensate for a serious correctness failure.

Proposed stopping rule:

> Complete the requested behavior and its necessary verification. Add further
> abstractions, infrastructure or process only when a requirement, demonstrated
> defect or material risk justifies them.

Acceptance example: adding pagination produces bounded results, appropriate tests
and an updated contract. It does not trigger a repository-wide service-layer
rewrite.

### 2. Audit strength and applicability together

Plain imperatives mean MUST under [rule language](../../templates/core/docs.md).
That gives context-dependent implementation choices mandatory force unless their
conditions are explicit.

Classify each rule during review:

| Rule kind | Recommended treatment |
|---|---|
| Essential invariant | Keep MUST/MUST NOT and state its boundary precisely |
| Deliberate organization policy | Keep mandatory after adoption; identify the choice during setup |
| Preferred implementation | Use SHOULD and identify circumstances supporting another choice |
| Conditional procedure | State its trigger before its instructions |
| Example | Prevent its numbers, tools or architecture becoming accidental requirements |

Use this as an authoring aid, not a new taxonomy consumers must learn.

Review universal exception hierarchies, replacement of every unit dependency with
a double, directory-derived test tiers and universal zero-downtime deployment
first. The objective is predictable decisions with fewer unnecessary exceptions,
not reducing MUST counts for their own sake.

### 3. Resolve interpretation gaps first

| Boundary | Recommended correction | Acceptance example |
|---|---|---|
| Public endpoints and authentication | Classify access explicitly. Protect endpoints by default; declare public exceptions and reconcile health access in the same change. | A public catalogue stays public; account records remain protected; probes use the declared access model. |
| Browser and service authentication | Scope refresh-token cookies to the browser flows that use them. State service identity requirements separately. | A gRPC worker acquires no browser-cookie mechanism merely through template inheritance. |
| Estimates and source truth | Separate observations, estimates and reference outputs. Permit declared product estimates without substituting them for evidence. | A forecast contains estimates while its validation dataset preserves absent observations. |
| Rule selection and inline delivery | Say every adopted rule where generation currently says every rule. Make the adopted selection authoritative. | Reading a newly pinned template does not silently add project obligations. |
| Optional integrations and secrets | Require a secret when its capability is enabled; validate enabled capabilities at startup. | Disabled mail delivery needs no provider key; enabled delivery fails clearly without it. |
| API version terminology | Separate the compatibility identifier, such as /v1, from the contract document's revision. | An optional endpoint updates the contract without forcing /v2. |

Sources: [HTTP](../../templates/backend/http.md),
[observability](../../templates/backend/observability.md),
[authentication](../../templates/backend/auth.md),
[data quality](../../templates/data/data-quality.md),
[context generation](../../templates/core/agents.md),
[configuration](../../templates/core/config.md), and
[API design](../../templates/backend/api.md).

These are text-level findings and proposed clarifications, not reproduced
downstream failures. For example, the health conflict requires a health endpoint
that is externally reachable; it does not affect every deployment.

### 4. Clarify relevance before cutting context

For each section, identify:

- Trigger: the project property or task that activates it.
- Action: the decision the agent should make.
- Evidence: how compliance is established.

Start container-testing guidance with an explicit container-testing condition.
A library without containers should not need to interpret resource-reaper rules.

Clarify conditions inside existing files first. Consider moves only after
measuring generated contexts and behavior. Preserve frozen IDs and paths.

Keep universal guidance focused on protecting work, staying in scope, verifying
actual behavior, preserving contracts, distinguishing evidence from assumptions
and choosing a sufficient implementation.

### 5. Declare the approval model and protect existing work

Generated context should settle which work the task request authorizes, which
paths or decisions require separate approval, when an outline is sufficient,
what invalidates an approval, and who approves policy deviations.

Keep stricter governance where a team chooses it. Avoid forcing agents to infer
it from unrelated instructions or ask again after an applicable approval.

Add a direct preservation rule to [Git](../../templates/core/git.md): inspect
existing changes, preserve unrelated work, and never discard it merely to obtain
a clean test baseline. This supports the project's stated lost-work scenario.

## File-level recommendations

The actions below are proposals, not instructions already adopted by consumers.
Preserve useful existing rules while changing their boundaries. A recommendation
to reconsider a default does not establish that the default is technically wrong.

### Core

| Template | Recommended action |
|---|---|
| [agents.md](../../templates/core/agents.md) | Make adoption precede delivery. Replace the literal next-turn relevance test with project relevance or an explicit task trigger. Qualify the inline model's highest-reliability claim until outcome evidence supports it. |
| [quality.md](../../templates/core/quality.md) | Preserve simplicity, compatibility and check trust. Review universal exception hierarchies, return-type shims and naming restrictions as conditional policies. Apply UTF-8 requirements explicitly to text files. Add the completion stopping rule. |
| [testing.md](../../templates/core/testing.md) | Preserve provenance, positive controls, input reach and rendered verification. Permit real deterministic collaborators. Treat mock count as a design signal. Scope leak checks to owned resources and fixture lifetime. Bind tier mechanics to the stack. |
| [review.md](../../templates/core/review.md) | Preserve evidence verification and security-first review. Audit adopted requirements. Separate demonstrated defects, policy deviations and improvement suggestions. Follow the declared approval model for planning. |
| [git.md](../../templates/core/git.md) | Protect pre-existing changes explicitly. Clarify agent commit identity. Bind forge-specific commands through the fork or state their condition. Preserve CI evidence and regeneration checks. |
| [docs.md](../../templates/core/docs.md) | Preserve adoption and source-of-truth rules. Exempt historical records from present-tense requirements. Distinguish project rules from architecture explanations when placing material in agent context. |
| [config.md](../../templates/core/config.md) | Require secrets for enabled capabilities. Let the schema declare whether empty values are legal without permitting silent fallback. Make the example follow its own variable-prefix convention. |
| [oop.md](../../templates/core/oop.md) | Preserve class restraint. Explain when an interface earns its cost. Reconsider mandatory factory placement and pattern names where they add indirection without improving the design. |
| [quality-gates.md](../../templates/core/quality-gates.md) | Preserve planted violations and scope checks. Adopt an explicit project linter rule set. Scope byte-identical refactor checks to deterministic output and declare normalization. Preserve scrutiny of weakened tests. |
| [embedded-checks.md](../../templates/core/embedded-checks.md) | Preserve extraction and compilation checks. Declare shell, working directory, dependencies and substitutions. Demonstrate clean and failing executions of extracted commands. |
| [measurement.md](../../templates/core/measurement.md) | Preserve provenance and blind reference collection. Clarify threshold-tuning order. Separate computational correctness from human verification of observations. Declare numerical tolerances when exact equality is inappropriate. |

### Backend

| Template | Recommended action |
|---|---|
| [http.md](../../templates/backend/http.md) | Resolve public and operational endpoint access. Separate durable/request state from disposable in-process state. Make port ownership conditional on hosting. Preserve parsing, bounded waits and shutdown guidance. |
| [api.md](../../templates/backend/api.md) | Separate agreement on a contract from hand-authoring its specification. Permit the chosen generation method with drift tests. Clarify version terminology and removal when a Sunset header is omitted. |
| [auth.md](../../templates/backend/auth.md) | Separate browser sessions, bearer-token APIs and service identities. State when refresh tokens exist. Preserve object-level authorization, revocation and negative tests. Label fixed lifetimes as defaults or adopted policy. |
| [database.md](../../templates/backend/database.md) | Preserve bounded reads, transactions and real-engine tests. State workload assumptions behind index and isolation defaults. Reconcile migration immutability with the data-migration template. |
| [caching.md](../../templates/backend/caching.md) | Preserve stale-window and race guidance. State how fallback protects the origin during an outage. Distinguish optional acceleration from authoritative session or coordination storage. |
| [concurrency.md](../../templates/backend/concurrency.md) | Bind cancellation signatures and race tooling to the runtime. Clarify bounded shutdown for uncooperative workers. Preserve ownership, lock ordering and disjoint-input tests. |
| [jobs.md](../../templates/backend/jobs.md) | Clarify that HTTP/database work belongs in delegated services, not that jobs generally prohibit it. Test handler wiring as well as business logic. Serialize schedules when overlap is unsafe. |
| [messaging.md](../../templates/backend/messaging.md) | Preserve durable acknowledgement and coalescing distinctions. Name retry ownership after handoff, poison-message handling and replay procedures. Require ordering where the domain needs it. |
| [webhooks.md](../../templates/backend/webhooks.md) | Preserve raw-byte verification and durable fast acknowledgement. Test persistence failure before acknowledgement. Scope deduplication identity by provider/connection where needed. Bind replay controls to the signature protocol. |
| [edge.md](../../templates/backend/edge.md) | Make availability-zone layout and geo restrictions conditional. Preserve trusted-proxy boundaries and body/time limits. Reconcile health exposure with HTTP and observability. |
| [grpc.md](../../templates/backend/grpc.md) | Prevent inherited browser-auth requirements. Clarify whether HTTP health is needed alongside gRPC health. Test deadlines and cancellation, including streams. |
| [microservices.md](../../templates/backend/microservices.md) | Preserve extraction restraint and ownership. Replace service-count suspicion with coupling evidence. Treat synchronous-hop limits as adopted budgets. Qualify consistency/availability guidance by failure assumptions. |
| [errors.md](../../templates/backend/errors.md) | Scope HTTP mappings to HTTP boundaries. Redact diagnostics before logging external errors. Share a bounded retry/deadline budget. Aggregate repeated unexpected failures into tracked defects. |
| [features.md](../../templates/backend/features.md) | Resolve permission flags versus mandatory retirement. Separate temporary rollout flags from durable entitlements. Define freshness and outage behavior instead of universally banning database storage or cross-request caching. |
| [observability.md](../../templates/backend/observability.md) | Separate liveness, readiness and detailed diagnostics. Identify readiness dependencies and reconcile health access. Define log-volume and sampling expectations while preserving required audit records. |
| [monitoring.md](../../templates/backend/monitoring.md) | Bind metrics to objectives and failure modes. Mark sample thresholds as illustrations. Define initial baselines for new services. Make status pages conditional on audience and operating needs. |

### Data

| Template | Recommended action |
|---|---|
| [data-modeling.md](../../templates/data/data-modeling.md) | Preserve deliberate relationships and precise types. Choose keys by identity stability and exposure requirements. Give normalization explicit exceptions. Preserve domain-required timezone information alongside UTC instants where needed. |
| [data-migration.md](../../templates/data/data-migration.md) | Separate rerunning a tracked migration command from rerunning its body. Require recovery from partial execution. Generalize validation beyond slug keys to missing, duplicate and orphaned records and relevant totals. |
| [data-governance.md](../../templates/data/data-governance.md) | Make classification and retention concrete project inputs. Explain authorized retention deletion alongside append-only storage. Decide explicitly which old sensitive values an audit trail records. |
| [data-quality.md](../../templates/data/data-quality.md) | Separate estimates and observations. Measure completeness over applicable fields and essential fields separately. Permit declared degraded presentation. Define the conservative direction of estimates. Group coherent corrections together. |

### Frontend

| Template | Recommended action |
|---|---|
| [ux.md](../../templates/frontend/ux.md) | Preserve keyboard, focus and manual verification. Separate automatic evidence from human sign-off. Define loading, empty, error and success states. Make browser support an explicit project choice. |
| [quality.md](../../templates/frontend/quality.md) | Make optimistic mutation conditional on recoverability. Bind browser-test serving to the framework rather than a thread. Separate new console failures from documented existing ones. |
| [content.md](../../templates/frontend/content.md) | Scope indexing and social metadata to relevant public content. Permit approved asset pipelines/CDNs. Prefer accurate useful descriptions over mandatory marketing language. Validate URLs under the deployment base path. |

### Infrastructure and security

| Template | Recommended action |
|---|---|
| [cicd.md](../../templates/infra/cicd.md) | Separate services, libraries and documentation projects. Bind availability to requirements. Define emergency-change reconciliation. Distinguish a source release record from successful publication or deployment. |
| [containers.md](../../templates/infra/containers.md) | Preserve non-root execution and runtime coherence. Align image identity with reproducibility requirements. Permit deliberate read-only mounts that do not replace application code. Give vulnerability exceptions owners and expiry. |
| [deployment.md](../../templates/infra/deployment.md) | Scope certificate, registry and secrets procedures to the target. Accept platform-provided capabilities without duplicate infrastructure. Test actual startup, connectivity and recovery assumptions. |
| [security.md](../../templates/security/security.md) | Preserve validation, CSRF distinctions and SSRF controls. Separate browser-response controls from other protocols. Clarify safe inspection of public certificates and examples without disclosing secrets. Scope domain-wide HSTS choices explicitly. |
| [devsecops.md](../../templates/security/devsecops.md) | Reconcile mandatory SBOM delivery with tolerated missing uploads: preserve source records but surface missing required release evidence. Define exception ownership, expiry and rechecks. State scanner applicability per artifact type. |

### Fixtures

Keep [stack](../../templates/fixture/stack.md) and
[platform](../../templates/fixture/platform.md) as test inputs. Add focused
composition cases around interpretation boundaries rather than making the fixture
stack a model production architecture.

## Better examples and runnable checks

For consequential rules, show a short applicable case, a nearby non-applicable
case and the observable difference. For example:

> A reference dataset preserves an absent measurement as missing. A forecasting
> feature may produce an estimate in a separate field with its method and
> provenance.

This teaches the boundary more clearly than another blanket prohibition on
invented values.

For each shipped check, provide prerequisites, shell, working directory, inputs,
timing, pass condition and the meaning of not applicable. Bind project-specific
values during generation. Do not make agents discover setup by repeatedly running
unusable commands.

Keep subjective judgments declarative. An automated keyword check cannot reliably
decide whether a solution is proportionate or an exception is justified.

## Behavioral acceptance cases

Structural checks establish composition, not consistent interpretation. Start
with the following cases before a broad rewrite:

| Case | Expected behavior |
|---|---|
| Public catalogue and protected account API | Preserve public access and enforce account authorization |
| Internal gRPC worker | Use the declared service identity without inventing browser authentication |
| Disabled optional integration | Start without its secret; fail clearly when enabled without it |
| Small library defect | Make a focused fix without service deployment infrastructure |
| Shared-function change | Exercise affected behavior without rewriting unrelated callers |
| Partial data migration | Detect incomplete population and follow the recovery procedure |
| Dataset with observations and estimates | Preserve the distinction through validation and presentation |
| Frontend interaction change | Inspect rendered behavior and report manual accessibility work honestly |
| Failed or empty quality check | Report insufficient verification without claiming a clean result |
| Existing uncommitted changes | Preserve user work while completing the request |

Use fresh agent sessions and repeated trials. Compare current templates, the
candidate change, a small curated context, and a no-template baseline where
meaningful. Keep task, model, settings, fixture and permissions comparable.

Measure:

- Share of outcomes that meet every required B+ dimension.
- Severe correctness, security or data-loss failures, reported separately.
- Unnecessary changes outside the task.
- Approval interruptions and unresolved interpretation questions.
- Time and cost, beside task completion.
- Variation between runs and project types, not only the best or average result.

Extend the [efficacy benchmark](../design/efficacy-benchmark.md) rather than create
a competing score. Predeclare acceptance criteria and comparison rules. Treat
small trial sets as descriptive evidence and report inconclusive outcomes.

## Implementation sequence

| Order | Change | Evidence needed before proceeding |
|---|---|---|
| First | Resolve adoption, authentication, estimates, optional secrets and version boundaries | Examples admit one clear interpretation; related templates agree |
| Second | Make B+ completion and approval boundaries explicit | Bounded tasks finish without unrelated work or unnecessary approval rounds |
| Third | Improve testing proportionality and preserve user work | Verification remains meaningful without implementation-mirroring tests |
| Fourth | Clarify applicability across the domain templates | Representative project types receive relevant requirements |
| Fifth | Reduce repeated or specialized core material | Before/after mapping preserves conditions, exceptions and intended strength |
| Sixth | Evaluate generated contexts and delivery models | Repeated outcomes support claimed consistency or cost improvements |

Use small, focused PRs with a behavioral case attached. Apply the playbook's
template-review procedure: map each old rule to its replacement, preserve shipped
IDs, run the applicable structural and conformance checks, read judgment outputs,
and update affected documentation. Assess changes to the composition or delivery
contract under the repository's ADR threshold.

Do not lower normative strength silently during shortening. Record intentional
policy changes separately from wording fixes. A smaller context is an improvement
only when the required outcomes hold.

The preferred first step is resolving the interpretation gaps and exercising
their acceptance cases. It targets cross-team consistency without first
restructuring the library or weakening its useful engineering standards.
