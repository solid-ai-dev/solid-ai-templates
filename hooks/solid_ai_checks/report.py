"""The output contract every hook follows.

A hook prints what it inspected, one count per line, then one line per
violation as `path:line: CODE message`. Run directly it exits 0 on a pass,
1 on a failure and 3 when it does not apply. Under pre-commit, which fails
a hook on any nonzero exit, "does not apply" prints `not applicable:
<reason>` and exits 0.
"""

import sys

PASS = 0
FAIL = 1
NOT_APPLICABLE = 3


def ascii_only(text):
    """Replace every non-ASCII character with its code point.

    A console that cannot encode a character fails the print, and the
    character itself is what the reader cannot see anyway.
    """
    return "".join(c if ord(c) < 128 else "U+%04X" % ord(c) for c in text)


class Report:
    """Collects a hook's counts and findings and prints them in order."""

    def __init__(self, pre_commit=False):
        self.pre_commit = pre_commit
        self.findings = []

    def count(self, label, value):
        """Print one inspected count and return the value."""
        n = value if isinstance(value, int) else len(value)
        print("%s: %d" % (label, n))
        return value

    def finding(self, path, line, code, message):
        """Record one violation. Line 0 means the finding is the whole file."""
        self.findings.append("%s:%d: %s %s" % (path, line, code, message))

    def note(self, text):
        """Print a line that is neither a count nor a finding."""
        print(ascii_only(text))

    def not_applicable(self, reason):
        """Say why the check does not apply, and return the exit status."""
        if self.pre_commit:
            print("not applicable: %s" % ascii_only(reason))
            return PASS
        print(ascii_only(reason))
        return NOT_APPLICABLE

    def finish(self, failed):
        """Print every finding, then return the exit status."""
        for line in self.findings:
            print(ascii_only(line))
        sys.stdout.flush()
        return FAIL if failed else PASS
