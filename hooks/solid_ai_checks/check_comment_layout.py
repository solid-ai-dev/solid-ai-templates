"""Fail on the two comment-layout violations a tokenizer can see.

A comment block with code directly above it and no blank line between, and
an aside to the right of code that is not a tool directive. Whether a
comment sits above the right item takes a person.
"""

import argparse
import subprocess
import tokenize

from .files import VENDORED, NotARepository, normalised, read_lines

DIRECTIVES = ("noqa", "nosec", "type:", "pragma:", "pylint:", "fmt:", "mypy:")

# A comment that is the first thing inside a block or bracket opens the
# first group rather than dividing two, so a line ending in one of these
# needs no blank line under it.
OPENERS = (":", "(", "[", "{")


def candidates(roots):
    """Tracked Python plus the untracked files a commit could still add."""
    try:
        listed = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others",
             "--exclude-standard", "*.py"],
            capture_output=True, check=True).stdout.decode("utf-8")
    except (OSError, subprocess.CalledProcessError):
        raise NotARepository("not inside a git work tree")
    prefixes = normalised(roots)
    return sorted(set(
        p for p in listed.split("\0")
        if p and (not prefixes or p.startswith(prefixes))
        and not any(part in VENDORED for part in p.split("/"))))


def main(argv, report):
    parser = argparse.ArgumentParser(prog="check-comment-layout")
    parser.add_argument("--root", action="append", default=[],
                        help="directory to scan; repeatable")
    args = parser.parse_args(argv)

    files = report.count("python files checked", candidates(args.root))
    for path in files:
        src = read_lines(path)
        with open(path, "rb") as handle:
            for tok in tokenize.tokenize(handle.readline):
                if tok.type != tokenize.COMMENT:
                    continue
                row, col = tok.start
                if src[row - 1][:col].strip():
                    body = tok.string.lstrip("#").strip()
                    if not body.startswith(DIRECTIVES):
                        report.finding(path, row, "ASIDE",
                                       "comment to the right of code")
                elif row > 1 and src[row - 2].strip():
                    above = src[row - 2].split("#")[0].rstrip()
                    if not src[row - 2].strip().startswith("#") \
                            and not above.endswith(OPENERS):
                        report.finding(path, row, "ABUTS",
                                       "comment block with code directly "
                                       "above it")
    report.count("layout violations", report.findings)
    if not files:
        return report.not_applicable("no Python file to check")
    return report.finish(bool(report.findings))
