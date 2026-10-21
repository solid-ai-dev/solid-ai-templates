# Frontend — Content
[ID: frontend-content]
[DEPENDS ON: templates/core/docs.md, templates/core/quality.md]

Abstract rules for authored web content — content and code separation,
assets, SEO and structured data — whatever builds and serves it. Extended
by a layer that builds the site, or picked alone by a project whose content
another system builds and serves.

## Content structure
[ID: static-site-content]
[EXTEND: base-docs]

All editable content lives in a data directory as structured files (JSON,
YAML, or Markdown). Never hardcode content that a non-developer might want
to change.

| File | Controls |
|------|----------|
| `[data path]/site.[ext]` | Nav links, hero text, contact links, footer |
| `[data path]/[section].[ext]` | [what it controls] |

## Assets
[ID: static-site-assets]

- Keep images and documents in the directory the build serves statically,
  and reference them by root-relative paths
- Serve no asset from outside that directory

## SEO
[ID: static-site-seo]

- `robots.txt`, Open Graph, and Twitter Card meta tags required for
  server-rendered and static pages
- Canonical URLs required for publicly indexed pages
- Sitemap MUST be generated at build time and referenced in `robots.txt`
- Every content page MUST have a unique `description` in frontmatter — used
  for `<meta name="description">`, OG description, and Twitter Card
- Meta descriptions MUST read as a pitch, not a summary — answer "why
  should I click this?"
- JSON-LD structured data SHOULD be present on content pages (Article,
  Course, or appropriate schema type)
- `robots.txt` MAY allow answer-engine crawlers (OAI-SearchBot,
  ChatGPT-User, PerplexityBot, Claude-SearchBot/Claude-User, Applebot);
  decide it deliberately, and verify no edge setting overrides the file
- MUST pick a trailing slash convention (with or without) and enforce it
  across all internal links, canonical URLs, and sitemap entries — redirect
  chains waste crawl budget, split link equity, and can prevent indexing
- If `og:image` is present, `twitter:image` MUST also be present —
  Twitter/X does not reliably fall back to `og:image`. Include
  `og:image:width`/`og:image:height` (recommended 1200×630) to avoid
  render delays on social platforms
- H1 keywords SHOULD appear in the page body — search and answer engines
  use heading/body coherence as a relevance signal; H1 SHOULD be unique
  per page and reflect its content
- Provide a complete favicon set: an SVG favicon
  (`<link rel="icon" type="image/svg+xml">`) and a 180×180
  `apple-touch-icon` for iOS home-screen bookmarks
- Answer engines retrieve passages, not whole pages — lead each section
  with a direct answer and keep paragraphs self-contained

## Structured data (if applicable)
[ID: frontend-content-structured-data]

- Schema `@type` MUST match the page's actual role — do not use
  `Product` + `Offer` on informational pages that do not sell anything
- Fields MUST NOT imply capabilities the site lacks (e.g. `availability`
  implies commerce, `priceValidUntil` implies a store)
- Review schema choice when site role differs from template examples —
  e-commerce examples applied to editorial sites produce misleading markup
