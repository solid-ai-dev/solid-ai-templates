# Frontend — Quality Attributes

[ID: frontend-quality]
[DEPENDS ON: templates/core/quality.md]

## Patterns

- Use error boundary, skeleton loading, optimistic update, virtual
  scroll, debounced search, form validation, responsive switch, and
  URL state sync patterns where appropriate

## Design patterns

Prefer these patterns for frontend concerns:

- **Container / Presentational** — separate data-fetching and state logic
  (container) from rendering (presentational); presentational components
  receive only props, have no side effects, and are easy to test in isolation
- **Compound Component** — expose a set of related sub-components that share
  implicit state (e.g. `<Tabs>`, `<Tab>`, `<TabPanel>`); prefer over deeply
  nested prop drilling
- **Observer** — subscribe to external state changes (store, event bus,
  WebSocket) via a single subscription point; unsubscribe on component unmount
- **Facade** — wrap third-party libraries (analytics, maps, payment SDKs)
  behind a thin project-owned interface; never scatter SDK calls across
  components
- **Optimistic Update** — apply the expected result of a mutation immediately
  in the UI and roll back on failure; document the rollback path

Avoid:

- **Mediator / Event Bus** between components — use shared state or lifting
  state up instead; an event bus between components creates invisible coupling

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

- Never duplicate server state in a global store — use a dedicated server
  cache; the store holds only client-owned state
- Never put derived state in the store — compute it from existing state
- Prefer URL state for anything the user should be able to bookmark or share
- Keep global store slices small and focused — one slice per domain concern,
  not one slice for everything
- Find everything that depends on shared browser state (history, URL,
  localStorage, global context) before changing it

## Linting and formatting

- A linter MUST be configured for all JS/TS code
- Linter and formatter SHOULD run on save in the IDE — never rely on CI
  alone to catch style issues
- No warnings or errors MUST appear in the browser console or test output
  before a PR is merged — start every review on a clean slate
- Lint error count SHOULD go down over time — never increase it

## CSS

- No inline styles except for dynamic/computed values
- No hardcoded colour or spacing values — always use CSS custom properties
  from `:root` or design tokens
- Consistent naming convention (e.g. BEM-like `.component-element`)

## Performance

- Preload critical above-the-fold assets
- Render pages at build or on the server by default; render on the client
  only where a page needs client-side state
- Keep client-side JS minimal — every dependency adds to bundle size
- Avoid unnecessary dependencies
- Defer non-critical scripts
- Monitor Core Web Vitals (LCP, CLS, INP) — treat regressions as bugs

## Theme persistence (if applicable)
[ID: static-site-theme]

- Apply a persisted theme before first paint (MUST): render it on the
  server, or set it from a blocking `<head>` script if the browser stores it
- Never set the theme from a body or deferred script (MUST NOT); the page
  flashes the wrong theme on every load

## Analytics (if applicable)

- No third-party tracking scripts without explicit user consent
