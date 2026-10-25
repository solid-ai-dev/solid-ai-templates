# Frontend — UX Principles

[ID: frontend-ux]
[DEPENDS ON: templates/core/quality.md]

## UX principles

- Make every view usable on a small screen, not only on a desktop one
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
- Never put a click handler on a non-focusable element (MUST NOT); it adds
  no tab stop or keyboard activation
- Use a native interactive element for such a control instead: a button, a
  link or another native control
- Style focus with `:focus-visible`, not `:focus`, which also outlines
  mouse clicks
- Keep a visible focus indicator on every focusable element, links and nav
  links included (MUST); links often lack one even where buttons have it
- Never convey meaning by colour alone
- Give images descriptive `alt` text, and decorative ones `alt=""`
- Use semantic HTML: landmark elements and a correct heading hierarchy
- Give an icon-only or ambiguous control, such as a social link, a
  descriptive `aria-label`; never add one where visible text already names
  the control
- Make an accessible name contain the control's visible text, ideally at
  its start (WCAG 2.5.3, Label in Name)
- Close menus on Escape and restore focus

## Accessibility testing

Automated tools catch about 30–40% of WCAG issues, so AA takes manual
testing too.

### Automated (run in CI)

- Scan rendered pages or components with an automated accessibility
  checker in CI; merge on zero violations

### Manual (run before shipping new interactive components)

- Tab through the whole feature without a mouse: every action reachable,
  focus order logical, no focus trap but an intentional modal
- Test it with one screen reader, such as NVDA, VoiceOver or TalkBack, and
  check every content and state change is announced
- Zoom to 200%: nothing clipped or overlapping, and no horizontal scroll
  at a 1280px viewport
- Check Windows High Contrast or the forced-colors media query: no
  information lost when colours are overridden

### Criteria for done

A feature is not complete until:

- [ ] The automated accessibility check reports zero violations
- [ ] Keyboard navigation verified manually
- [ ] Screen reader walkthrough completed for new interactive elements

## Design system

- Use the project's design system where one exists; never build an ad-hoc
  component that duplicates one of its patterns
- Take design tokens (colours, spacing, typography, radii, breakpoints)
  from the design system (MUST); never hardcode a visual value
- Build UI as a hierarchy of reusable, self-contained components, never a
  monolithic view

## Browser support

[ID: frontend-ux-browsers]

- Support the last two versions of Chrome, Firefox, Safari and Edge by
  default
- Degrade gracefully where a browser lacks a feature
