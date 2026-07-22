# PhotoPots — Design Brief

Read this fully before building any page. It defines the brand, the exact CSS
classes available, copy voice, and file conventions. Pair with `SEO_BRIEF.md`.

---

## 1. Brand foundation

**Product**: PhotoPots, an iOS/Mac app that keeps work and personal photos in
separate "pots" (containers).

**Tagline**: *Keep work and life photos apart.*

**App icon concept**: dark camera lens surrounded by 4 colored rounded petals
(cyan top-left, blue top-right, orange bottom-right, red bottom-left) with a
small dark flash dot. Recreated as vectors in `assets/img/logo.svg` (full
icon), `logo-mark.svg` (petals only), `favicon.svg` (simplified for small
sizes). Raster: `app-icon-512.png`, `app-icon-maskable-512.png`,
`apple-touch-icon.png`, `favicon-32.png`, `og-image.png` (1200×630).

**Domain**: `https://www.photopots.com`

---

## 2. Color palette

All values live in `assets/css/tokens.css`. **Never hard-code hex values in
page markup** — use the custom properties.

### Brand accents (use sparingly — buttons, tiles, highlights only)

| Token | Hex | Use |
|---|---|---|
| `--blue` | `#1C9DE0` | Aperture blue — **primary** CTA, links, key accents |
| `--cyan` | `#2CD3E1` | Pot color |
| `--orange` | `#EA8A1E` | Pot color |
| `--red` | `#D8453E` | Pot color |
| `--green` | `#1D9E75` | Pot color, success/check marks |
| `--violet` | `#8C5BD9` | Pot color |

Each color also has a `-dark` variant (hover states, text on tints):
`--blue-dark` `#157FB8`, `--cyan-dark` `#1FA9B5`, `--orange-dark` `#C7751A`,
`--red-dark` `#B83B35`, `--green-dark` `#178263`, `--violet-dark` `#7449B5`.

### Pastel tints (pot tile backgrounds, soft washes)

| Color | Tint (≈15%) | Strong tint (≈30%) |
|---|---|---|
| Blue | `--blue-tint` `#DCF0FA` | `--blue-tint-strong` `#BAE1F6` |
| Cyan | `--cyan-tint` `#DFF8FA` | `--cyan-tint-strong` `#BFF2F6` |
| Orange | `--orange-tint` `#FBEDDD` | `--orange-tint-strong` `#F8DBBB` |
| Red | `--red-tint` `#F9E3E2` | `--red-tint-strong` `#F3C7C5` |
| Green | `--green-tint` `#DDF0EA` | `--green-tint-strong` `#BBE2D6` |
| Violet | `--violet-tint` `#EDE6F9` | `--violet-tint-strong` `#DCCDF4` |

### Neutrals (large surfaces — always low saturation)

`--white` `#FFFFFF`, `--cream` `#FAF7F2` (signature warm background),
`--sand` `#F3EEE6`, `--line` `#E8E2D8` (borders), `--ink` `#23262E`
(headings), `--ink-soft` `#4A4F5A` (body), `--ink-mute` `#777C88` (captions).

### Visual policy — HARD RULES

1. Large surfaces stay low-saturation: white, `--cream`, soft neutrals.
2. Brand colors are **accents only**: buttons, pot tiles, icon chips, the
   `.hl` highlight, small details.
3. **NO blue-purple gradients. NO highly saturated full-bleed backgrounds.**
4. Ample whitespace; clear hierarchy. Subtle grain/soft pastel shapes (`.blob`)
   are fine.
5. Pot tiles use pastel gradient + colored glow — that's where the color lives.

---

## 3. Spacing, radii, shadows, type

- **Spacing (4pt grid)**: `--space-1` 4 → `--space-2` 8 → `--space-3` 12 →
  `--space-4` 16 → `--space-5` 24 → `--space-6` 32 → `--space-7` 48 →
  `--space-8` 64 → `--space-9` 96.
- **Radii**: `--radius-6/10/12/16/24/full`. Cards & pot tiles = 16, hero
  panels & pricing & CTA banner = 24, buttons = full (pill).
- **Shadows**: `--shadow-lifted-sm`, `--shadow-lifted`; per-color glows
  `--glow-{blue,cyan,orange,red,green,violet}` (app recipe: 45% alpha, blur
  14, y 6) and softer `-soft` variants used by default on tiles/buttons.
- **Type**: headings `var(--font-display)` (ui-rounded → SF Pro Rounded →
  Nunito, weight 800), body `var(--font-body)` (Nunito 400/600/700). Scale:
  `--text-display` (fluid 40–56), `--text-h1` 36–48, `--text-h2` 28–36,
  `--text-h3` 22, `--text-h4` 18, `--text-body` 17, `--text-small` 15,
  `--text-tiny` 13.
- **Breakpoints**: 480 / 768 / 1024 / 1280. Nav collapses at 860.

---

## 4. Component class inventory

Exact class names — copy these patterns. All are in `assets/css/main.css`.

### Buttons

```html
<a class="btn btn--primary" data-appstore>Download free</a>   <!-- primary = aperture blue pill -->
<a class="btn btn--secondary" href="how-it-works.html">See how it works</a>
<a class="btn btn--ghost" href="features.html">All features →</a>
<!-- size modifiers: .btn--lg .btn--sm -->
```

**Every App Store link/button uses `data-appstore`** (config.js injects the
URL). Never paste a raw App Store URL.

### Section scaffolding

```html
<section class="section section--cream">   <!-- .section--cream | .section--sand | .section--tight optional -->
  <div class="container">                  <!-- .container--narrow for text-heavy pages -->
    <div class="section-header section-header--center reveal">
      <span class="eyebrow">How it works</span>   <!-- .eyebrow--orange/--green/--red/--violet -->
      <h2 class="section-title">Two ways to keep photos apart</h2>
      <p class="section-sub">Supporting sentence, one or two lines max.</p>
    </div>
    ...
  </div>
</section>
```

### Hero patterns

```html
<!-- Centered hero -->
<section class="hero">
  <div class="container">
    <h1 class="hero__title">Keep work and life photos <span class="hl">apart</span>.</h1>
    <p class="hero__sub">Subheadline.</p>
    <div class="hero__actions">
      <a class="btn btn--primary btn--lg" data-appstore>Download free</a>
      <a class="btn btn--secondary btn--lg" href="#how">See how it works</a>
    </div>
    <p class="hero__note">Free · 25 sorts a week · iPhone, iPad & Mac</p>
  </div>
</section>

<!-- Split hero: text left, visual right -->
<section class="hero hero--split">
  <div class="container">
    <div>…title/sub/actions…</div>
    <div>…image or pot-grid…</div>
  </div>
</section>
```

Highlight variants: `.hl` (cyan underline), `.hl--blue`, `.hl--orange`,
`.hl--green`.

### Pot tile grid (signature component)

```html
<ul class="pot-grid">
  <li class="pot-tile pot-tile--blue">
    <svg class="pot-tile__icon" …>…</svg>
    <div class="pot-tile__name">Work</div>
    <div class="pot-tile__meta">128 photos</div>
  </li>
  <li class="pot-tile pot-tile--orange">…</li>
  <li class="pot-tile pot-tile--green">…</li>
  <li class="pot-tile pot-tile--violet">…</li>
</ul>
```

Color modifiers: `.pot-tile--blue` `--cyan` `--orange` `--red` `--green`
`--violet`. Tiles render pastel gradient + matching glow automatically.

### Feature cards

```html
<ul class="card-grid">
  <li class="card reveal">
    <div class="card__icon card__icon--cyan"><svg …>…</svg></div>
    <h3 class="card__title">Capture straight into a pot</h3>
    <p class="card__body">The in-app camera never touches your Camera Roll.</p>
  </li>
</ul>
```

Icon chip variants: `.card__icon` (blue default), `--cyan`, `--orange`,
`--red`, `--green`, `--violet`.

### Check list

```html
<ul class="check-list">
  <li>Unlimited capture & sorting</li>
  <li>GPS metadata preserved</li>
</ul>
```

### FAQ accordion (native details/summary — no JS needed)

```html
<div class="faq faq--center">
  <details class="faq__item">
    <summary class="faq__q">Do sorted photos disappear from my Camera Roll?</summary>
    <div class="faq__a">
      <p>Yes — the original is moved into the pot, not hidden…</p>
    </div>
  </details>
</div>
```

### Pricing cards

```html
<div class="pricing-grid">
  <div class="price-card">
    <h3 class="price-card__name">Free</h3>
    <p class="price-card__price">$0 <small>forever</small></p>
    <ul class="check-list price-card__features">
      <li>25 sorts per week</li>
      <li>…</li>
    </ul>
    <a class="btn btn--secondary" data-appstore>Download free</a>
  </div>
  <div class="price-card price-card--featured">
    <span class="price-card__badge">Best value</span>
    <h3 class="price-card__name">Pro</h3>
    <p class="price-card__price">$X <small>/ month</small></p>
    <ul class="check-list price-card__features">…</ul>
    <a class="btn btn--primary" data-appstore>Go Pro</a>
  </div>
</div>
```

### CTA banner

```html
<section class="section">
  <div class="container">
    <div class="cta-banner reveal">
      <div>
        <h2 class="cta-banner__title">Your Camera Roll is not a filing system.</h2>
        <p class="cta-banner__sub">Put work photos in a work pot. It takes seconds.</p>
      </div>
      <div class="cta-banner__actions">
        <a class="btn btn--primary btn--lg" data-appstore>Download PhotoPots</a>
      </div>
    </div>
  </div>
</section>
```

### Header & footer

Copy the exact markup from `template.html`. Set
`aria-current="page"` on the active `.nav__link`.

### Utilities

`.text-center` `.text-mute` `.text-small` `.mt-2/4/6/8` `.mb-4/6`
`.grid-2` (2-col, collapses on mobile) `.position-relative` `.blob
.blob--cyan/.blob--orange` (decorative soft shapes) `.visually-hidden`.

### Scroll reveal

Add `reveal` to any block; stagger siblings with `reveal--delay-1/2/3`.
main.js handles it via IntersectionObserver and respects
`prefers-reduced-motion` (content appears instantly).

---

## 5. Voice & tone

Warm, direct, human. Talk like a person who gets the problem, not a brand
deck. Short sentences. Concrete verbs. No jargon, no hype, no cutesiness.

**Do / Don't examples**

1. ✅ "Work photos stay out of your Memories." ❌ "Leverage intelligent
   containerization to curate your photographic experience."
2. ✅ "Snap a photo at the job site — it lands straight in the work pot,
   never in your Camera Roll." ❌ "Our revolutionary capture pipeline
   redefines photo management." (hype) / ❌ "Oopsie! Your pics go
   bye-bye into the right pot!" (cutesy)
3. ✅ "Free gets you 25 sorts a week. Pro removes the limit. That's it."
   ❌ "Choose the plan that empowers your journey." 

More rules:

- "pots" is lowercase in prose; "PhotoPots" is the app.
- Say what the app *does*, not what it "empowers".
- It's fine to name the audience: contractors, agents, inspectors, nurses,
  teachers, field techs, designers.
- The key differentiator, stated plainly: sorting **moves** the photo out of
  the Camera Roll (original removed, not hidden); capture-to-pot **never
  touches** the Camera Roll.

---

## 6. File conventions

Static site, vanilla HTML/CSS/JS, no build step, deployed to Cloudflare
Pages.

- **Main pages** → root-level files: `index.html`, `features.html`,
  `how-it-works.html`, `pricing.html`, `faq.html`, `blog.html`,
  `privacy.html`, `terms.html`, `support.html`.
- **SEO landing pages & blog posts** → directory style (pretty URLs):
  `for-contractors/index.html`, `blog/sort-work-photos/index.html`.
  Pages in a subdirectory must reference assets with `../assets/...`
  (or `../../` for blog posts).
- Every page starts from a copy of `template.html`.
- Page-specific CSS goes in a `<style>` block in the page head **only** for
  a few rules; anything reusable belongs in `main.css` (propose it first).
- Images for a page live in `assets/img/` (shared) with descriptive
  kebab-case names. Always set `width`/`height` and `loading="lazy"` on
  below-fold images.
- No external JS libraries. Only external request allowed: Google Fonts.

---

## 7. Asset quick reference

| File | Purpose |
|---|---|
| `assets/img/logo.svg` | Full icon (nav, footer) |
| `assets/img/logo-mark.svg` | Petals only (compact marks) |
| `assets/img/favicon.svg` + `favicon-32.png` | Favicons |
| `assets/img/app-icon-512.png` | App icon (OG fallback, press) |
| `assets/img/app-icon-maskable-512.png` | Maskable icon (PWA-safe) |
| `assets/img/apple-touch-icon.png` | iOS home screen |
| `assets/img/og-image.png` | Default social share image (1200×630) |
| `tools/generate_assets.py` | Regenerates rasters from the app icon |
