"""The templates' own checks, as this repository runs them.

dispositions.py says what happens to each fenced check. The words it uses
are defined here, so a fork's fork_dispositions.py imports them from the
package without importing the registry that takes it in.
"""

# Disposition values.
RUN = "run"
SKIP = "skip"

# Pass predicates beside the list form; dispositions.py describes them.
MANUAL = "manual"
READ = "read"
