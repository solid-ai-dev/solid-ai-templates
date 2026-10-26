"""Check that no figure about the tree sits in a document outside a generated block.

A count written into a sentence ("14 checks", "Eight files") is right the day it
is typed and wrong the next time the tree moves. Where a number carries the
point, `tools/sync_docs.py` emits it into a generated block its `--check` gates;
elsewhere a document names the thing without counting it.

Scans every tracked Markdown file except dated records (the changelog, the
journal, decision records, audits) and source material (templates and what is
generated from them). Skips fenced blocks, table rows, generated blocks and
passages marked `<!-- measured: YYYY-MM-DD -->` ... `<!-- /measured -->`.

Exits 0 when nothing is found, 1 on any finding or when no document was
reached. Runs as a local pre-commit hook; `--self-test` runs the planted cases.

Usage:
    py tools/check_doc_figures.py              # the tracked documents
    py tools/check_doc_figures.py --self-test  # the planted cases below
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

NOUNS = ("file", "files", "template", "templates", "stack", "stacks",
         "chain", "chains", "check", "checks", "test", "tests", "root",
         "roots", "directory", "directories", "document", "documents",
         "section", "sections", "example", "examples")

# Prose style spells a numeral under ten, which is where most counts fall.
# Below five it is an ordinary quantifier ("two templates") and states no
# measurement, so the list starts at five.
WORDS = ("five", "six", "seven", "eight", "nine", "ten", "eleven",
         "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
         "seventeen", "eighteen", "nineteen", "twenty", "dozen")

# A modifier may sit between the numeral and its noun ("14 manifest-reading
# checks"). A function word or a unit may not: "a 15 KB document" measures a
# size, not a population.
STOP = ("of|in|on|at|to|for|from|and|or|the|a|an|is|are|was|were|be"
        "|means|per|than|as|by|with|that|which|into|out|up|down|over"
        "|under|kb|mb|gb|kib|mib|byte|bytes|character|characters|word"
        "|words|line|lines|minute|minutes|second|seconds|token|tokens"
        "|page|pages")
GAP = r"(?:\s+(?!(?:%s)\b)[\w-]+){0,2}" % STOP
FIGURE = re.compile(r"(?<![\w.\-])(\d{1,6}|%s)%s\s+(%s)\b"
                    % ("|".join(WORDS), GAP, "|".join(NOUNS)), re.I)
GENERATED = re.compile(r"<!--\s*/?generated:")
MEASURED = re.compile(r"<!--\s*measured:\s*\d{4}-\d{2}-\d{2}")
MEASURED_END = re.compile(r"<!--\s*/measured\s*-->")
FENCE = re.compile(r"^\s*```")

# Dated records state what was true on their date.
HISTORY = ("CHANGELOG.md", "docs/dev-journal.md", "docs/decisions/",
           "docs/audits/")

# Roots whose numerals are the subject matter, not measurements.
SOURCES = ("templates/", "generated/", "examples/")


def figures(lines):
    """Yield (line number, numeral, noun) for each ungated figure."""
    generated = fenced = measured = False

    for number, line in enumerate(lines, 1):
        if FENCE.match(line):
            fenced = not fenced
            continue

        if GENERATED.search(line):
            generated = not generated
            continue

        # Matched separately: a toggle cannot tell which end it met, so an
        # unterminated record would exempt the rest of the file.
        if MEASURED.search(line):
            measured = True
            continue

        if MEASURED_END.search(line):
            measured = False
            continue

        if fenced or generated or measured or line.lstrip().startswith("|"):
            continue

        for hit in FIGURE.finditer(line):
            yield number, hit.group(1), hit.group(2)


def documents():
    """Return the tracked Markdown paths the check covers."""
    out = subprocess.check_output(["git", "ls-files", "-z", "*.md"])
    return sorted(p for p in out.decode("utf-8").split(chr(0))
                  if p.endswith(".md") and not p.startswith(HISTORY)
                  and not p.startswith(SOURCES))


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

        for number, numeral, noun in figures(lines):
            findings.append("%s:%d states '%s %s' outside a generated block"
                            % (rel, number, numeral, noun))

    print("documents scanned: %d" % len(paths))
    print("ungated figures: %d" % len(findings))

    for finding in findings:
        print(finding)

    return 1 if findings else 0


# (text, figures expected). Each case is one document's lines.
CASES = [
    (["The suite has 14 checks."], 1),
    (["Eight files moved."], 1),
    (["The 14 manifest-reading checks run."], 1),
    (["Two templates and four sections."], 0),
    (["A 15 KB document."], 0),
    (["| 14 checks | row |"], 0),
    (["```", "14 checks", "```"], 0),
    (["<!-- generated: x -->", "14 checks", "<!-- /generated: x -->"], 0),
    (["<!-- measured: 2026-10-20 -->", "14 checks", "<!-- /measured -->",
      "12 files"], 1),
]


def self_test():
    failed = 0

    for lines, expected in CASES:
        found = len(list(figures(lines)))

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
