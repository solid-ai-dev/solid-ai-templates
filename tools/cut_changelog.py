"""Write the changelog's entries from the labels of the merged pull requests.

Each pull request carries one `changelog:` label naming the section its
entry belongs to, or `changelog:none` when a consuming project would not
notice it. This reads the pull requests merged since the previous `v*` tag
from the squash subjects, which end with the pull request number, and adds
an entry to the `Unreleased` section for each labelled one not yet listed
there. The entry is the title without its `type(scope):` prefix and issue
numbers, or the text of a `Changelog:` line in the body, which overrides it.

`--cut vA.B.C` then renames `Unreleased` to `## [A.B.C] - YYYY-MM-DD` and
opens an empty `Unreleased` above it; `tools/check_release.py` checks the
cut and the SemVer step.

Exits 0 when every pull request since the tag is accounted for and the file
is written, 1 when one carries no `changelog:` label or two, or the cut is
refused, and 2 when no previous tag exists or `--cut` names no vA.B.C.
Nothing is written on 1 or 2.

Usage:
    py tools/cut_changelog.py                 # add the entries
    py tools/cut_changelog.py --dry-run       # print them, write nothing
    py tools/cut_changelog.py --cut v3.1.0    # add them, then cut
    py tools/cut_changelog.py --self-test     # the planted cases below
"""

import argparse
import datetime
import json
import re
import subprocess
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", newline="\n")
    except (AttributeError, ValueError):
        pass

RECORD = "CHANGELOG.md"
REPO = "https://github.com/solid-ai-dev/solid-ai-templates/pull/"
RUN = dict(capture_output=True, text=True, encoding="utf-8")

# Pull requests before this one carry hand-written entries, so the
# generator leaves them alone; from this one on, the label decides.
LABELS_SINCE = 2431

# Label suffix to section heading, in the order the sections appear.
SECTIONS = {
    "breaking": "Breaking changes",
    "added": "Added",
    "changed": "Changed",
    "deprecated": "Deprecated",
    "fixed": "Fixed",
    "security": "Security",
}
PREFIX = re.compile(r"^[a-z]+(\([^)]*\))?!?:\s*")
ISSUES = re.compile(r"(\s*\(#\d+(?:,\s*#\d+)*\))+\s*$")
# Same-line text only: a bare `Changelog:` must not take the next line.
OVERRIDE = re.compile(r"^Changelog:[ \t]*(\S[^\n]*?)[ \t]*$", re.MULTILINE)
NUMBER = re.compile(r"\(#(\d+)\)\s*$")
VERSION = re.compile(r"^v(\d+\.\d+\.\d+)$")
BOTS = {"app/dependabot", "dependabot[bot]", "dependabot"}


def entry_text(title, body=""):
    """The plain-words entry for a pull request."""
    override = OVERRIDE.search(body or "")
    text = override.group(1) if override else ISSUES.sub(
        "", PREFIX.sub("", title.strip()))
    return text[:1].upper() + text[1:]


def section_of(labels):
    """The section a pull request's labels name: a heading, '' or None.

    '' means `changelog:none`; None means no label or more than one.
    """
    kinds = [n.split(":", 1)[1].strip() for n in labels
             if n.startswith("changelog:")]
    if len(kinds) != 1:
        return None
    if kinds[0] == "none":
        return ""
    return SECTIONS.get(kinds[0])


def unreleased_span(lines):
    """The index range of the `Unreleased` section's body."""
    start = next(i for i, line in enumerate(lines)
                 if line.startswith("## [Unreleased]"))
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("## [")), len(lines))
    return start + 1, end


def add_entries(text, entries):
    """Add (heading, number, text) entries to `Unreleased`, with their links.

    A pull request already linked anywhere in the file is left alone, so a
    run repeated after new merges, or after a cut not yet tagged, adds only
    what is new.
    """
    lines = text.split("\n")
    start, end = unreleased_span(lines)
    body = lines[start:end]
    listed = set(re.findall(r"\[#(\d+)\]", text))
    links = [i for i, line in enumerate(body) if re.match(r"^\[#\d+\]: ", line)]
    content = body[:links[0]] if links else body
    refs = body[links[0]:] if links else []
    added = []
    for heading, number, words in entries:
        if str(number) in listed:
            continue
        listed.add(str(number))
        added.append(number)
        bullet = "- %s ([#%d])" % (words, number)
        marker = "### " + heading
        if marker not in content:
            # Place a new heading before the first later one, in order.
            order = list(SECTIONS.values())
            later = [h for h in order[order.index(heading) + 1:]]
            at = next((i for i, line in enumerate(content)
                       if line[4:] in later and line.startswith("### ")),
                      None)
            block = [marker, "", bullet, ""]
            if at is None:
                while content and content[-1] == "":
                    content.pop()
                content += [""] + block
            else:
                content[at:at] = block
            continue
        at = content.index(marker) + 1
        while at < len(content) and not content[at].startswith("### "):
            at += 1
        while content[at - 1] == "":
            at -= 1
        content.insert(at, bullet)
    # The section is rebuilt as entries, a blank line, the links and a
    # blank line, so a run that adds nothing leaves the file unchanged.
    while refs and refs[-1] == "":
        refs.pop()
    refs += ["[#%d]: %s%d" % (n, REPO, n) for n in added]
    while content and content[-1] == "":
        content.pop()
    tail = [""] + refs + [""] if refs else [""]
    lines[start:end] = content + tail
    return "\n".join(lines), added


def cut(text, version, day):
    """Rename `Unreleased` to the version and open an empty one above it.

    Refuses a version already in the file and an `Unreleased` with no
    entry, which `tools/check_release.py` would refuse at the tag.
    """
    if "## [%s]" % version in text:
        raise ValueError("the changelog already has a %s section" % version)
    lines = text.split("\n")
    start, end = unreleased_span(lines)
    if not any(line.startswith("- ") for line in lines[start:end]):
        raise ValueError("Unreleased holds no entry to cut")
    return text.replace("## [Unreleased]",
                        "## [Unreleased]\n\n## [%s] - %s" % (version, day), 1)


def merged_since(tag):
    """The pull request numbers the squash subjects since `tag` name."""
    log = subprocess.run(["git", "log", "--format=%s", tag + "..HEAD"], **RUN)
    if log.returncode != 0:
        raise SystemExit("cut_changelog: git log %s..HEAD failed: %s"
                         % (tag, log.stderr.strip()))
    found = []
    for subject in log.stdout.splitlines():
        match = NUMBER.search(subject)
        if match:
            found.append(int(match.group(1)))
    return found


def fetch(number):
    """The title, labels and body of a pull request, through `gh`.

    A dependency bump carries no entry, and the label gate exempts its
    author, so it reads as `changelog:none` here.
    """
    out = subprocess.run(["gh", "pr", "view", str(number), "--json",
                          "title,labels,body,author"], **RUN)
    if out.returncode != 0:
        raise SystemExit("cut_changelog: gh pr view %d failed: %s"
                         % (number, out.stderr.strip()))
    data = json.loads(out.stdout)
    labels = [lab["name"] for lab in data["labels"]]
    if (data.get("author") or {}).get("login") in BOTS:
        labels = ["changelog:none"]
    return data["title"], labels, data["body"]


def run(args):
    parser = argparse.ArgumentParser(prog="cut_changelog")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cut", metavar="vA.B.C")
    options = parser.parse_args(args)
    version = None
    if options.cut is not None:
        match = VERSION.match(options.cut)
        if not match:
            print("cut_changelog: --cut takes vA.B.C, not %r" % options.cut)
            return 2
        version = match.group(1)
    tag = subprocess.run(["git", "describe", "--tags", "--abbrev=0",
                          "--match", "v*"], **RUN).stdout.strip()
    if not tag:
        print("cut_changelog: no previous v* tag to read from")
        return 2
    numbers = [n for n in merged_since(tag) if n >= LABELS_SINCE]
    entries, unlabelled = [], []
    for number in sorted(numbers):
        title, labels, body = fetch(number)
        heading = section_of(labels)
        if heading is None:
            unlabelled.append("#%d %s" % (number, title))
        elif heading:
            entries.append((heading, number, entry_text(title, body)))
    print("previous tag: %s" % tag)
    print("pull requests read: %d" % len(numbers))

    # A cut with an unlabelled pull request would publish a release that
    # silently lacks its entry, so nothing is written until all are labelled.
    if unlabelled:
        for line in unlabelled:
            print("no changelog label: %s" % line)
        print("nothing written; label them and run again")
        return 1
    with open(RECORD, encoding="utf-8") as handle:
        text = handle.read()
    text, added = add_entries(text, entries)
    print("entries added: %d" % len(added))
    if version:
        try:
            text = cut(text, version, datetime.date.today().isoformat())
        except ValueError as error:
            print("cut_changelog: %s; nothing written" % error)
            return 1
        print("cut: %s" % version)
    if not options.dry_run:
        with open(RECORD, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    return 0


def self_test():
    sample = ("# Changelog\n\n## [Unreleased]\n\n### Added\n\n"
              "- Old entry ([#10])\n\n### Fixed\n\n- Old fix ([#11])\n\n"
              "[#10]: %s10\n[#11]: %s11\n\n## [1.0.0] - 2026-01-01\n\n"
              "### Added\n\n- First ([#1])\n" % (REPO, REPO))
    cases = []
    cases.append(("the prefix and issue numbers are dropped",
                  entry_text("feat(tools): emit the skills (#12) (#13)")
                  == "Emit the skills"))
    cases.append(("a Changelog line overrides the title",
                  entry_text("docs: x (#1)", "Body\nChangelog: Plain words\n")
                  == "Plain words"))
    cases.append(("one label names its section",
                  section_of(["P2", "changelog:fixed"]) == "Fixed"))
    cases.append(("changelog:none names no section",
                  section_of(["changelog:none"]) == ""))
    cases.append(("no label, or two, is refused",
                  section_of(["task"]) is None
                  and section_of(["changelog:added", "changelog:fixed"])
                  is None))
    text, added = add_entries(sample, [("Added", 20, "New thing"),
                                       ("Added", 10, "Duplicate")])
    unreleased = text.split("## [1.0.0]")[0]
    cases.append(("an entry joins its section, a listed one is skipped",
                  added == [20] and "- New thing ([#20])" in unreleased
                  and "Duplicate" not in text
                  and unreleased.index("[#20])") < unreleased.index(
                      "### Fixed")))
    cases.append(("its link joins the section's links",
                  "[#20]: %s20" % REPO in unreleased))
    text, _ = add_entries(sample, [("Breaking changes", 30, "Big change")])
    cases.append(("a missing section is opened in its place",
                  text.index("### Breaking changes")
                  < text.index("### Added")))
    text, _ = add_entries(sample, [("Security", 31, "Patched")])
    cases.append(("a last section goes after the others",
                  text.index("### Fixed") < text.index("### Security")
                  < text.index("[#10]:")))
    cases.append(("a bare Changelog line leaves the title as the entry",
                  entry_text("feat: emit skills (#1)",
                             "Changelog:\n\nCloses #2") == "Emit skills"))
    emptied = (sample.replace("- Old entry ([#10])", "")
               .replace("- Old fix ([#11])", ""))
    refused = []
    for text_in, version in ((sample, "1.0.0"), (emptied, "1.1.0")):
        try:
            cut(text_in, version, "2026-02-02")
        except ValueError:
            refused.append(version)
    cases.append(("the cut refuses a known version and an empty section",
                  refused == ["1.0.0", "1.1.0"]))
    cases.append(("a pull request linked in an earlier section is skipped",
                  add_entries(sample, [("Added", 1, "Again")])[1] == []))
    cases.append(("a run that adds nothing leaves the file unchanged",
                  add_entries(sample, [])[0] == sample))
    cases.append(("the cut keeps an empty Unreleased above the version",
                  "## [Unreleased]\n\n## [1.1.0] - 2026-02-02"
                  in cut(sample, "1.1.0", "2026-02-02")))
    failed = [name for name, ok in cases if not ok]
    for name, ok in cases:
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
    print("VERDICT: %s - %d case(s), %d failed"
          % ("FAIL" if failed else "PASS", len(cases), len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(run(sys.argv[1:]))
