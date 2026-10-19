# Base — Git Conventions
[ID: base-git]

## Committer identity
- Configure git with your full name and a consistent, professional email address
- Do not use private or personal email addresses for work repositories
- Identity must not change — git history and tooling depend on consistent
  authorship

## Branching
- Always work on a branch — never commit directly to `main`

## Pull requests
- PRs should be small and focused — one concern per PR
- Always test locally before committing
- **A local run is evidence about one platform.** Read the CI run for the
  push before describing the change as good. Where development and CI
  differ in operating system, interpreter version or locale, a green
  local suite and a green pipeline are different claims, and only the
  second covers what the project ships on. A pipeline check at session
  start is a different moment — it catches one broken before you began,
  not one you broke and are about to report as clean
- **A check reading the change under review is confirmed where it ships.**
  The host builds that subject rather than finding it: a pull-request event
  checks out a merge commit of the branch into the base, HEAD is detached,
  the clone may be shallow, and the branch name survives only in an
  environment variable. A check that counts commits, names the branch or
  diffs against the base therefore reads a different tree there from the one
  it was written against, and every control run on the author's machine
  still passes. Read its first run in that environment and require a
  verdict: a check reporting that it does not apply, on the very change it
  was written for, is the failure this catches. It hides in a green pipeline
  because a decline summons no reader
- **Regenerate derived artifacts in the same PR** — when a change
  affects generated or derived files committed to the repo (extractor
  outputs, snapshot fixtures, generated docs), regenerate them in the
  fixing PR, not a follow-up. A stale artifact is indistinguishable
  from a regression to the next reviewer. Include a before/after
  summary (verdict matrix, delta table, screenshot diff) in the PR
  body so reviewers see the user-visible impact without re-running
  the pipeline.
  - When regeneration is too expensive to bundle (e.g. >30s in CI or
    >100 files), the PR MUST open a tracked follow-up issue AND state
    the STALE accounting explicitly (N files affected, named or
    globbed) — silent staleness is the failure mode
  - This rule applies to one-directional (source → artifact)
    derivations only. An artifact that also serves as, or feeds, the
    source of truth is bidirectional — the tell is an `--apply` or
    ingest step that reads the artifact back into the source. Do NOT
    auto-regenerate a bidirectional artifact from the pipeline it
    feeds: regeneration overwrites human-verified values. Refresh it
    only through the human-in-the-loop step that owns it, and flag
    the staleness explicitly instead
- **Before merging**, review the diff against the base branch. Follow
  `templates/core/review.md` priority order: security → correctness →
  clarity →
  conventions. Check CI passes. Only merge after the review passes.
- **A pull request with no registered check has not passed CI.** Run
  straight after a push, before the host has registered the workflow run,
  `gh pr checks <N> --watch` prints `no checks reported` and exits at
  once, so a merge chained after it goes through with no check run and
  the output reads as a quiet pass. Wait until at least one check is
  registered, then watch every check to completion:

```bash
PR=<N>
count=0
# The host registers a run some seconds after the push; poll for it
# rather than reading its absence as a verdict.
for _ in $(seq 1 60); do
  count=$(gh pr checks "$PR" --json name --jq 'length' 2>/dev/null)
  [ "${count:-0}" -gt 0 ] && break
  sleep 5
done
echo "checks registered: ${count:-0}"
[ "${count:-0}" -gt 0 ] || exit 1
gh pr checks "$PR" --watch > /dev/null
watched=$?
failing=$(gh pr checks "$PR" --json bucket \
  --jq '[.[] | select(.bucket != "pass" and .bucket != "skipping")] | length')
echo "checks not passing: $failing"
[ "$watched" -eq 0 ] && [ "$failing" -eq 0 ]
```

  Pass condition: `checks registered` is above zero, `checks not passing`
  is zero, and the block exits zero. Zero registered checks after five
  minutes, or any failing or cancelled check, exits non-zero, and the
  pull request does not merge
- **Re-run the verification a pull request body claims, rather than
  reading it, whenever the base has advanced since the body was
  written.** A well-written body carries evidence — a grep that found no
  surviving references, a count, a command whose output justified the
  change. That evidence is scoped to the base it was produced against,
  and a commit landing afterwards can falsify it without producing a
  conflict, a failing check, or any other signal: the merge is clean, the
  checks pass against the merge commit, and the body still reads as
  verified. It matters most for a change that proves an ABSENCE — a
  deleted file, a removed reference, a retired flag — where the later
  commit reintroduces the very thing the body proved gone
- **Never force-push a branch**, including with `--force-with-lease`.
  Force-push rewrites shared history and can clobber upstream commits
  (collaborators, agents, CI bots) that haven't been fetched locally.
  - When a PR branch is behind `main`, merge `main` into the branch —
    do not rebase and force-push. On GitHub, use the "Update branch"
    button or `gh pr update-branch <N>`.
  - Updating the branch is half the recovery. The merge brings in the
    other branch's sources and re-derives nothing, so a repository
    holding regenerated artifacts now has a branch whose artifact was
    built from a tree lacking them. Git reports the branch `MERGEABLE`
    throughout, because the two changes fall in different regions of
    the same files, so nothing warns that the derived output is stale.
    Regenerate and re-run the staleness comparison AFTER the update,
    and stage what they produce. This is what happens on every release
    carrying more than one pull request, not an edge case

### Verifying regenerated artifacts

Regenerating is owed by the edit, not by the review. Every rule below
inspects output that already exists, and none of them fires if the
regeneration never ran.

- MUST regenerate the artifact and stage both together in the change
  that edits a source. Where an artifact is derived from sources under
  version control, a test suite that does not read the artifact passes
  on a stale one — so local green is not evidence the artifact is
  current, and the first signal is whichever CI step compares the two,
  after the branch is pushed and the author has moved on
- MUST name the regeneration trigger beside the sources it derives from,
  so an author editing a source meets the obligation without having to
  know the build graph
- MUST run the staleness comparison AFTER the edit, and again after any
  merge that brings another branch's sources into this one. Run before
  either, the comparison reports the previous state and reads as a pass:

```bash
<regenerate-command>
git diff --exit-code --stat -- <artifact-path>
```

  Pass condition: no diff, on a zero status — `--exit-code` is what
  makes the absence of output a verdict. Any output means the committed
  artifact does not match what its sources produce, and the
  regeneration is part of this change rather than a follow-up. A
  regenerator that is not idempotent fails this against an
  already-current artifact, which is a defect in the generator rather
  than in the change under review

After regenerating derived artifacts and before staging them, verify
the diff is real and the output is correct.

- Filter line-ending and whitespace noise first, file by file:

```bash
git diff --ignore-all-space <file>
```

  An empty diff marks the change as CRLF/whitespace-only. Drop it with
  `git checkout -- <file>` so the PR stays scoped to genuine content
  (and the noise does not reappear as a fake regression on another OS)
- Binary artifacts (images, diagrams, screenshots, plots) diff as
  "Binary files differ" — opaque to git and often uncovered by the
  test suite. Open each in a viewer (or an image-read tool for agent
  workflows) and confirm it tracks its source data with no corruption
- Regenerate a known-current control artifact on its own first. A zero
  diff proves the generator is byte-deterministic in this environment
  and already matches the committed baseline, so every remaining diff
  is genuine change. A non-zero control diff means the environment
  disagrees with whatever produced the committed files — reconcile
  that before committing, or ship a spurious mass rewrite disguised as
  the intended change
- Mask the known-volatile parts, then diff the remainder. A
  self-contained bundle carries pieces that legitimately change every
  run — an embedded base64 blob, a generation timestamp, a build id. A
  clean masked remainder proves the data and prose are untouched and
  the change lives only where intended:

```bash
mask() { sed -E 's/base64,[A-Za-z0-9+/=]+/base64,#/g' "$1"; }
diff <(mask old.html) <(mask new.html) | grep -v 'generated '
```

- When a fix regenerates many artifacts, pair a spot-check of 3-5
  representative cases (the fix's primary target, the most complex
  case, a clean baseline) with a global metric that aggregates across
  the population (test pass rate, link check, accessibility score,
  calibration result). The spot-check catches broken regeneration;
  the metric catches population-wide drift — together they match full
  per-artifact review at a fraction of the cost

### Ordered documents merge cleanly and still collide

A clean merge proves the *edits* did not overlap. It proves nothing about
whether the *result* is coherent, and for a document with an ordered
structure those are different questions.

Two branches each add a section to the same numbered document. One appends
3.9 at the end; the other inserts 3.5 and renumbers the tail, so its last
section also becomes 3.9. The edits touch different regions, so git merges
them without a conflict and the result carries two sections numbered 3.9.
Nothing reports it — not the merge, not the checks, not a reviewer reading
either diff, because each diff is individually correct. The defect exists
only in the combination. Here a conflict would have been the good outcome:
it would have forced the reconciliation the clean merge skipped.

The existing rules do not reach it. Squash-merge safety is about commits
being orphaned, not content colliding. `Merging a batch of PRs` tells you
to merge the base in and re-run the checks, which resolves the staleness
and produces exactly this clean, wrong merge.

- MUST verify the merged numbering, not merely that the merge was clean,
  when two or more open pull requests edit one document with an ordered or
  numbered structure. The second to merge owns the check
- MUST re-run it after merging the base in, not before — the collision is
  created by the combination, so a run against either branch alone reports
  a clean document
- Applies to any ordered structure a reader relies on: numbered sections,
  ordered procedures, lettered clauses, a table whose rows carry an index

The check. `PATHS` names the documents two open pull requests both touch:

```bash
py - <<'EOF'
import re

# The documents under review -- those more than one open branch edits.
PATHS = ["<file>"]

# A numbered heading (### 3.9 Title) and a list ordinal (  4. Step).
HEADING = re.compile(r"^(#{1,6}) +([0-9]+(?:\.[0-9]+)*)\.? ")
LISTITEM = re.compile(r"^\s*([0-9]+)\. ")
PLAIN = re.compile(r"^#{1,6} ")

failed = False
for path in PATHS:
    group, runs, problems, total = "(top)", {}, [], 0
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        match = HEADING.match(line)
        if match:
            parts = match.group(2).split(".")
            # Group a numbered heading under its parent, so 3.x and 4.x are
            # separate runs and each may legitimately restart.
            key = "%s %s" % (match.group(1), ".".join(parts[:-1]) or "(root)")
            value, label = int(parts[-1]), match.group(2)
            group = line.strip()
        else:
            if PLAIN.match(line):
                # A list restarts under each heading, numbered or not.
                group = line.strip()
                continue
            match = LISTITEM.match(line)
            if not match:
                continue
            key, value, label = group, int(match.group(1)), match.group(1)
        total += 1
        run = runs.setdefault(key, [])
        if value in run:
            problems.append("  %s:%d: %s repeats under %s"
                            % (path, n, label, key))
        elif run and value != run[-1] + 1:
            problems.append("  %s:%d: %s follows %s under %s"
                            % (path, n, label, run[-1], key))
        run.append(value)
    print("%s: %d ordinals across %d group(s)" % (path, total, len(runs)))
    for problem in problems:
        print(problem)
    if not total:
        print("  no ordinals found; the pattern drifted")
    if problems or not total:
        failed = True

# The counts are the reading; the status is the verdict.
raise SystemExit(1 if failed else 0)
EOF
```

Pass condition: the command reports, for each document, how many ordinals
it inspected and how many groups they fall into, and exits zero. A
collision line, or a count of zero, reaches a non-zero status instead. A
count of zero is a failure rather than a flat document — it means the
numbering pattern drifted and the check reached nothing. Adapt the two
patterns to the document's own convention before trusting a clean result;
a check calibrated against the wrong convention reports zero either way.

## General
- Do not commit build output, secrets, or dependency directories
- Do not commit generated files that can be reproduced by running a
  build command
- Treat every repository as if it were public — no secrets,
  credentials, or sensitive information in source files or history

## Submodules
A merged pin bump moves the recorded pointer and nothing else. `git pull`
fast-forwards the superproject and leaves the submodule working tree at
the revision the bump replaced, so the clone reads the old content while
the pin names the new one. It fails silently and at the worst moment:
reconciling against the vendored content is the step after a bump, and
reading it then returns the previous version with no error.

- After pulling a merged pin bump, MUST run
  `git submodule update --init --recursive` before reading anything
  under the submodule path
- The drift is visible before the read: `git status` lists the path as
  modified in the work-tree column and `git submodule status` prefixes
  its line with `+`. A clean status is evidence the tree was moved, not
  that the pull moved it
- A bump procedure MUST carry this step past the merge. One that ends at
  "push, open PR, merge" stops one command short of the state it set out
  to reach
- A project MAY set `submodule.recurse` to `true` so `pull` and
  `checkout` move the tree themselves; the check above still applies to
  clones that have not set it

## Off-limits paths
- Some paths carry consequences a diff does not show. The change reads
  as ordinary and its blast radius is not local, so the usual signals —
  a small diff, a green suite — say nothing about it
- The project's context file MUST declare an **Off-limits** section
  listing paths that MUST NOT be modified without explicit approval. A
  restriction that lives only in a reviewer's head is not one
- Offer this as the default set and let the project cut it down: auth
  and session code, payment and billing code, database migrations,
  `.env*` and anything else handling secrets, CI/CD workflow
  definitions, and — where the project vendors its governing rules — the
  pointer to the submodule carrying them
- That last member earns its place differently from the others, so state
  why beside it. The rest are dangerous for what they execute or what
  they hold; a pointer executes nothing, so no linter, suite or gate
  reads it and the diff is a pair of hashes. One line replaces every rule
  the project binds, which is a wider blast radius than a workflow file,
  and a malformed workflow at least fails loudly
- A change inside an off-limits path MUST be proposed before it is
  made, and the proposal MUST carry a rollback strategy and the test
  coverage that would catch a regression. The approval is for that
  plan, not for the area
- The restriction binds executable content: steps, commands, flags,
  permissions, triggers, pins, and a vendored pointer's revision. A diff
  confined to comments and prose is ordinary work. Its rollback is
  `git revert` and its regression coverage is that nothing executes, so
  a proposal written for it is a form, and a form teaches the next
  author that the proposal step is one
- A directive spelled as a comment is executable. A tool that reads a
  `#` line changes behaviour when the line changes, whatever the line
  looks like — `# noqa`, `# nosec`, a linter's disable comment, a
  coverage pragma
- The diff is the classifier, not the file. A change is prose only when
  removing every comment line from it leaves nothing; one touching a
  comment and a step is executable entire
- A diff touching an off-limits path MUST say so at the top of its
  summary, naming the path, whether or not it owes a proposal. The
  reviewer's attention is the control, and it is only allocated if the
  summary spends it

The check, run from the repository root after committing and before
opening a pull request. Its subject is committed history, so a run
against staged but uncommitted work reports exactly what a compliant
branch reports. Keep `OFF_LIMITS` beside the declared list so the rule
and its check cannot drift apart:

```bash
py - <<'EOF'
import subprocess, sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = "origin/main"

# Prefixes rather than patterns: a path holds no regex metacharacter to
# escape, so nothing can be lost on the way into the file.
OFF_LIMITS = [".github/workflows/", ".env", "migrations/"]

# This check's moment is a branch with commits on it. Run on the base
# itself the range is empty by construction, so the count below would
# print the shape of a failure for a question nobody asked.
here = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                      text=True, encoding="utf-8").stdout.strip()
base = subprocess.run(["git", "rev-parse", BASE], capture_output=True,
                      text=True, encoding="utf-8")

# An unresolvable base is not an empty one. `git rev-parse` echoes the
# argument it could not resolve, so the value looks like a baseline, the
# diff against it errors, and no changed files reads as nothing off
# limits. Ask the exit status, which is the only thing that says whether
# a baseline was produced.
if base.returncode != 0:
    print("%s does not resolve, so there is nothing to diff against"
          % BASE)
    raise SystemExit(1)

there = base.stdout.strip()
if here == there:
    dirty = subprocess.run(["git", "status", "--porcelain"],
                           capture_output=True, text=True,
                           encoding="utf-8").stdout.strip()
    if dirty:
        print("HEAD is at %s and the work is uncommitted; commit it and "
              "run again" % BASE)
        raise SystemExit(0)
    print("HEAD is at %s and the tree is clean; no branch is open, so "
          "this check does not apply" % BASE)
    raise SystemExit(3)

out = subprocess.run(["git", "diff", "--name-only", BASE + "...HEAD"],
                     capture_output=True, text=True,
                     encoding="utf-8").stdout
changed = [path for path in out.splitlines() if path]

print("files changed: %d" % len(changed))

for path in changed:
    for prefix in OFF_LIMITS:
        if path.startswith(prefix) or ("/" + prefix) in path:
            print("  off-limits: %s (matches %s)" % (path, prefix))
EOF
```

Pass condition: the command reports how many files it compared. Zero is
a failure rather than a clean branch, and the likeliest cause is that the
change is not committed yet — the natural moment to run a
pre-pull-request check is while writing it, and that run is guaranteed to
report nothing. The other cause is a wrong base, which the command now
refuses rather than counts: `git rev-parse` echoes an argument it cannot
resolve, so a mistyped base looks like a resolved one and the failing
diff reports the same nothing a clean branch does.

The command separates those two from a third case that is not a failure
at all, and does it before counting. With HEAD at the base it asks
whether the tree is dirty: uncommitted work is the forgot-to-commit
failure above, and said in those words rather than as a zero; a clean
tree means no branch is open, so the check does not apply and exits 3.
The zero it would otherwise print carries the weight of a finding on a
tree where nothing is being proposed. Every
`off-limits:` line is an escalation trigger rather than a failure. The
check reads path names, so it cannot see whether the change inside is
executable or prose and reports both alike; an executable hit is
discharged by the proposal above, a prose-only one by the summary naming
the path.

## `.gitignore`
- Every repository MUST have a `.gitignore` file
- Ignore at minimum:
  - **Dependencies** — `node_modules/`, `.venv/`, `vendor/`
  - **Build output** — `dist/`, `build/`, `out/`, `*.pyc`, `__pycache__/`
  - **Secrets** — `.env`, `.env.local`, `*.pem`, `*.key`
  - **IDE/editor** — `.idea/`, `.vscode/`, `*.swp`, `*.swo`
  - **OS files** — `.DS_Store`, `Thumbs.db`, `desktop.ini`
  - **Test/coverage** — `coverage/`, `.coverage`, `htmlcov/`
- Share the editor config that mirrors the CI gates through an
  allowlist rather than ignoring the directory wholesale — ignore
  `.vscode/*`, then re-include `!settings.json` and
  `!extensions.json`. The shared project setup is versioned while
  per-user editor state stays ignored
- Use [gitignore.io](https://gitignore.io) or GitHub's templates as a
  starting point — then trim to what the project actually needs
- Do not ignore lockfiles — they MUST be committed
