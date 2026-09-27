# What the templates can and cannot claim

An assessment of the evidence the efficacy benchmark has produced so far, read
against what this library says it does. It argues from three rounds, dated
2026-09-17, 2026-09-18 and 2026-09-27, whose reports sit under `docs/audits/`.
The experiment itself — its rules, metrics and controls, all fixed before the
first trial — is `efficacy-benchmark.md` in this directory.

## 1. The answer in brief

On one well-specified web application, built in a single session by a strong
model, **no context file made the code measurably better in a way that held
from one round to the next.** Every file made the agent build more and spend
more. The one gain the evidence supports is narrower than "better code": with
the templates' hybrid file, and to a lesser degree its short one, the agent
followed the project's conventions more often.

So the templates cannot claim today that they make an agent write better
software. They can claim, as a signal rather than a proof, that they get their
conventions followed. Whether they help where a project resembles real work
more closely — a thin spec, a cheaper model, many sessions over months — is
untested, and section 6 sets out how each would be tested.

## 2. What was tested

The question is the one a team adopting the library would ask: does an agent
given a generated `CLAUDE.md` build a better application than the same agent
with none, given the same spec, model and tools, and at what cost?

| Setting | Value |
|---|---|
| Application | `tariff`, a small invoicing engine with a Flask, Jinja and HTMX front end, about 1,500–2,000 lines |
| Spec | 475 lines, handed to every arm; it fixes the contract the grader needs, not how to engineer it |
| Builder | `claude-sonnet-5` in Claude Code, one session per build, no web access |
| Arms | `none` (no file), `full` (the generated file, inline), `short` (generated, at most 40 lines), `hybrid` (generated, with the templates vendored into the workspace), `hand` (a hand-written file of at most 40 lines) |
| Trials | K = 3 per arm, paired by block: `full-1` is compared with `none-1` |
| Task success | A hidden acceptance suite, kept in a private repository the agent never sees |
| Quality | Static tools (ruff, mypy, bandit, complexity, coverage), structural probes, eleven security and three data-protection probes, and a model judge reading the code blind, three times per tree |
| Verdict | A bootstrap interval over the three paired differences: **better** or **worse** only when the whole interval sits on one side of zero |
| Change task | A second session adds a feature the design was not told about, to see how far each design has to be disturbed |

The rules for reading a result were committed before any trial ran, so no
metric or threshold could be picked after seeing the numbers. The `hand` arm
exists to separate "the templates helped" from "having any file helped".

## 3. What the evidence shows

### 3.1 Task success does not move

Every arm passes almost the entire hidden suite. In round 3 the rates are 99.5
to 99.6 % for every arm, including `none`, and every change task passes its
acceptance suite in full. A context file neither rescues nor breaks a working
build here, because a strong model given this spec already gets it right.

### 3.2 Code quality: no verdict survives from one round to the next

The headline verdict per arm, "does the file improve the code?":

| Arm | Round 1 | Round 2 | Round 3 |
|---|---|---|---|
| `full` | No | not measured | Yes |
| `short` | — | Worse | Worse |
| `hybrid` | — | No | Worse |
| `hand` | Yes | not measured | No |

`full` goes from No to Yes, `hand` from Yes to No. A reader could take either
round's verdict as the answer; the argument here is that neither is. Between
rounds the judge changed vendor, the spec and the hidden suite were revised,
and the templates moved on by several revisions. Each round's verdict is
internally sound, but three trials describe a result rather than prove it, and
a verdict that flips when the ruler changes is not yet a finding.

What does hold within round 3: `full` reads as more readable (+0.7 on a 1–5
scale) and better tested; `hybrid` reads as more secure to the judge (+0.4);
`short` loses one security probe in every trial (−9.1 percentage points). None
of these appeared in an earlier round.

### 3.3 Size and cost rise, every round

This is the one result that repeats without exception. Every file arm writes
more code and more files, takes more turns, and costs more. In round 3, against
`none`:

| Arm | Lines of code | Files | Cost per build |
|---|---|---|---|
| `full` | +180 % | +124 % | +122 % |
| `short` | +52 % | +24 % | +32 % |
| `hybrid` | +96 % | +76 % | +87 % |
| `hand` | +122 % | +29 % | +53 % |

The follow-up change then has to move through that larger structure: `full`
touches twice the files `none` does to add the same feature. The extra code is
not waste by definition — some of it is tests, and `full`, `hybrid` and `hand`
each cover 4 to 7 more points of their own code with them — but it is paid for
on every build and every change.

### 3.4 Conventions are followed more often, with the hybrid file

The adherence checklist scores thirteen conventions on every arm, the bare one
included: lint-clean, type-clean, formatted, coverage at 80 %, complexity
bounded, a `src/` layout, one error hierarchy, no `print` in the library, a
library logger with a null handler, packaging metadata, a usable README,
discoverable tests, and no ticket citations in code.

In round 3, against `none` at 52.8 % of the checklist:

| Arm | Adherence | Difference, with its interval | Verdict |
|---|---|---|---|
| `hybrid` | 74.3 % | +21.6 points (18.6, 24.3) | better |
| `short` | 63.9 % | +11.1 points (8.3, 16.7) | better |
| `hand` | 66.7 % | +13.9 points (0, 22.2) | no improvement shown |
| `full` | 55.3 % | +2.5 points (0, 3.8) | no improvement shown |

`hybrid`'s gain is the clearest in round 3: every one of its three trials beats
its partner, by 19 to 27 points, and task success holds
within the two-point margin while it does. It is also the only effect here
that answers the library's own claim directly.

Two readings keep it in proportion. Several items are rules the templates
themselves state, so a file that carries them is expected to raise the count;
the gain shows the rules were delivered and followed, which is the library's
purpose, not that the code is better. And `full`, generated from the same
library but delivered inline without the vendored templates, gains almost
nothing. Two files from one library differ by 19 points, so what a file carries
and how it is delivered matter as much as the library behind it.

### 3.5 Length is not quality

Round 1's 39-line hand-written file was the only arm judged better that round,
and it wrote no more code than `none`. Round 3's 39-line generated file lost a
security probe in every trial, and its hand-written peer moved nothing. Across
rounds, the long files cost the most and the short ones the least, and neither
length bought quality reliably.

## 4. Why round 3 could not see a gain

The most useful thing the three rounds show is what they could not show. The
bare agent left almost nothing for a file to fix, and two things put it there.

**The spec states much of the *what*.** It is 475 lines. It is careful to leave
out *how* the application is engineered — no layout, linter, logging policy or
password scheme — because that is what a context file would add. But it
requires every route behind sign-in, CSRF and server-side validation on form
posts, erasure of a customer on request, an export of one customer's data,
valid HTML, `Decimal` money with named rounding points, and an error base
class. A requirement in the spec reaches every arm alike.

**The model supplies most of the *how* unprompted.** The eleven security probes
mostly test what the spec leaves out: a hashed password, sign-in failures that
do not reveal which accounts exist, no open redirect, a secret key not
hard-coded, debug off, session cookie flags, security headers, no stack traces
in error answers. In round 3 the bare agent passes every one of them in every
trial, and every data-protection probe too. The defaults a context file would
state are defaults `claude-sonnet-5` already applies to a Flask application.

So round 3 measured the case least favourable to a context file: a strong
model, a complete spec, one session. Nothing there was left to improve, and
the one probe a file moved, it moved the wrong way (`short` dropped security
headers or a cookie flag). The round cannot say how much of the ceiling is the
spec and how much the model, because it varied neither; the axes in section 6
separate the two. It says nothing about the cases a real project more often
is.

## 5. What the templates can and cannot claim

The library's README makes its case in three parts: it codifies a team's
conventions once, feeds them to every agent on every project, and stops the
codebase drifting from those standards. Read against the evidence, beside two
claims a reader is likely to assume:

| Claim | Status | Evidence |
|---|---|---|
| The agent follows the codified conventions | **Supported, as a signal** | Adherence gains for `hybrid` and `short` in round 3 (§3.4); one round, K = 3 |
| A context file does not break working software | **Supported** | Task success within 2 points for every arm in round 3 (§3.1) |
| The agent writes better-designed, more readable or more secure code | **Not supported** | No quality verdict holds across rounds (§3.2) |
| Using the templates costs little | **Contradicted** | 32 to 122 % more per build, and more churn per change (§3.3) |
| A longer, more complete file is better | **Contradicted** | Length tracked cost, not quality (§3.5) |
| Every project and every agent gets the same conventions | **Untested** | Needs agreement across trials and a second agent (§6) |
| The codebase stops drifting over time | **Untested** | Every trial so far is one or two sessions (§6) |
| The effect generalises beyond one app, stack and model | **Untested** | One application, one stack, one builder model |

The fair public statement is therefore modest: the templates deliver
conventions an agent then follows, at a real cost in tokens and code volume,
and on a well-specified single build they do not make a strong model's code
better. Anything beyond that is a hypothesis, not a result.

## 6. What is untested, and how it would be tested

Three axes cover the settings round 3 could not see. Each hypothesis is to be
registered before its first counted trial with one primary metric, its
direction, its margin and the result that would refute it.

**Spec variant.** The spec is one half of round 3's ceiling, so it is the
first to vary: vague (a paragraph of intent), thin (only the contract the
grader needs), normal (round 3's), detailed and overspecified. Two variants
test the file under stress. *Pressure*: the spec itself asks for a bad
practice, such as an unauthenticated export of the users table — does the file
hold its security rules? *Conflict*: the spec contradicts the file, say a flat
layout and plain `sqlite3` where the file says `src/` and SQLAlchemy. The spec
is the project's own decision and should win; if the file wins, the templates
harm every project that departs from their defaults. The same design yields a
*substitution* contrast with no extra trials: a file plus a thin spec against
no file plus the normal spec. If the first is no worse, the templates stand in
for spec-writing effort, which is a claim worth making.

**Budget.** A cheaper build is a weaker model, a lower reasoning effort or a
tighter turn cap. Dollars largely fix the model-and-effort pair, but one budget
buys different mixes, so points along the axis are chosen and the model and
effort behind each recorded. The hypothesis is that a file compensates for what
a cheaper configuration does not know.

**Project evolution.** A project built in steps across sessions — a Python
library, then a Flask application on it, then a chain of changes — tests the
claim closest to the README's: that conventions hold over a project's life
where a bare agent drifts. The measure is the slope of adherence and the
judge's rows across steps, not their level. It also widens the task beyond a
greenfield build to changes, refactoring and review.

Two further tests sit outside the axes: whether an arm's trials agree with each
other more than bare trials do (analysis of round 3's data, no new trials), and
whether the effect carries to another agent reading `AGENTS.md`.

## 7. Limits of this evidence

- **Three trials per arm.** No arrangement of three paired differences reaches
  conventional significance; every interval is descriptive. One escalation to
  K = 5 is owed on round 3's judge security row and has not yet run.
- **One application.** `tariff` is the development app. A second, `ledger`, is
  sealed for the final claim, so nothing here is tuned against it.
- **One builder model, one agent.** All trials use `claude-sonnet-5` in Claude
  Code.
- **A model judge.** The judge is blind, shuffled, anchored and validated
  against a control fixture, but it is one model per round, and round 3's is
  from the same vendor as the builder.
- **Reach.** Some change-task sessions read outside their workspace; the
  reports name each one.
- **The benchmark changed while it ran.** Five measurement defects were found
  and fixed before round 3's report, each with a control. That is why the
  rounds are not pooled.

## 8. What would change this conclusion

- A file arm that turns a primary dimension better in one round and holds it in
  the next, under the same judge and spec.
- A thin or vague spec under which the file closes a gap the bare agent opens —
  a failed security probe, a lost data-protection property, a missed pattern.
- A weaker or cheaper builder under which the file lifts task success.
- A chain of sessions in which the bare agent's adherence falls and the file
  arm's does not.

Any one of these would move a claim in section 5 from untested to supported.
None has been observed yet.
