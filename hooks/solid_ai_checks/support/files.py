"""The files a hook reads: the tracked ones, never the working-tree walk."""

import posixpath
import subprocess

# Vendored and installed code is not the project's own. Tracked copies of
# it still dominate any count they are left in.
VENDORED = ("node_modules", "vendor", "site-packages", ".venv", "venv",
            "build", "dist", ".tox")


class NotARepository(Exception):
    """Raised outside a git work tree, where nothing is tracked."""


def tracked(suffixes, roots=()):
    """Tracked paths ending in one of `suffixes`, under one of `roots`.

    Asking git keeps a scratch or ignored file out of the corpus, so a
    check reads the same tree on a laptop as in CI. An empty `roots`
    means the whole tree.
    """
    try:
        listing = subprocess.run(
            ["git", "ls-files", "-z"], capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        raise NotARepository("not inside a git work tree")
    paths = listing.stdout.decode("utf-8").split("\0")
    prefixes = normalised(roots)
    return sorted(
        p for p in paths
        if p.endswith(tuple(suffixes))
        and (not prefixes or p.startswith(prefixes))
        and not any(part in VENDORED for part in p.split("/")))


def normalised(roots):
    """Roots as the prefixes git prints; empty when one names the whole tree.

    git prints `docs/a.md`, so `./docs`, `docs/` and `docs\\` all have to
    become `docs/` before they can match it, and `.` means every path.
    """
    prefixes = []
    for root in roots:
        clean = posixpath.normpath(root.replace(chr(92), "/"))
        if clean in (".", ""):
            return ()
        prefixes.append(clean + "/")
    return tuple(prefixes)


def path_prefix(raw):
    """A path prefix spelled as git prints paths; empty for the whole tree.

    `./.github/workflows/` and `.github\\workflows\\` both become
    `.github/workflows/`. A trailing slash is kept, because `.env` names a
    file prefix and `migrations/` a directory, and the two match
    differently.
    """
    text = raw.strip().replace(chr(92), "/")
    clean = posixpath.normpath(text) if text else "."
    if clean == ".":
        return ""
    return clean + "/" if text.endswith("/") else clean


def read_lines(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read().splitlines()
