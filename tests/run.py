#!/usr/bin/env python3
"""Run a test suite by name.

A suite is a folder under tests/ that holds a run.py. A fork adds one, such
as tests/e2e/run.py, and it is listed and runnable with no edit here.

Usage:
  py tests/run.py                        # list the suites
  py tests/run.py smoke [SYS-01 ...]     # one suite; the rest is its own
  py tests/run.py conformance --list
  py tests/run.py fork_sync --base=<ref>
  py tests/run.py all                    # the suites CI runs, in its order
"""

import os
import runpy
import subprocess
import sys

TESTS = os.path.dirname(os.path.abspath(__file__))

# The suites CI runs, in its order. A suite outside this list, such as a
# fork's end-to-end run against paid models, runs only when named.
ALL = ["smoke", "conformance", "fork_sync"]


def suites():
    """Every folder under tests/ holding a run.py, by name."""
    return sorted(name for name in os.listdir(TESTS)
                  if os.path.isfile(os.path.join(TESTS, name, "run.py")))


def run_all():
    """Run each suite in ALL in its own process; fail if any fails."""
    found = suites()
    missing = [name for name in ALL if name not in found]
    if missing:
        print(f"missing suite(s): {', '.join(missing)}")
        return 1
    failed = []
    for name in ALL:
        print(f"\n=== {name}")
        code = subprocess.run([sys.executable, __file__, name]).returncode
        if code:
            failed.append(name)
    skipped = [name for name in found if name not in ALL]
    print(f"\nsuites run: {len(ALL)}, failed: {len(failed)}"
          + (f" ({', '.join(failed)})" if failed else ""))
    if skipped:
        print(f"not in all, run by name: {', '.join(skipped)}")
    return 1 if failed else 0


def main(args):
    found = suites()
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        print(f"\nsuites: {', '.join(found)}")
        return 0
    name, rest = args[0], args[1:]
    if name == "all":
        return run_all()
    if name not in found:
        print(f"no suite named {name!r}; suites: {', '.join(found)}")
        return 1

    # The suite runs as if started directly: its own __main__ block reads
    # its own arguments, and tests/ is importable for its packages and a
    # fork's modules.
    sys.argv = [os.path.join(TESTS, name, "run.py")] + rest
    runpy.run_module(f"{name}.run", run_name="__main__", alter_sys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
