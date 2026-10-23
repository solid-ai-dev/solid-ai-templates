# Frontend — Quality Attributes

[ID: frontend-quality]
[DEPENDS ON: templates/core/quality.md]

## Patterns

- Use the pattern each case names: an error boundary around a failing
  subtree, a skeleton for loading, virtual scroll for long lists, a
  debounce on search input, validation on form input, a responsive switch
  at breakpoints, URL sync for shareable state

## Design patterns

- Separate data fetching and state (container) from rendering
  (presentational); give presentational components only props and no side
  effects (SHOULD)
- Expose related sub-components that share implicit state as a compound
  component (`<Tabs>`, `<Tab>`, `<TabPanel>`) rather than drill props
  (SHOULD)
- Subscribe to external state (store, event bus, WebSocket) through one
  subscription point, and unsubscribe on unmount (SHOULD)
- Wrap a third-party library (analytics, maps, payment SDK) behind a thin
  project-owned interface; never scatter its calls across components
  (SHOULD)
- Apply a mutation's expected result at once and roll back on failure;
  document the rollback path (SHOULD)
- Avoid connecting components through an event bus; share state or lift
  it up instead (SHOULD NOT)

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

- Configure a linter for all JS/TS code (MUST)
- Run the linter and formatter on save in the IDE (SHOULD); never rely on
  CI alone for style
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

- Load no third-party tracking script without explicit user consent
