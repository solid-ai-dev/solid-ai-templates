"""Check that no tracked Markdown file carries a horizontal rule.

Headings already separate the sections, so a rule between them is noise, and
every chain that loads a template pays for it in tokens. A rule is `---`,
`***` or `___` (three or more, spaces allowed) on a line of its own.

Scans every tracked Markdown file. Skips YAML frontmatter, fenced blocks and
setext heading underlines, a `---` directly under a line of paragraph text.

Exits 0 when nothing is found, 1 on any finding or when no document was
reached. Runs as a local pre-commit hook; `--self-test` runs the planted cases.

Usage:
    py tools/check_horizontal_rules.py              # the tracked documents
    py tools/check_horizontal_rules.py --self-test  # the planted cases below
"""

import pathlib
import re
import subprocess
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", newline="\n")
    except (AttributeError, ValueError):
        pass

RULE = re.compile(r"^ {0,3}([-*_])(?:[ \t]*\1){2,}[ \t]*$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")

# A line that opens a block of its own. A `---` under one of these is a
# rule; under any other text it underlines a setext heading.
BLOCK_START = re.compile(r"^\s*(#|>|\||[-*+]\s|\d+[.)]\s)")


def rules(lines):
    """Yield the 1-based line number of each horizontal rule."""
    fence = None
    start = 0

    # Frontmatter opens on the first line and closes on the next `---`.
    if lines and lines[0].strip() == "---":
        for number, line in enumerate(lines[1:], 2):
            if line.strip() in ("---", "..."):
                start = number
                break

    for number, line in enumerate(lines, 1):
        if number <= start:
            continue

        opener = FENCE.match(line)

        if fence:
            if opener and opener.group(1)[0] == fence[0] \
                    and len(opener.group(1)) >= len(fence) \
                    and not line.strip()[len(opener.group(1)):].strip():
                fence = None
            continue

        if opener:
            fence = opener.group(1)
            continue

        if not RULE.match(line):
            continue

        previous = lines[number - 2] if number > 1 else ""
        setext = (line.strip()[0] == "-" and previous.strip()
                  and not BLOCK_START.match(previous))

        if not setext:
            yield number


def documents():
    """Return the tracked Markdown paths."""
    out = subprocess.check_output(["git", "ls-files", "-z", "*.md"])
    return sorted(p for p in out.decode("utf-8").split(chr(0))
                  if p.endswith(".md"))


def check():
    paths = documents()

    # An empty list means the pathspec reached nothing, which would report
    # zero findings from a scan that never ran.
    if not paths:
        print("no tracked Markdown reached; the pathspec drifted")
        return 1

    findings = []

    for rel in paths:
        lines = pathlib.Path(rel).read_text(encoding="utf-8").splitlines()

        for number in rules(lines):
            findings.append("%s:%d is a horizontal rule" % (rel, number))

    print("documents scanned: %d" % len(paths))
    print("horizontal rules: %d" % len(findings))

    for finding in findings:
        print(finding)

    return 1 if findings else 0


# (text, rules expected). Each case is one document's lines.
CASES = [
    (["# A", "", "---", "", "# B"], 1),
    (["text", "", "***"], 1),
    (["text", "", "_ _ _"], 1),
    (["- item", "---"], 1),
    (["---", "title: x", "---", "", "body"], 0),
    (["Heading", "---"], 0),
    (["```", "---", "```"], 0),
    (["````", "```", "---", "````"], 0),
    (["~~~", "***", "~~~"], 0),
    (["| a |", "|---|"], 0),
    (["    ---"], 0),
]


def self_test():
    failed = 0

    for lines, expected in CASES:
        found = len(list(rules(lines)))

        if found != expected:
            failed += 1
            print("FAIL %r: expected %d, found %d" % (lines, expected, found))

    print("VERDICT: %s - %d case(s), %d failed"
          % ("FAIL" if failed else "PASS", len(CASES), failed))
    return 1 if failed else 0


def main(args):
    if "--self-test" in args:
        return self_test()

    if args:
        print("unknown argument: %s" % " ".join(args))
        return 2

    return check()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
