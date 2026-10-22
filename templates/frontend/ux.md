# Frontend — UX Principles

[ID: frontend-ux]
[DEPENDS ON: templates/core/quality.md]

## UX principles

- Design for small screens first, then enhance for larger ones
- Show only what the user needs at each step
- Never use a dark pattern: misleading UI, a forced action, a hidden cost
- Use the same interaction pattern for the same task throughout
- Treat a slow interface as a UX defect
- Make every component behave as it looks: what looks like a button acts
  like one

## Accessibility — WCAG 2.1 AA

- Meet WCAG 2.1 AA
- Keep text contrast at 4.5:1 or more, 3:1 for large text
- Make every interactive element reachable and operable by keyboard
- Put a `<button>` inside any non-focusable element (`<th>`, `<div>`,
  `<span>`) with an `onClick` (MUST); `onClick` alone adds no tab stop or
  keyboard activation
- Style focus with `:focus-visible`, not `:focus`, which also outlines
  mouse clicks
- Keep focus indicators visible throughout keyboard navigation
- Give every `<a>` and nav link a visible `:focus-visible` outline (MUST);
  links often lack one even where buttons have it
- Never convey meaning by colour alone
- Give images descriptive `alt` text, and decorative ones `alt=""`
- Use semantic HTML: landmark elements and a correct heading hierarchy
- Give every interactive element an `aria-label` (buttons, icon links,
  social links), and every icon-only or ambiguous link a descriptive one
- Close menus on Escape and restore focus

## Accessibility testing

Automated tools catch about 30–40% of WCAG issues, so AA takes manual
testing too.

### Automated (run in CI)

- Run axe-core through the framework's adapter (`@axe-core/react`,
  `@axe-core/vue`, `axe-playwright`, `jest-axe`); merge on zero violations
- Hold every key page to a Lighthouse accessibility score of 90 or more,
  in CI through `lighthouse-ci`
- Lint for missing `alt`, wrong ARIA roles and missing form labels with
  the framework's a11y plugin (`eslint-plugin-jsx-a11y`,
  `eslint-plugin-vuejs-accessibility`; Svelte warns by default)

### Manual (run before shipping new interactive components)

- Tab through the whole feature without a mouse: every action reachable,
  focus order logical, no focus trap but an intentional modal
- Walk it with one screen reader (NVDA with Chrome, VoiceOver with Safari,
  or TalkBack), and check every content and state change is announced
- Zoom to 200%: nothing clipped or overlapping, and no horizontal scroll
  at a 1280px viewport
- Check Windows High Contrast or the forced-colors media query: no
  information lost when colours are overridden

### Criteria for done

A feature is not complete until:

- [ ] `axe-core` reports zero violations in component tests
- [ ] Lighthouse accessibility score ≥ 90
- [ ] Keyboard navigation verified manually
- [ ] Screen reader walkthrough completed for new interactive elements

## Design system

- Use the project's design system where one exists; never build an ad-hoc
  component that duplicates one of its patterns
- Take design tokens (colours, spacing, typography, radii, breakpoints)
  from the design system (MUST); never hardcode a visual value
- Build UI as a hierarchy of reusable, self-contained components, never a
  monolithic view
- Document a new component with usage examples before shipping it (SHOULD)

## Browser support

[ID: frontend-ux-browsers]

- Support the last two versions of Chrome, Firefox, Safari and Edge by
  default
- Degrade gracefully where a browser lacks a feature
