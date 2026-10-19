"""Check that the tree being tagged carries the changelog cut for a release.

Enforces the changelog-cut step of the playbook, "Release a new version": the
`Unreleased` section is cut into `## [A.B.C] - YYYY-MM-DD`, and the version
is the one SemVer names for that section against the previous tag. A patch
holds only `### Fixed` or `### Security`, a major holds
`### Breaking changes`, and a minor is anything else.

The changelog is read from HEAD, the commit the tag names, not from the
working tree. The previous release is the newest `v*` tag reachable from
HEAD other than the release itself, so the check runs the same at the
release commit and on the tag.

Exits 0 when the cut is complete and the version agrees, 1 on any finding,
and 2 when no release is named or no previous tag exists to compare with.

The release workflow also asks it two questions about a release: which
milestone names it, and what the release's notes are. Each prints its
answer and exits 1 when it cannot give one.

Usage:
    py tools/release_check.py v3.0.0              # the release being cut
    py tools/release_check.py --milestone v3.0.0  # the milestone naming it
    py tools/release_check.py --notes v3.0.0      # its changelog section
    py tools/release_check.py --self-test         # the planted cases below
"""

import os
import re
import subprocess
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", newline="\n")
    except (AttributeError, ValueError):
        pass

RECORD = "CHANGELOG.md"
VERSION = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
HEADING = re.compile(r"^## \[([^\]]+)\](?: - (\d{4}-\d{2}-\d{2}))?\s*$")
BULLET = re.compile(r"^\s*[-*] ")
PATCH_KINDS = {"Fixed", "Security"}
RUN = dict(capture_output=True, text=True, encoding="utf-8")


def sections(text):
    """Map each `## [name]` heading to its date and body lines."""
    found, name = {}, None
    for line in text.splitlines():
        match = HEADING.match(line)
        if match:
            name = match.group(1)
            found.setdefault(name, []).append((match.group(2), []))
        elif line.startswith("## "):
            name = None
        elif name is not None:
            found[name][-1][1].append(line)
    return found


def bump(previous, release):
    """Name the SemVer step from one version tuple to the next, or None."""
    if release == (previous[0] + 1, 0, 0):
        return "major"
    if release == (previous[0], previous[1] + 1, 0):
        return "minor"
    if release == (previous[0], previous[1], previous[2] + 1):
        return "patch"
    return None


def findings(text, release, previous):
    """Return what keeps `text` from being the cut for `release`."""
    out = []
    version = "%d.%d.%d" % release
    found = sections(text)
    cut = found.get(version, [])
    if len(cut) != 1:
        out.append("%s holds %d section(s) named [%s], expected 1"
                   % (RECORD, len(cut), version))
        return out
    date, body = cut[0]
    if date is None:
        out.append("[%s] carries no date" % version)
    entries = [line for line in body if BULLET.match(line)]
    if not entries:
        out.append("[%s] holds no entries" % version)
    for _, unreleased in found.get("Unreleased", []):
        left = [line for line in unreleased if BULLET.match(line)]
        if left:
            out.append("Unreleased still holds %d entr%s the cut did not "
                       "carry" % (len(left), "y" if len(left) == 1 else "ies"))
    kinds = {line[4:].strip() for line in body if line.startswith("### ")}
    if "Breaking changes" in kinds:
        owed = "major"
    elif kinds and kinds <= PATCH_KINDS:
        owed = "patch"
    else:
        owed = "minor"
    step = bump(previous, release)
    if step is None:
        out.append("v%s does not follow v%d.%d.%d by one SemVer step"
                   % ((version,) + previous))
    elif step != owed:
        out.append("v%s is a %s, but [%s] holds %s, which owes a %s"
                   % (version, step, version, sorted(kinds), owed))
    return out


def previous_tag(release_name):
    """The newest `v*` tag reachable from HEAD other than the release."""
    proc = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0", "--match", "v*",
         "--exclude", release_name, "HEAD"], **RUN)
    return proc.stdout.strip() if proc.returncode == 0 else None


def check(release_name):
    match = VERSION.match(release_name or "")
    if not match:
        print("no release named as vA.B.C (got %r); nothing was checked"
              % release_name)
        return 2
    previous_name = previous_tag(release_name)

    # A baseline the command did not produce is not a baseline: with no
    # earlier tag the bump cannot be read, and reporting it as agreeing
    # would pass a version nothing was compared with.
    if previous_name is None or not VERSION.match(previous_name):
        print("no previous v* tag is reachable from HEAD, so the bump "
              "cannot be compared")
        return 2
    shown = subprocess.run(["git", "show", "HEAD:" + RECORD], **RUN)
    if shown.returncode != 0:
        print("HEAD carries no %s" % RECORD)
        return 1
    release = tuple(int(n) for n in match.groups())
    previous = tuple(int(n) for n in VERSION.match(previous_name).groups())
    print("release: %s" % release_name)
    print("previous release: %s" % previous_name)
    print("changelog read from: HEAD:%s" % RECORD)
    found = findings(shown.stdout, release, previous)
    print("findings: %d" % len(found))
    for line in found:
        print("  " + line)
    return 1 if found else 0


def named(version, titles):
    """The titles naming `version` alone or before " — " and a theme."""
    return [title for title in titles
            if title == version or title.startswith(version + " — ")]


def milestone(release_name, titles):
    """Return the one title naming the release, or None if none does.

    Raises ValueError when more than one title names it.
    """

    # A minor's milestone names the minor line and a patch's the full
    # version, so the full version wins and the minor line is the fallback.
    # Matching the separator rather than a bare prefix stops v2.8 claiming
    # every v2.8x title.
    found = named(release_name, titles)
    if not found:
        found = named(".".join(release_name.split(".")[:2]), titles)
    if len(found) > 1:
        raise ValueError("more than one milestone names %s: %s"
                         % (release_name, "; ".join(found)))
    return found[0] if found else None


def print_milestone(release_name):
    repo = os.environ.get("GITHUB_REPOSITORY") or "{owner}/{repo}"
    proc = subprocess.run(
        ["gh", "api", "repos/%s/milestones?state=all" % repo, "--paginate",
         "--jq", ".[].title"], **RUN)

    # A failed listing is not an empty one: reading it as no milestone
    # would report a release scoped to one as scoped to none.
    if proc.returncode != 0:
        print("the milestones could not be listed: %s" % proc.stderr.strip(),
              file=sys.stderr)
        return 1
    try:
        title = milestone(release_name, proc.stdout.splitlines())
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    print(title or "")
    return 0


def notes(text, version):
    """Return the body of the one `## [version]` section, or None."""
    cut = sections(text).get(version, [])
    if len(cut) != 1:
        return None
    return "\n".join(cut[0][1]).strip("\n")


def print_notes(release_name):
    match = VERSION.match(release_name or "")
    shown = subprocess.run(["git", "show", "HEAD:" + RECORD], **RUN)
    body = notes(shown.stdout, release_name[1:]) if match else None
    if shown.returncode != 0 or not body:
        print("HEAD:%s holds no single section for %r"
              % (RECORD, release_name), file=sys.stderr)
        return 1
    print(body)
    return 0


CUT = """## [Unreleased]

## [3.0.0] - 2026-10-20

### Breaking changes

- Stacks move to forks.

## [2.90.0] - 2026-09-12
"""

# Each case is (name, changelog, release, previous, the one finding owed as
# a fragment of its text, or None for a clean cut). Matching the text rather
# than the count keeps a case from passing on a finding other than its own.
CASES = [
    ("a complete major cut", CUT, (3, 0, 0), (2, 90, 0), None),
    ("no section for the release", CUT, (3, 1, 0), (3, 0, 0),
     "0 section(s) named [3.1.0]"),
    ("a minor where the section owes a major", CUT.replace(
        "3.0.0", "2.91.0"), (2, 91, 0), (2, 90, 0), "owes a major"),
    ("a skipped version", CUT.replace("## [2.90.0] - 2026-09-12\n", "")
     .replace("3.0.0", "2.90.0").replace("Breaking changes", "Added"),
     (2, 90, 0), (2, 88, 0), "does not follow v2.88.0 by one SemVer step"),
    ("entries left under Unreleased", CUT.replace(
        "## [Unreleased]\n", "## [Unreleased]\n\n- Left behind.\n"),
     (3, 0, 0), (2, 90, 0), "Unreleased still holds 1 entry"),
    ("an undated section", CUT.replace(" - 2026-10-20", ""),
     (3, 0, 0), (2, 90, 0), "carries no date"),
    ("a patch holding only fixes", CUT.replace("3.0.0", "2.90.1").replace(
        "Breaking changes", "Fixed"), (2, 90, 1), (2, 90, 0), None),
    ("a patch holding an addition", CUT.replace("3.0.0", "2.90.1").replace(
        "Breaking changes", "Added"), (2, 90, 1), (2, 90, 0), "owes a minor"),
]


TITLES = ["v2.8 — Old line", "v2.80 — Later line", "v2.90.1 — A patch",
          "v2.90 — Benchmark", "v3.0 — The split"]

# Each case is (name, titles, release, the title owed, or None for no
# milestone, or ValueError when the titles are ambiguous).
MILESTONE_CASES = [
    ("a minor resolves to its line", TITLES, "v3.0.0", "v3.0 — The split"),
    ("a patch's own milestone wins", TITLES, "v2.90.1", "v2.90.1 — A patch"),
    ("a patch without one falls back to its line", TITLES, "v2.90.2",
     "v2.90 — Benchmark"),
    ("v2.8 does not claim v2.80's title", TITLES, "v2.8.0",
     "v2.8 — Old line"),
    ("a bare title names its release", ["v3.1"], "v3.1.0", "v3.1"),
    ("no milestone names the release", TITLES, "v4.0.0", None),
    ("two titles name the release", TITLES + ["v3.0 — Again"], "v3.0.0",
     ValueError),
]

# Each case is (name, changelog, version, the notes owed, or None).
NOTES_CASES = [
    ("the section's body, trimmed", CUT, "3.0.0",
     "### Breaking changes\n\n- Stacks move to forks."),
    ("no section for the version", CUT, "3.1.0", None),
    ("two sections for the version", CUT + CUT[16:], "3.0.0", None),
]


def self_test():
    failed = 0

    def report(ok, name, got):
        print("  %s  %s: %s" % ("ok  " if ok else "FAIL", name, got))
        return not ok

    for name, text, release, previous, owed in CASES:
        got = findings(text, release, previous)
        if owed is None:
            ok = not got
        else:
            ok = len(got) == 1 and owed in got[0]
        failed += report(ok, name, "; ".join(got) or "clean")
    for name, titles, release, owed in MILESTONE_CASES:
        try:
            got = milestone(release, titles)
        except ValueError as error:
            got = error
        ok = (isinstance(got, ValueError) if owed is ValueError
              else got == owed)
        failed += report(ok, name, got)
    for name, text, version, owed in NOTES_CASES:
        got = notes(text, version)
        failed += report(got == owed, name, repr(got))
    total = len(CASES) + len(MILESTONE_CASES) + len(NOTES_CASES)
    print("VERDICT: %s - %d case(s), %d failed"
          % ("PASS" if not failed else "FAIL", total, failed))
    return 1 if failed else 0


ACTIONS = {"--milestone": print_milestone, "--notes": print_notes}


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--self-test"]:
        raise SystemExit(self_test())
    if len(args) == 2 and args[0] in ACTIONS:
        raise SystemExit(ACTIONS[args[0]](args[1]))
    name = args[0] if args else os.environ.get("RELEASE")
    raise SystemExit(check(name))
