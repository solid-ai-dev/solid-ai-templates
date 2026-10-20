"""Fail on a Python identifier holding a non-ASCII character.

A name is typed, searched and compared; a character confusable with the
ASCII it resembles turns all three into guesswork. Comments, docstrings and
strings are documentation and carry no charset restriction.
"""

import argparse
import token
import tokenize

from .support.files import tracked


def main(argv, report):
    parser = argparse.ArgumentParser(prog="check-ascii-identifiers")
    parser.add_argument("--root", action="append", default=[],
                        help="directory to scan; repeatable")
    args = parser.parse_args(argv)

    files = report.count("python files inspected", tracked([".py"], args.root))
    for path in files:
        with open(path, "rb") as handle:
            for item in tokenize.tokenize(handle.readline):
                if item.type != token.NAME:
                    continue
                bad = sorted({ord(c) for c in item.string if ord(c) > 127})
                if bad:
                    report.finding(path, item.start[0], "NON-ASCII",
                                   " ".join("U+%04X" % c for c in bad))
    report.count("non-ASCII identifiers", report.findings)
    if not files:
        return report.not_applicable("no Python file is tracked")
    return report.finish(bool(report.findings))
