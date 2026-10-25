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
wired years later reported 122 of them in one module, which is why a tool,
not review, checks every override against its base.

A subtype declining a differently-named method breaks nothing; a subtype
declining a parameter its supertype promised breaks every caller holding the
supertype.
