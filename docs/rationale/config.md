# Rationale: config

Why the rules in `templates/core/config.md` say what they say. The template
states each rule as one instruction; the reasoning is here, one heading per
section.

## Sources

Configuration in the environment can change per deployment without a
rebuild, and a secret kept out of source never enters the history. A global
config object read from anywhere hides which component depends on which
setting.

## Naming

An unprefixed name such as `DATABASE_URL` collides as soon as two services
share an environment. A common prefix keeps related settings together in a
listing.

## Precedence

A lookup that returns the same null for an absent source and an empty one
makes the highest-priority source silently lose to the lowest: a flag passed
with no value falls back to the very default the user was reaching past.

## Validation

A value checked at first use fails in the middle of a request, far from the
cause; a value checked at load time fails at start, with the name of the
setting. A default for a secret lets a deployment run with a known value.

## Build time and run time

A build-time value is inside the artifact, so anyone who inspects the
artifact can read it, and changing it needs a rebuild rather than a
restart.

## Secrets

A flat file of secrets on a production host is one copy too many and cannot
rotate centrally. A real secret in a test run lets the suite act on a live
account. A logged configuration value is a secret in the log store.

## Dependencies

A system-wide package works on the machine that has it and fails everywhere
else.
