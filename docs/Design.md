# LeadForge — Visual & Experience Design Specification

**Version:** 1.0 | **Status:** Approved design baseline for MVP | **Scope:** Single-business demo website, not a SaaS dashboard

## 1. Design intent

**Direction: Quiet confidence.** LeadForge should look like a respected independent design/technology consultancy, not a generic AI-generated startup template. The public-facing demo brand is **Forma Studio**, a fictional B2B digital experience consultancy. LeadForge remains the underlying product/repository name. Fictional case studies/testimonials must be explicitly labeled as demo content.

**Reference principles (inspiration, not reproduction):**
- **Linear:** precise alignment, disciplined spacing, restrained interface density and clear typographic hierarchy.
- **Stripe:** editorial clarity, strong content sequencing, trustworthy explanatory copy, and clear paths to action.

Do **not** copy logos, branded illustrations, layouts pixel-for-pixel, trade dress, or proprietary assets. Our execution is intentionally more editorial and less colorful than either reference.

## 2. Strict two-color system

Only two *chromatic base colors* across the entire public website:

| Token | Hex | Purpose |
|---|---|---|
| `--ink` | `#171717` | Primary text, borders, primary button fill, footer background |
| `--paper` | `#F7F6F2` | Page background, reversed text, secondary button background |

**No third brand/accent color.** Do not use gradients, purple/blue glows, neon accents, multicolored badges, decorative shadows, or default Tailwind gray palette. Subtle borders, muted labels, disabled states, overlays and hover backgrounds may use *opacity variants of ink or paper*, not additional hex colors. Photography is allowed in case studies but should be subdued, editorial, and preferably desaturated; it is content, not UI accent. Native focus outlines use ink with adequate offset. No dark-mode toggle in MVP.

```css
:root { --ink: #171717; --paper: #F7F6F2; }
body { color: var(--ink); background: var(--paper); }
::selection { background: var(--ink); color: var(--paper); }
```

## 3. Typography

- **Typeface:** `Inter` (self-hosted, variable if feasible) with system sans fallback; single family only.
- Body: 16px/1.65; secondary: 14px/1.55; captions: 12–13px/1.5.
- Desktop display: clamp(48px, 6vw, 88px), line-height 1.03, letter-spacing -0.055em, weight 500–600.
- H1 only once per page; H2 clamp(32px, 3.6vw, 52px), line-height 1.12; H3 22–28px.
- Avoid faux sophistication: all-caps paragraphs, excessive letter spacing, italic hero slogans, animated word-by-word headlines.
- Numbers and proof points use tabular numerals where relevant. Avoid unsupported metrics.

## 4. Layout system

- Content container: `max-width: 1200px`, horizontal padding 24px desktop / 20px mobile; article reading width 720px.
- 12-column grid desktop, 6-column tablet, 4-column mobile; gutters 24px desktop / 16px mobile.
- Vertical rhythm: 8px spacing scale; sections 112–144px desktop, 64–88px mobile.
- Header: 72px desktop, 64px mobile, logo wordmark left; Services, Work, Contact right. No giant nav, no sticky promotional bar.
- Corner radius: 0–4px (buttons/cards); hairline 1px borders using ink at 14–24% opacity.
- Content first. Use whitespace to create emphasis, not cards around every element.

## 5. Component specifications

| Component | Visual / behavior | Data source |
|---|---|---|
| `SiteHeader.astro` | Minimal wordmark + three links, accessible mobile menu | Static nav / site settings |
| `SiteFooter.astro` | Ink background, paper text; address/contact if provided | `SiteSettings` |
| `Hero.astro` | Eyebrow, clear outcome-focused H1, 2-line description, single solid CTA | `SiteSettings` |
| `SectionHeading.astro` | Small kicker, H2, optional paragraph | Page content |
| `ServiceRow.astro` | Number, title, short description, text-arrow link; horizontal rules | `Service` |
| `CaseStudyTile.astro` | Large 3:2 editorial image or monochrome typographic placeholder, title, sector, summary | `CaseStudy` |
| `TestimonialQuote.astro` | Oversized quotation, compact attribution; no carousel | `Testimonial` |
| `PrimaryButton.astro` | Ink fill/paper text; reversed hover with visible border | Props |
| `TextLink.astro` | Underline or directional arrow; clear focus state | Props |
| `ContactForm.astro` | Label-above-input, generous hit targets, inline validation, status region | FastAPI POST |
| `SEOHead.astro` | Title, description, canonical, OG and social tags | Strapi SEO fields |

No generic dashboard charts, fake KPI cards, glassmorphism, giant rounded pills, bouncing icons, Lottie, floating blobs, gradient backgrounds, auto-advancing testimonials, or fabricated customer logos.

## 6. Page blueprints

### `/` — Home
1. Header.
2. **Hero** (left aligned): eyebrow `INDEPENDENT DIGITAL STUDIO`; H1 `Digital experiences, built with intent.`; 1–2 sentence value proposition; CTA `Discuss a project` -> `/contact`.
3. **Selected services**: 3 numbered horizontal service rows; each links to detail.
4. **Selected work**: 2 editorial case-study tiles (real permissioned assets or clearly labeled fictional examples).
5. **Process**: three plain-text steps (`Discover / Design / Deliver`), no icon grid.
6. **Testimonial**: one approved quote, or omit section if none exists.
7. **Closing CTA**: high-contrast ink panel, `Have a project in mind?` with paper button.
8. Footer.

### `/services` — Services index
Intro H1, concise summary, vertically stacked service rows with meaningful descriptions. No pricing cards in MVP.

### `/services/[slug]` — Service detail
Breadcrumb -> H1 + value proposition -> scope / deliverables -> optional related case study -> contextual CTA linking `/contact?service=<slug>`. Missing/unpublished slug generates no page.

### `/case-studies` — Work index
Editorial grid: 2 columns desktop, 1 mobile. No category filter unless data justifies it.

### `/case-studies/[slug]` — Case study detail
Hero, project context, challenge, approach, outcome, large supporting media, next step CTA. Demo content must not invent client relationships or claim real performance gains.

### `/contact` — Lead capture
Left: brief invitation and what happens next. Right: accessible form fields `name`, `email`, `service` (optional), `message`, hidden honeypot `website`. No multi-step wizard. No phone requirement. Add a concise privacy note and no unverified response-time promises.

### `404`
One-line explanation, link back to home, consistent header/footer.

## 7. Contact form UX and accessibility

- Required: name, email, message; service interest optional; labels always visible; helper text for constraints.
- States: idle, submitting (disabled submit + progress label), success only after HTTP 201, validation error (422), rate limit (429), server/network failure (5xx/timeout).
- Preserve non-sensitive form input after recoverable errors; do not clear until confirmed success.
- Put a text summary in `role="status"` / `aria-live="polite"`; validation errors linked via `aria-describedby` and announced appropriately.
- Honeypot hidden visually and from assistive technology; FastAPI validates independently.
- Keyboard focus visible at 2px minimum; touch targets at least 44x44px; semantic landmarks; no hover-only interactions.
- Contrast: ink on paper and paper on ink are high contrast; opacity-muted text must still meet WCAG AA 4.5:1 for normal text. Test actual computed contrast.

## 8. Responsive behavior

| Breakpoint | Rules |
|---|---|
| `< 640px` | Single-column sections, compact header/menu, full-width form/buttons where helpful; hero 44–52px |
| `640–1023px` | Reduced gutters; flexible 2-column areas only where legible |
| `>= 1024px` | 12-column grid; home hero max 9 columns; contact 5/7 split; work grid 2 columns |

No horizontal overflow at 320px viewport. Images preserve aspect ratio; avoid text embedded in images. Responsive menu is the only optional small client-side JS in the header.

## 9. Motion policy

- Functional only: link underline, arrow translation <= 3px, border/fill transitions 120–180ms.
- No entrance-on-scroll animation, parallax, auto-play video, marquee, or typewriter effects.
- Respect `prefers-reduced-motion: reduce` by disabling nonessential transitions.

## 10. Content and image direction

- Tone: concise, specific, professional; use verbs and concrete deliverables, not hype.
- Forbidden phrases: `revolutionize`, `unlock limitless potential`, `next-generation solutions`, `seamless synergy`, unless supported by precise context.
- Service copy answers **what / for whom / deliverables / next step**.
- Work imagery: authentic screenshots, architecture diagrams, or licensed editorial photos; avoid stock handshakes, robot heads, abstract glowing AI brains, and generic 3D spheres.
- No customer logos, awards, testimonials, or conversion numbers without permission and evidence.
- Alt text communicates purpose, not `image of...` filler; decorative imagery gets empty alt.

## 11. CMS-to-UI content contract

- `SiteSettings`: brand name, tagline, hero copy, contact information, default SEO fields.
- `Service`: title, slug, short description, body, optional thumbnail, SEO component.
- `CaseStudy`: title, slug, client/sector (fictional clearly labeled if demo), challenge, solution, results, cover image, SEO.
- `Testimonial`: quote, author, role/company, optional service relation, publication status.
- Draft content must not appear in Astro static paths or navigation. Build fails loudly if required content is absent; do not quietly render broken/empty sections.
- Optional content sections should disappear gracefully rather than show dummy placeholders in production.
- Strapi admin uses its standard UI; **no Strapi admin redesign** in scope.

## 12. Performance, SEO and QA design gates

- Static HTML pages must contain real H1 and body copy before hydration; no client-only content dependency.
- Use responsive image sizing, explicit dimensions, lazy-load below-the-fold images, reserve hero image space; optimize with Astro image pipeline when feasible.
- Avoid full SPA hydration, heavy animation libraries and UI component suites.
- Test keyboard navigation, 320/375/768/1024/1440px layouts, form error/success states, long titles, missing optional images, and empty testimonial collection.
- Validate page titles, descriptions, canonical URLs, OG tags and readable heading hierarchy on all published routes.
- Target good Core Web Vitals; report measured results rather than promising arbitrary Lighthouse scores.

## 13. Implementation-ready design acceptance checklist

- [ ] Public UI uses only `#171717` and `#F7F6F2` as base colors; any shades are opacity variants.
- [ ] No gradients, decorative glow, glassmorphism, pill-card grids, fabricated social proof or AI stock imagery.
- [ ] Home, services, service detail, work, work detail, contact and 404 implemented.
- [ ] All public content loads from published Strapi entries at build time; no hardcoded business data beyond demo fallback fixtures.
- [ ] Contact form handles 201/422/429/5xx and keyboard/screen-reader behavior.
- [ ] Works from 320px mobile to 1440px desktop without horizontal overflow.
- [ ] Accessible focus states and reduced-motion preference verified.
- [ ] Representative screenshots reviewed manually before completion.

## 14. Explicit design decisions

- D-01: Two-color **ink/paper** visual system instead of black/white plus accent.
- D-02: Reference **Linear's precision** and **Stripe's editorial trust**, not their exact styling.
- D-03: Demo business identity **Forma Studio**, repository/product **LeadForge**.
- D-04: Editorial service rows instead of SaaS pricing cards.
- D-05: Native Strapi admin remains uncustomized.
- D-06: No animation dependencies or decorative UI until measurable UX need emerges.

**Next:** `TDD.md` should translate these UI contracts into Astro component interfaces, Strapi fetch adapters, API validation, and test cases.
