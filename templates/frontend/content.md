# Frontend — Content
[ID: frontend-content]
[DEPENDS ON: templates/core/docs.md, templates/core/quality.md]

Rules for authored web content, whatever builds and serves it: content and
code separation, assets, SEO and structured data.

## Content structure
[ID: static-site-content]
[EXTEND: base-docs]

- Store editable content as structured data apart from code, such as JSON,
  YAML or Markdown files
- Never hardcode content a non-developer might want to change

## Assets
[ID: static-site-assets]

- Reference each image and document by a path that resolves the same from
  every page, never by one relative to the current page

## SEO
[ID: static-site-seo]

- Add `robots.txt`, Open Graph and Twitter Card tags to server-rendered and
  static pages
- Give every publicly indexed page a canonical URL
- Serve a sitemap and reference it in `robots.txt` (MUST)
- Generate the sitemap at build time where the build knows every page URL
- Generate it at runtime where pages exist only at runtime
- Give every content page a unique description (MUST) — used for
  `<meta name="description">`, OG description, and Twitter Card
- Write meta descriptions as a pitch, not a summary (MUST); answer "why
  should I click this?"
- Add JSON-LD structured data to content pages (SHOULD)
- Match each JSON-LD schema type to the page's actual role, such as Article
  or Course (MUST)
- Never mark up a claim the page does not make (MUST NOT), such as an offer
  with no seller named on a page that only reviews the item
- Decide answer-engine crawler access in `robots.txt` deliberately
- Allow answer-engine crawlers by user agent in `robots.txt` (MAY)
- Verify no edge setting overrides the answer-engine crawler access set
  in `robots.txt`
- Add `twitter:image` wherever `og:image` is present (MUST); Twitter/X
  does not reliably fall back to `og:image`
- Keep each H1 unique to its page and true to its content (SHOULD)
- Provide a favicon, and an icon for home-screen bookmarks on mobile
- Lead each section with a direct answer in self-contained paragraphs;
  answer engines retrieve passages, not pages
- Serve a custom 404 page that links back into the site

## Trailing slash
[ID: static-site-trailing-slash]

- Pick one convention, with or without, and enforce it across internal
  links, canonical URLs and sitemap entries (MUST); redirect chains waste
  crawl budget and can prevent indexing
- Verify the convention matches the host's behaviour (MUST); some hosts
  force one, others make it configurable
- Add a CI check that fails on an internal link breaking the convention
  (SHOULD)
