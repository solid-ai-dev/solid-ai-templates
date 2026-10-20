"""Find a check stated in prose rather than in a fenced block.

A check typed into a sentence cannot be extracted, counted or run, so a
tool that runs the fenced checks reports clean over a rule nobody runs.
"""

import argparse
import re

from .files import read_lines, tracked

# A stated check pairs a verification phrase with the command it
# introduces. The pair is matched over a paragraph, because a wrapped check
# puts the phrase on one line and the command on the next.
PHRASE = re.compile(
    r"(?:verify|check|confirm)\s+with"
    r"|(?:verified|checked|confirmed)\s+by"
    r"|pass condition"
    r"|\b(?:[\w-]+\s+)?checks?:",
    re.IGNORECASE)
COMMAND = re.compile(r"[`][^`]+[`]")

# The other order: the command comes first and its pass condition after it,
# with no announcing phrase at all.
VERDICT = re.compile(
    r"output\s+must\s+be\s+empty"
    r"|\bno\s+output\s+means"
    r"|\bis\s+done\s+when",
    re.IGNORECASE)

# A sentence boundary between the phrase and the command means the
# paragraph talks ABOUT a check and names a command somewhere else.
BREAK = re.compile(r"[.]\s")

# A paragraph this close to a fence is the prose beside a fenced check.
WINDOW = 5

FENCE = "`" * 3
BULLET = re.compile(r"\s*(?:[-*+]\s|\d+[.]\s)")


def examine(path, para, numbers, marks, report):
    """Record a finding where the paragraph states a check no fence holds."""
    if not para:
        return 0
    near = (min(min(abs(m - n) for m in marks) for n in numbers)
            if marks else WINDOW + 1)
    if near <= WINDOW:
        return 1
    joined = " ".join(line.strip() for line in para)
    pairs = [(p, COMMAND.search(joined, p.end()))
             for p in PHRASE.finditer(joined)]
    pairs += [(c, VERDICT.search(joined, c.end()))
              for c in COMMAND.finditer(joined)]
    for first, second in pairs:
        if second and not BREAK.search(joined[first.end():second.start()]):
            report.finding(path, numbers[0], "UNFENCED",
                           joined[first.start():second.end()])
            break
    return 1


def main(argv, report):
    parser = argparse.ArgumentParser(prog="find-unfenced-checks")
    parser.add_argument("--root", action="append", default=[],
                        help="directory holding rule documents; repeatable")
    args = parser.parse_args(argv)

    files = report.count("markdown files scanned",
                         tracked([".md"], args.root))
    inspected = 0
    for path in files:
        lines = read_lines(path)
        marks = [n for n, line in enumerate(lines, 1)
                 if line.lstrip().startswith(FENCE)]
        fenced, para, numbers = False, [], []
        for number, line in enumerate(lines, 1):
            stripped = line.lstrip()
            skip = (stripped.startswith(FENCE) or not line.strip()
                    or stripped.startswith("|") or stripped.startswith("#"))
            if skip or (para and BULLET.match(line)):
                inspected += examine(path, para, numbers, marks, report)
                para, numbers = [], []
            if stripped.startswith(FENCE):
                fenced = not fenced
                continue
            if fenced or skip:
                continue
            para.append(line)
            numbers.append(number)
        inspected += examine(path, para, numbers, marks, report)

    report.count("prose paragraphs inspected", inspected)
    report.count("checks stated outside a fence", report.findings)

    # Zero paragraphs means the roots named nothing that exists: the check
    # reached no input, which is not a clean tree.
    return report.finish(bool(report.findings) or not inspected)
