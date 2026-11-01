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

Exits 0 when every pull request since the tag is accounted for, 1 when one
carries no `changelog:` label or two, and 2 when no previous tag exists.

Usage:
    py tools/cut_changelog.py                 # add the entries
    py tools/cut_changelog.py --dry-run       # print them, write nothing
    py tools/cut_changelog.py --cut v3.1.0    # add them, then cut
    py tools/cut_changelog.py --self-test     # the planted cases below
"""

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
OVERRIDE = re.compile(r"^Changelog:\s*(.+?)\s*$", re.MULTILINE)
NUMBER = re.compile(r"\(#(\d+)\)\s*$")


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

    A pull request already linked in the section is left alone, so a run
    repeated after new merges adds only what is new.
    """
    lines = text.split("\n")
    start, end = unreleased_span(lines)
    body = lines[start:end]
    listed = set(re.findall(r"\[#(\d+)\]", "\n".join(body)))
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
    """Rename `Unreleased` to the version and open an empty one above it."""
    return text.replace("## [Unreleased]",
                        "## [Unreleased]\n\n## [%s] - %s" % (version, day), 1)


def merged_since(tag):
    """The pull request numbers the squash subjects since `tag` name."""
    log = subprocess.run(["git", "log", "--format=%s", tag + "..HEAD"], **RUN)
    found = []
    for subject in log.stdout.splitlines():
        match = NUMBER.search(subject)
        if match:
            found.append(int(match.group(1)))
    return found


def fetch(number):
    """The title, labels and body of a pull request, through `gh`."""
    out = subprocess.run(["gh", "pr", "view", str(number), "--json",
                          "title,labels,body"], **RUN)
    if out.returncode != 0:
        raise SystemExit("cut_changelog: gh pr view %d failed: %s"
                         % (number, out.stderr.strip()))
    data = json.loads(out.stdout)
    return data["title"], [lab["name"] for lab in data["labels"]], data["body"]


def run(args):
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
    with open(RECORD, encoding="utf-8") as handle:
        text = handle.read()
    text, added = add_entries(text, entries)
    if "--cut" in args:
        version = args[args.index("--cut") + 1].lstrip("v")
        text = cut(text, version, datetime.date.today().isoformat())
    print("previous tag: %s" % tag)
    print("pull requests read: %d" % len(numbers))
    print("entries added: %d" % len(added))
    for line in unlabelled:
        print("no changelog label: %s" % line)
    if "--dry-run" not in args:
        with open(RECORD, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    return 1 if unlabelled else 0


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
