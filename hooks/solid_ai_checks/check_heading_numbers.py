"""Fail on a repeated or skipped ordinal in a numbered document.

Two branches can each add a section 3.9 to one document in regions git
merges without conflict. Each diff is correct; only the merged result is
wrong, so the check reads the result.
"""

import argparse
import itertools
import os
import re

from .support.fences import spans
from .support.files import read_lines

# A numbered heading (### 3.9 Title) and a list ordinal (  4. Step).
HEADING = re.compile(r"^(#{1,6}) +([0-9]+(?:[.][0-9]+)*)[.]? ")
LISTITEM = re.compile(r"^([ \t]*)([0-9]+)[.] ")
PLAIN = re.compile(r"^#{1,6} ")


class Lists:
    """The ordered lists open under one heading, outermost first.

    Each list is a run of its own, so a nested 1. 2. does not repeat the
    outer 1. 2., and a new list starting at 1 does not repeat the last.
    An open list is (marker column, text column, run key).
    """

    def __init__(self, group, serials):
        self.group = group
        self.serials = serials
        self.open = []
        self.closed = {}

    def _close(self):
        key = self.open.pop()[2]
        self.closed[len(self.open)] = key

    def end_at(self, indent):
        """Close every list whose item text a line at `indent` ends."""
        while self.open and self.open[-1][1] > indent:
            self._close()

    def key(self, indent, width, value):
        """The run key of an item whose marker, `width` wide, is at `indent`."""
        while self.open and indent < self.open[-1][0]:
            self._close()
        depth = len(self.open)
        if self.open and indent < self.open[-1][1]:
            depth -= 1

        # A list closed under an earlier item is that item's own, so it
        # never continues into the next one.
        for deeper in [d for d in self.closed if d > depth]:
            del self.closed[deeper]
        if depth < len(self.open):
            return self.open[depth][2]

        # A list that does not start at 1 continues the last one closed at
        # its depth, as a step after a flush code block carries on the
        # numbering, so a skip or a repeat across the break is still found.
        key = self.closed.pop(depth, None)
        if key is None or value == 1:
            key = (self.group, next(self.serials))
        self.open.append((indent, indent + width, key))
        return key


def ordinals(lines):
    """Yield (line number, group key, value, label) for every ordinal.

    A group key is a (label, serial) pair, so two runs under one heading
    stay apart. Fenced content is an example, never the document's own
    numbering.
    """
    fenced = {opening: (closing, indent)
              for opening, closing, indent, _ in spans(lines)}
    serials = itertools.count(1)
    lists = Lists("(top)", serials)
    n = 0
    while n < len(lines):
        line, number = lines[n], n + 1
        if n in fenced:
            closing, indent = fenced[n]
            lists.end_at(indent)
            n = closing + 1
            continue
        n += 1
        match = HEADING.match(line)
        if match:
            parts = match.group(2).split(".")

            # A heading is grouped under its parent, so 3.x and 4.x are
            # separate runs and each may restart.
            key = "%s %s" % (match.group(1), ".".join(parts[:-1]) or "(root)")
            lists = Lists(line.strip(), serials)
            yield number, (key, 0), int(parts[-1]), match.group(2)
            continue
        if PLAIN.match(line):
            lists = Lists(line.strip(), serials)
            continue
        match = LISTITEM.match(line)
        if match:
            indent = len(match.group(1).expandtabs(4))
            width = len(match.group(2)) + 2
            key = lists.key(indent, width, int(match.group(2)))
            yield number, key, int(match.group(2)), match.group(2)
        elif line.strip():
            text = line.expandtabs(4)
            lists.end_at(len(text) - len(text.lstrip()))


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
                               "%s repeats under %s" % (label, key[0]))
            elif run and value != run[-1] + 1:
                report.finding(path, number, "SKIPPED",
                               "%s follows %s under %s"
                               % (label, run[-1], key[0]))
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
