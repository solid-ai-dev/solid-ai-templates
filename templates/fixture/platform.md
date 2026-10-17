# Platform — Fixture
[ID: platform-fixture]
[DEPENDS ON: templates/core/quality-gates.md]

Test input for the checks that read a platform, not a platform to pick. It
resolves as its own root, beside the fixture stack and never inside it.

---

## CI
[ID: platform-fixture-ci]

- Run every gate the quality-gate tier names on each pull request
- Fail the pull request when any gate fails; never mark a gate optional
