# Base — Git Conventions

[ID: base-git]

How changes are committed, reviewed, verified and merged.

## Commits

- Commit under your full name and one consistent work email; never change
  identity mid-project
- Work on a branch; never commit directly to `main`
- Never commit build output, dependency directories, reproducible
  generated files or secrets
- Treat every repository as public: no secret, credential or sensitive
  value in source or history
- Keep a `.gitignore` (MUST) covering dependencies, build output, secrets,
  editor state, OS files and coverage output
- Track the shared editor settings that mirror the CI gates; ignore the
  rest of the editor's state
- Commit lockfiles (MUST)

## Pull requests

- Keep a pull request to one concern
- Test locally before committing
- Review the diff against the base before merging, in the order security,
  correctness, clarity, conventions
- Merge only after the review passes and CI is green

## CI evidence

- Read the CI run for the push before describing a change as good; a local
  run is evidence about one platform
- Treat a pull request with no registered check as not passed: wait until
  one registers, then watch every check to completion

```bash
PR=<N>
count=0
for _ in $(seq 1 60); do
  count=$(gh pr checks "$PR" --json name --jq 'length' 2>/dev/null)
  [ "${count:-0}" -gt 0 ] && break
  sleep 5
done
echo "checks registered: ${count:-0}"
[ "${count:-0}" -gt 0 ] || exit 1
gh pr checks "$PR" --watch > /dev/null
watched=$?
failing=$(gh pr checks "$PR" --json bucket --jq '[.[] | select(.bucket != "pass" and .bucket != "skipping")] | length')
echo "checks not passing: $failing"
[ "$watched" -eq 0 ] && [ "$failing" -eq 0 ]
```

Pass condition: `checks registered` is above zero, `checks not passing` is
zero, and the block exits zero. No check registered after five minutes, or
any failing or cancelled check, exits non-zero and the pull request does not
merge.

- Re-run a verification a pull request body claims, rather than reading
  it, whenever the base has advanced since the body was written; above all
  a proof of absence

## Updating a branch

- Never force-push, including with `--force-with-lease` (MUST NOT)
- Bring a branch up to date by merging the base into it, or with
  `gh pr update-branch <N>`; never rebase and force-push
- Regenerate derived artifacts and re-run the staleness comparison after
  every such merge, and stage what they produce

## Regenerated artifacts

- Regenerate a derived artifact in the change that edits its source, and
  stage both together (MUST)
- Name the regeneration trigger beside the sources it derives from (MUST)
- Run the staleness comparison after the edit, and again after merging the
  base in (MUST)

```bash
<regenerate-command>
git diff --exit-code --stat -- <artifact-path>
```

Pass condition: no diff, on a zero status. Any output means the committed
artifact does not match its sources. A regenerator that is not idempotent
fails this on a current artifact, which is a generator defect.

- Put a before-and-after summary of the visible impact in the pull request
  body: a verdict matrix, a delta table, a screenshot diff
- Open a tracked follow-up and state the stale files, by name or glob,
  where regeneration is too expensive to bundle (MUST)
- Never regenerate a bidirectional artifact, one an ingest or `--apply`
  step reads back into the source, from the pipeline it feeds; refresh it
  through the step a person owns, and flag it stale
- Drop a regenerated file whose diff is whitespace or line endings only:

```bash
git diff --ignore-all-space <file>
```

An empty diff marks the change as noise; `git checkout -- <file>` drops it.

- Open every regenerated binary artifact in a viewer, or an image-read
  tool, and confirm it tracks its source
- Regenerate a known-current control artifact first; a non-zero diff there
  means the environment disagrees with the committed files
- Pair a spot-check of three to five representative artifacts with one
  metric across the whole population

## Off-limits paths

- Declare an Off-limits section in the project's context file, listing the
  paths that MUST NOT change without explicit approval (MUST)
- Offer this default set for the project to cut down: auth and session
  code, payment code, database migrations, `.env*` and secret handling,
  CI/CD workflows, and the pointer to a vendored rules submodule
- Propose a change inside an off-limits path before making it, with a
  rollback strategy and the tests that would catch a regression (MUST)
- Apply the restriction to executable content: steps, commands, flags,
  permissions, triggers, pins and a vendored pointer's revision; a diff
  confined to prose is ordinary work
- Treat a comment a tool reads as executable: `# noqa`, `# nosec`, a
  linter disable, a coverage pragma
- Classify by the diff: it is prose only when removing every comment line
  leaves nothing
- Name an off-limits path at the top of the change's summary whenever the
  diff touches one, proposal or not (MUST)

```bash
pre-commit run report-off-limits-paths --hook-stage manual --all-files --verbose
```

Pass condition: the paths-declared and files-changed counts are above zero.
Each path is a `--path` argument, kept beside the declared list; `--base`
defaults to `origin/main`. Every off-limits line is an escalation to state
in the summary, not a failure. Run it after committing: on the base with a
clean tree it prints `not applicable`, and a base that does not resolve
fails it.
