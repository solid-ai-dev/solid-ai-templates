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

# A suffix for a substituted command whose findings are read, not scored. A
# checker exits 1 on findings, which the block carries on past; any other
# exit means it could not run at all (a bad configuration, a crash), so the
# block stops there with that exit, before a later command can overwrite it.
FINDINGS_ONLY = " || { s=$?; [ $s -eq 1 ] || exit $s; }"
