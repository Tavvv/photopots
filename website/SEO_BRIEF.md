# PhotoPots — SEO Brief

Rules every page agent MUST follow. Pair with `DESIGN_BRIEF.md`.

Canonical domain: **`https://www.photopots.com`** (always absolute, always
`www`, always HTTPS).

---

## 1. Title tags — ≤ 60 characters

Formulas (pick one per page):

| Page type | Formula | Example |
|---|---|---|
| Home | `PhotoPots — Keep Work and Life Photos Apart` | (46 chars) |
| Main page | `{Primary keyword} — PhotoPots` | `Features — PhotoPots` |
| Landing page | `{Keyword phrase} — PhotoPots` | `Photo App for Contractors — PhotoPots` |
| Blog post | `{Post title} — PhotoPots Blog` | trim title until ≤ 60 with suffix |
| Legal/utility | `{Page name} — PhotoPots` | `Privacy Policy — PhotoPots` |

- Put the primary keyword first; brand last.
- Count characters including spaces. If over 60, shorten the front part,
  never drop the separator pattern silently on main pages.

## 2. Meta descriptions — ≤ 155 characters

- One sentence (two max), active voice, includes the primary keyword and a
  concrete benefit or differentiator.
- End with a soft CTA where natural ("Free to download.").
- Example (home, 139 chars): *"PhotoPots keeps work and personal photos in
  separate pots. Sort or capture straight into a pot — originals leave your
  Camera Roll. Free for iPhone, iPad & Mac."*

## 3. On-page structure

- **Exactly one `<h1>` per page**, containing the primary keyword, visually
  near the top.
- Heading hierarchy never skips levels (`h1` → `h2` → `h3`). Don't pick
  headings for size — restyle with classes instead.
- Semantic HTML: `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`,
  `<ul>` for repeated cards/tiles, `<details>/<summary>` for FAQ.
- First 100 words of body copy should include the primary keyword naturally.

## 4. Images

- Every `<img>` has a descriptive `alt` (what + context, not "image of").
  Decorative images (logo glyphs next to a text wordmark, blobs) use
  `alt=""`.
- Always set `width` and `height` attributes (prevents layout shift).
- Below-fold images: `loading="lazy" decoding="async"`. Hero/above-fold
  images: no lazy attribute.
- Filenames: kebab-case, descriptive (`sort-into-pots-screenshot.png`, not
  `IMG_4521.png`).

## 5. Canonical & URLs

- Every page has `<link rel="canonical">` with its absolute URL.
- URL style: root pages `https://www.photopots.com/features.html`;
  directory pages `https://www.photopots.com/for-contractors/` (trailing
  slash). Be consistent with the file convention in DESIGN_BRIEF.md §6.
- Lowercase, hyphens, no parameters, no dates in blog URLs.

## 6. Internal linking plan

Mandatory links:

- **Every page** → header nav (Features, How it works, Pricing, Blog, FAQ,
  Download CTA) + footer columns (Product / Resources / Legal).
- **Home** → features, how-it-works, pricing, faq (contextual links in body
  copy, not just nav).
- **features.html** → how-it-works, pricing; each landing page relevant to
  the feature.
- **how-it-works.html** → pricing, faq.
- **pricing.html** → faq (billing questions), features.
- **faq.html** → how-it-works, pricing, support.
- **Each landing page** (`for-*/index.html`) → features, pricing, and at
  least one sibling landing page where natural.
- **Each blog post** → parent `blog.html`, at least one product page
  (features or how-it-works) and one related post.
- Blog index → every post.
- Use descriptive anchor text ("sort photos out of your Camera Roll"), never
  "click here".

## 7. JSON-LD structured data

Add one `<script type="application/ld+json">` block per page (template has a
placeholder). Use these schemas:

- **Home (`index.html`)** — `Organization` **and** `SoftwareApplication`:
  ```json
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "PhotoPots",
    "operatingSystem": "iOS, macOS",
    "applicationCategory": "PhotoApplication",
    "description": "…same as meta description…",
    "url": "https://www.photopots.com/",
    "image": "https://www.photopots.com/assets/img/og-image.png",
    "offers": [
      { "@type": "Offer", "name": "Free", "price": "0", "priceCurrency": "USD" },
      { "@type": "Offer", "name": "Pro", "price": "TODO", "priceCurrency": "USD" }
    ]
  }
  ```
  ```json
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "PhotoPots",
    "url": "https://www.photopots.com/",
    "logo": "https://www.photopots.com/assets/img/app-icon-512.png"
  }
  ```
- **Any page with Q&A** (faq.html, pricing if it has Q&A) — `FAQPage` with
  `mainEntity` of `Question`/`acceptedAnswer` pairs that **match the visible
  page copy exactly**.
- **All subpages and directory pages** — `BreadcrumbList`
  (Home → Features, Home → Blog → Post title, etc.).
- **Blog posts** — `BlogPosting` (headline, datePublished, dateModified,
  author Organization, image).
- Don't invent `aggregateRating` or `review` data — none exists yet.

## 8. Sitemap & robots (integration agent will create these)

Conventions to follow so that work is mechanical later:

- `sitemap.xml` at site root; list every canonical URL with `<lastmod>`.
  Priority hint: home 1.0, main pages 0.8, landing pages 0.7, blog posts 0.6,
  legal 0.2.
- `robots.txt` at site root: allow all, reference
  `Sitemap: https://www.photopots.com/sitemap.xml`.
- If you create a page, note its canonical URL for the integration agent.

## 9. Performance / Core Web Vitals

- **No external JS libraries.** Vanilla JS only. The only third-party
  request allowed is Google Fonts (`preconnect` + single css2 request,
  already in `template.html`).
- Keep page-specific JS inline and tiny; shared behavior lives in
  `assets/js/main.js`.
- CSS: reuse `tokens.css` + `main.css`; avoid page-specific `<style>` blocks
  beyond a few rules.
- `width`/`height` on all images (CLS); `loading="lazy"` below the fold.
- Compress screenshots before committing (target < 200 KB; prefer PNG for UI
  screenshots, quality-80 JPEG/WebP for photos).
- Don't add third-party analytics/pixels without explicit approval.
- Respect `prefers-reduced-motion` (already handled by main.css/main.js).

## 10. Keyword seeds (guidance, not stuffing)

- Core: "separate work and personal photos", "photo organizer app",
  "sort photos into folders iphone", "keep work photos separate".
- Feature-led: "ocr photo search", "scan screenshots cleanup",
  "photo metadata preserved".
- Audience-led: "photo app for contractors", "photo app for real estate
  agents", "photo app for inspectors", "photo app for nurses/teachers/
  field technicians".
- One primary keyword per page; secondary keywords support, never compete.
