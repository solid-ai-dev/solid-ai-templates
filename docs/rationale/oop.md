# Rationale: oop

Why the rules in `templates/core/oop.md` say what they say. The template
states each rule as one instruction; the reasoning and the worked examples
are here, one heading per section, named by ID where the section has one.

## Hierarchies

A variadic in a base states no contract a subtype can honour or break: it
guarantees only that the call compiles, so every subtype narrows what the
base promised, and a caller holding the abstract type cannot call the
operation without knowing the concrete class. This is the contravariance
rule on parameters (Liskov and Wing, 1994); what a codebase lacks is the
tell. Nothing reports it: a linter has no rule, review reads one class at a
time, and tests instantiate concrete classes. In one project a type checker
wired years later reported 122 of them in one module. Frozen variadic
findings are the entries to shrink first: they are not missing annotations,
they are the abstraction not holding.

A subtype declining a differently-named method breaks nothing; a subtype
declining a parameter its supertype promised breaks every caller holding the
supertype.

A plain `getattr` resolves a `staticmethod` or `classmethod` to its bound
callable and hides its own signature, so the contract test reads the class's
own descriptor. A sketch of that test:

```python
import inspect


def unwrap(cls, name):
    found = inspect.getattr_static(cls, name)
    if isinstance(found, (staticmethod, classmethod)):
        found = found.__func__
    return found


def override_findings(base, hierarchy):
    ops = [n for n, v in vars(base).items()
           if inspect.isfunction(v) or isinstance(v, (staticmethod, classmethod))]
    findings = []
    for name in ops:
        kind = type(inspect.getattr_static(base, name))
        want = list(inspect.signature(unwrap(base, name)).parameters)
        for cls in hierarchy:
            got = list(inspect.signature(unwrap(cls, name)).parameters.values())
            if type(inspect.getattr_static(cls, name)) is not kind:
                findings.append("%s.%s changes member kind" % (cls.__name__, name))
            if [p.name for p in got[:len(want)]] != want:
                findings.append("%s.%s narrows or reorders" % (cls.__name__, name))
            if any(p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD) for p in got):
                findings.append("%s.%s declares a variadic" % (cls.__name__, name))
    return findings
```
