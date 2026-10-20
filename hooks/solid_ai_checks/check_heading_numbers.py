"""Fail on a repeated or skipped ordinal in a numbered document.

Two branches can each add a section 3.9 to one document in regions git
merges without conflict. Each diff is correct; only the merged result is
wrong, so the check reads the result.
"""

import argparse
import os
import re

from .support.files import read_lines

# A numbered heading (### 3.9 Title) and a list ordinal (  4. Step).
HEADING = re.compile(r"^(#{1,6}) +([0-9]+(?:[.][0-9]+)*)[.]? ")
LISTITEM = re.compile(r"^[ \t]*([0-9]+)[.] ")
PLAIN = re.compile(r"^#{1,6} ")


def ordinals(lines):
    """Yield (line number, group key, value, label) for every ordinal."""
    group = "(top)"
    for number, line in enumerate(lines, 1):
        match = HEADING.match(line)
        if match:
            parts = match.group(2).split(".")

            # A heading is grouped under its parent, so 3.x and 4.x are
            # separate runs and each may restart.
            key = "%s %s" % (match.group(1), ".".join(parts[:-1]) or "(root)")
            group = line.strip()
            yield number, key, int(parts[-1]), match.group(2)
            continue
        if PLAIN.match(line):
            group = line.strip()
            continue
        match = LISTITEM.match(line)
        if match:
            yield number, group, int(match.group(1)), match.group(1)


def main(argv, report):
    parser = argparse.ArgumentParser(prog="check-heading-numbers")
    parser.add_argument("--path", action="append", default=[],
                        help="a numbered document to check; repeatable")
    args = parser.parse_args(argv)

    paths = report.count("documents inspected", args.path)
    if not paths:
        return report.not_applicable("no --path names a numbered document")

    total = 0
    for path in paths:
        if not os.path.isfile(path):
            report.finding(path, 0, "MISSING", "no such document")
            continue
        runs, found = {}, 0
        for number, key, value, label in ordinals(read_lines(path)):
            found += 1
            run = runs.setdefault(key, [])
            if value in run:
                report.finding(path, number, "REPEATED",
                               "%s repeats under %s" % (label, key))
            elif run and value != run[-1] + 1:
                report.finding(path, number, "SKIPPED",
                               "%s follows %s under %s"
                               % (label, run[-1], key))
            run.append(value)

        # A document with no ordinal means the pattern drifted from its
        # convention, not that its numbering is clean.
        if not found:
            report.finding(path, 0, "NO-ORDINALS",
                           "no ordinal found; the pattern drifted")
        total += found
    report.count("ordinals inspected", total)
    report.count("numbering problems", report.findings)
    return report.finish(bool(report.findings))
