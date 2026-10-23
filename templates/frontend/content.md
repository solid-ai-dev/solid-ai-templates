# Frontend — Content
[ID: frontend-content]
[DEPENDS ON: templates/core/docs.md, templates/core/quality.md]

Rules for authored web content, whatever builds and serves it: content and
code separation, assets, SEO and structured data.

## Content structure
[ID: static-site-content]
[EXTEND: base-docs]

- Store editable content as structured files: JSON, YAML or Markdown
- Never hardcode content a non-developer might want to change

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

- Add `robots.txt`, Open Graph and Twitter Card tags to server-rendered and
  static pages
- Give every publicly indexed page a canonical URL
- Sitemap MUST be generated at build time and referenced in `robots.txt`
- Every content page MUST have a unique `description` in frontmatter — used
  for `<meta name="description">`, OG description, and Twitter Card
- Meta descriptions MUST read as a pitch, not a summary — answer "why
  should I click this?"
- Add JSON-LD structured data to content pages, with the schema type that
  matches the page (Article, Course) (SHOULD)
- `robots.txt` MAY allow answer-engine crawlers (OAI-SearchBot,
  ChatGPT-User, PerplexityBot, Claude-SearchBot/Claude-User, Applebot);
  decide it deliberately, and verify no edge setting overrides the file
- Add `twitter:image` wherever `og:image` is present (MUST); Twitter/X
  does not reliably fall back to `og:image`
- Add `og:image:width` and `og:image:height` (1200×630 recommended) to
  avoid render delays on social platforms
- Repeat H1 keywords in the page body (SHOULD); engines read heading and
  body coherence as relevance
- Keep each H1 unique to its page and true to its content (SHOULD)
- Provide an SVG favicon (`<link rel="icon" type="image/svg+xml">`) and a
  180×180 `apple-touch-icon` for iOS bookmarks
- Lead each section with a direct answer in self-contained paragraphs;
  answer engines retrieve passages, not pages
- Serve a custom 404 page that links back into the site

## Trailing slash
[ID: static-site-trailing-slash]

- Pick one convention, with or without, and enforce it across internal
  links, canonical URLs and sitemap entries (MUST); redirect chains waste
  crawl budget and can prevent indexing
- Verify the convention matches the host's behaviour (MUST): GitHub Pages
  forces trailing slashes; Netlify and Vercel are configurable
- Add a CI check that scans built HTML for internal hrefs that break the
  convention (SHOULD)

## Structured data (if applicable)
[ID: frontend-content-structured-data]

- Schema `@type` MUST match the page's actual role — do not use
  `Product` + `Offer` on informational pages that do not sell anything
- Fields MUST NOT imply capabilities the site lacks (e.g. `availability`
  implies commerce, `priceValidUntil` implies a store)
- Review schema choice when site role differs from template examples —
  e-commerce examples applied to editorial sites produce misleading markup
