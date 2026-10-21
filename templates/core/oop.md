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
- Encapsulate state and implementation; expose behaviour through a public
  interface
- Design to interfaces, protocols or abstract base classes, not concrete
  types
- Treat a hierarchy deeper than two levels as a signal to refactor toward
  composition
- Model a closed type family, every variant known when the type is
  written, as a tagged union on a literal field (`kind`, `type`), so the
  compiler checks every branch
- Keep class hierarchies for families callers extend
- Name a module or class for the role its layer gives it; rename an
  `endpoints.py` with no routes or a `*RestApi` that is not the REST API

## When not to reach for a class
[ID: base-oop-restraint]

SOLID and the patterns below bias toward classes; these rules are the
counterweight.

- Write stateless logic as a free function; introduce a class only to
  encapsulate state it owns
- Treat a class whose only public method is `run()` or `execute()` as a
  function in disguise, unless its retained state warrants an object
- Put state-mutating behaviour on the object that owns the state, never in
  an external function that mutates a data bag
- Construct through named constructors or factory methods on the type,
  not free functions that build and return it

## Design patterns

- Use an established pattern where it fits the problem; never invent an
  ad-hoc solution to a problem that has a named one
- Use **Singleton** only for stateless services or infrastructure objects
  (logger, config) — never for mutable shared state
- Name the pattern in code when you use one: a class named
  `OrderExportStrategy` communicates intent; a class named `OrderHelper`
  does not

## Cross-cutting concerns
[ID: base-oop-aop]

- Keep cross-cutting behaviour visible at its call site: a logger call, an
  auth middleware or guard, a transaction context manager, a validation
  call at the boundary
- Never inject behaviour through method interception, bytecode weaving or
  an opaque runtime proxy — it is hard to read, debug and test
- Use a decorator only when it wraps and visibly delegates
