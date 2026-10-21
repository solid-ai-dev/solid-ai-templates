# Frontend — Static Site
[ID: frontend-static-site]
[DEPENDS ON: templates/core/git.md, templates/security/security.md]
[DEPENDS ON: templates/frontend/content.md, templates/frontend/ux.md]
[DEPENDS ON: templates/frontend/quality.md]

Abstract rules for any static site generated at build time and served as
plain HTML, CSS, and minimal JavaScript. Never used directly — always
extended by a framework-specific stack (Astro, Hugo, Eleventy, etc.).

## Stack
[ID: static-site-stack]

- Output: static HTML generated at build time
- Serving: CDN or plain web server — no server-side runtime required
- JavaScript: minimal and opt-in — zero-JS by default where possible

## Architecture principle
[ID: static-site-architecture]

```
data files  →  components  →  build output (HTML)
    ↑                               ↓
Edit here                    Deployed here
```

- Separation of content and code — editable content lives in a data directory
- Default to static components; only reach for an interactive framework when
  client-side state is genuinely required
- One stylesheet — no inline styles except dynamic/computed values

## Pages
[ID: static-site-pages]

| Page     | Path    | Notes             |
|----------|---------|-------------------|
| Homepage | `/`     | The site's entry page |
| 404      | `/404`  | Custom error page |

## Code conventions
[ID: static-site-code]

- Lint any JS/TS code with the stack's linter, configured in the repository
  and run on save; skip it where the project has no JS/TS
- Let one formatter own all formatting, with its configuration committed;
  no style debates in code review

## CSS conventions
[EXTEND: frontend-quality]

- All CSS in a single global stylesheet
- Use CSS custom properties from `:root` for all colours and spacing
- BEM-like naming: `.component-element` (e.g. `.hero-grid`, `.nav-link`)
- No CSS-in-JS, no utility frameworks unless explicitly chosen in stack

## Typography
[ID: static-site-typography]

- Prefer system font stacks over web fonts — eliminates font FOUC and
  external dependencies:
  ```css
  --font-text: system-ui, -apple-system, sans-serif;
  --font-code: ui-monospace, "Cascadia Code", "Fira Code", monospace;
  ```
- If web fonts are required, self-host them as woff2 files in the directory
  the build serves statically
  and declare `@font-face` in CSS — never depend on external CDNs at runtime
- Use `font-display: block` for self-hosted fonts to prevent layout shift

## Theme persistence
[ID: static-site-theme]

- If the site supports dark mode via a `data-theme` attribute, initialize
  the theme from `localStorage` in a `<script>` tag inside `<head>` —
  before any content renders:
  ```html
  <script>
    document.documentElement.setAttribute(
      "data-theme",
      localStorage.getItem("theme") || "light"
    );
  </script>
  ```
- MUST NOT set the theme in a body script or deferred module — this causes
  a visible flash from light to dark on every page load

## Performance
[EXTEND: frontend-quality]

- Preload critical above-the-fold assets (hero image, primary font)
- Static generation by default — no client-side rendering unless necessary
- Defer non-critical scripts

## Trailing slash
[ID: static-site-trailing-slash]

- MUST verify the trailing slash convention matches the hosting platform's
  behavior (e.g. GitHub Pages forces trailing slashes, Netlify and Vercel
  are configurable)
- SHOULD add a CI check that scans built HTML output for internal hrefs
  violating the convention
