# Frontend — Quality Attributes

[ID: frontend-quality]
[DEPENDS ON: templates/core/quality.md]

## Design patterns

- Subscribe to external state (store, event bus, WebSocket) through one
  subscription point, and unsubscribe on unmount (SHOULD)
- Wrap a third-party library (analytics, maps, payment SDK) behind a thin
  project-owned interface; never scatter its calls across components
  (SHOULD)

## State management

Choose the right tool for the scope of the state — do not use a global store
for state that is local to a component or a server cache for state that is
never fetched from a server.

| State type          | Scope                | When to use                                       |
| ------------------- | -------------------- | ------------------------------------------------- |
| **Local UI state**  | Single component     | Form inputs, toggles, counters                    |
| **Shared UI state** | Multiple components  | Auth session, sidebar state, active filters       |
| **Server state**    | Cached from API      | Lists, detail views, paginated results            |
| **Form state**      | Form lifecycle       | Validation, field arrays, multi-step flows        |
| **URL state**       | URL search params    | Bookmarkable filters, pagination, selected tab    |

Rules:

- Keep server data in one client cache; never copy it into a global store,
  which holds only client-owned state
- Never put derived state in a store — compute it from existing state
- Prefer URL state for anything the user should be able to bookmark or share
- Find everything that depends on shared browser state (history, URL,
  localStorage, global context) before changing it

## Linting and formatting

- Configure a linter for all script code the frontend ships (MUST)
- Merge no PR with a warning or error in the browser console or test
  output (MUST)
- Lower the lint error count over time, never raise it (SHOULD)

## CSS

- Use no inline styles except dynamic or computed values
- Use CSS custom properties from `:root` or design tokens for every colour
  and spacing value; never hardcode one
- Use one class-naming convention (e.g. BEM-like `.component-element`)

## Performance

- Preload critical above-the-fold assets
- Keep client-side script minimal; add a dependency only when it earns
  its bundle size
- Defer non-critical scripts
- Monitor Core Web Vitals (LCP, CLS, INP) — treat regressions as bugs

## In-process server

[ID: testing-in-process-server]

- Run browser-driven UI journeys against the real app, served in-process
  on port 0 and driven over real HTTP (SHOULD)
- Derive the base URL from the assigned port, and stop the server however
  the test ends
- Reserve a container for tests that need the built image or sidecar
  services

## Theme persistence (if applicable)
[ID: static-site-theme]

- Apply a persisted theme before first paint (MUST): render it on the
  server, or set it from a blocking `<head>` script if the browser stores it
- Never set the theme from a body or deferred script (MUST NOT); the page
  flashes the wrong theme on every load

## Analytics (if applicable)

- Load no third-party tracking script without explicit user consent
