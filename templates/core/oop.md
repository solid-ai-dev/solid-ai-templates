# Base — Object-Oriented Design

[ID: base-oop]

## SOLID principles

Apply SOLID at the class, module and service level:

- **Single responsibility**: give each class or module one reason to
  change; split one that serves two concerns
- **Open/closed**: extend behaviour by adding code, not by editing it,
  through interfaces, abstract base classes or composition
- **Liskov substitution**: keep every subtype substitutable for its base;
  never override a method so that it weakens the contract
- **Interface segregation**: prefer small, focused interfaces; never make a
  caller depend on methods it does not use
- **Dependency inversion**: depend on abstractions, and inject dependencies
  rather than constructing them inside a class

## Object design

- Prefer composition over inheritance; inherit only for a true is-a
  relationship
- Treat a hierarchy deeper than two levels as a signal to refactor toward
  composition
- Model a closed type family, every variant known when the type is
  written, so that a branch missing a variant fails rather than falls
  through
- Keep class hierarchies for families callers extend
- Name a module or class for the role its layer gives it
- Rename a module or class whose name claims a role it does not play

## Hierarchies

- Never declare a variadic parameter on an abstract or overridable
  operation; it states no contract a subtype can keep
- Give a capability its own name where a class part-way down a hierarchy
  offers what its own subtypes must not
- Never widen the shared operation to carry such a capability
- Keep every override callable wherever its base is: the same member kind
  and parameters, with new parameters only appended and given defaults
- Check every override against its base with a tool (SHOULD), such as:
  - the compiler
  - a strict type checker's override rule
  - a contract test walking every concrete class

## When not to reach for a class
[ID: base-oop-restraint]

SOLID and the patterns below bias toward classes; these rules are the
counterweight.

- Write stateless logic as a function; introduce a class only to
  encapsulate state it owns
- Treat a class whose only public method is `run()` or `execute()` as a
  function in disguise, unless its retained state warrants an object
- Put state-mutating behaviour on the object that owns the state, never in
  an external function that mutates a data bag
- Construct through named constructors or factory methods on the type,
  not free functions that build and return it

## Design patterns

- Use an established pattern once its problem is present, never before
- Never invent an ad-hoc version of a named pattern
- Use **Singleton** only for stateless services or infrastructure objects
  (logger, config) — never for mutable shared state
- Name the pattern in code when you use one: a class named
  `OrderExportStrategy` communicates intent; a class named `OrderHelper`
  does not

## Cross-cutting concerns
[ID: base-oop-aop]

- Keep cross-cutting behaviour visible at its call site, such as:
  - a logger call
  - an auth middleware or guard
  - a transaction block
  - a validation call at the boundary
- Never inject behaviour through method interception, bytecode weaving or
  an opaque runtime proxy — it is hard to read, debug and test
- Use a decorator only when it wraps and visibly delegates
