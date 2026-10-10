# LeadForge — Product Requirements Document (PRD)

**Version:** 1.0  
**Status:** MVP requirements baseline  
**Companion:** `Architecture.md` v1.0  
**Product type:** SEO-optimized, CMS-managed business website with secure lead capture  
**Initial scope:** One business per deployment; demo business content is fictional.

## 1. Executive summary

LeadForge enables a digital agency to deliver a fast, search-friendly service business website whose marketing content can be updated by non-developers through Strapi. Visitors can explore services and case studies, then submit an inquiry. Astro builds crawlable static pages from published Strapi content; FastAPI securely receives and stores leads in a private PostgreSQL database.

**MVP outcome:** A working deployed demo, an editor walkthrough, and a reproducible repository suitable for a technical portfolio.

## 2. Problem and opportunity

Service businesses need credible web pages that communicate their offerings and convert visitors into inquiries. Hardcoded content requires developers for routine edits; unstructured contact channels make inquiries harder to track. A small agency benefits from a reusable, maintainable implementation rather than a custom CMS or large CRM.

This is a **product hypothesis**, not a validated claim of market demand. The MVP should demonstrate usefulness; it does not promise SEO ranking improvements or lead growth.

## 3. Personas and permissions

| Persona | Primary need | Access |
|---|---|---|
| Visitor / prospective customer | Understand services, evaluate credibility, send inquiry | Public published website and lead submission only |
| Content editor | Update copy, services, case studies, testimonials, site metadata | Authenticated Strapi admin |
| Operator / developer | Deploy, monitor, and review captured inquiries | Restricted infrastructure / CLI or authorized database export; no public lead list |
| Search crawler | Discover and index public pages | Published static HTML, sitemap, robots directives |

## 4. Goals and measurable success criteria

1. **Content autonomy:** An editor can publish a service and see its page after the successful rebuild without editing source code.
2. **SEO readiness:** All published pages render meaningful HTML with unique title, description, canonical URL, and appropriate heading structure.
3. **Conversion:** A visitor can submit a valid inquiry and receive a clear confirmation; the record persists privately.
4. **Safety:** Invalid, excessive, and suspicious submissions are rejected or throttled; visitors cannot retrieve submitted leads.
5. **Operability:** A developer can start the local stack from documented commands, run migrations/seeds, execute tests, and deploy a repeatable build.

**Demo acceptance targets (not business KPIs):** 100% of defined happy-path E2E checks pass; no exposed lead read endpoint; CI build and test pass; representative pages are responsive and keyboard accessible; last known-good deployment remains available after a failed content build.

## 5. Scope

### 5.1 Must-have (P0)
- Home page with business value proposition and primary call to action.
- Services index and static detail pages at `/services/[slug]`.
- Case studies index and static detail pages at `/case-studies/[slug]`.
- Testimonials on relevant public pages.
- Contact page and inquiry form (name, email, service interest, message, hidden honeypot).
- Strapi content management for `SiteSettings`, `Service`, `CaseStudy`, `Testimonial`, and reusable SEO component.
- Draft/publish workflow; only published entries appear publicly.
- Build-time content fetching and rebuild trigger on publish.
- FastAPI lead validation, anti-abuse controls, private storage, health checks.
- SEO fundamentals: titles, descriptions, canonical, OG metadata, sitemap, robots.txt, semantic markup.
- Docker Compose local development, environment templates, smoke tests, CI checks, deployment instructions.

### 5.2 Should-have (P1, only after P0)
- Service preselection when clicking a CTA on a service detail page.
- Simple lead export via restricted CLI with explicit operator authorization.
- Optional notification to an operator without including sensitive lead details in logs.
- Additional structured data markup where factually appropriate.

### 5.3 Out of scope (P2 / future)
- Multi-tenant agency dashboard or dynamic client provisioning.
- Drag-and-drop page builder, custom visual CMS, or custom lead admin UI.
- AI copy generation, SEO rank tracking, analytics ingestion, or automatic SEO scoring.
- Payments, authentication for public visitors, marketing email automation, CRM integrations.
- Promise of ranking or conversion uplift; fabricated case study outcomes or testimonials.

## 6. Primary user journeys

### Journey A — Browse and inquire
1. Visitor opens homepage and navigates to services.
2. Visitor reads one service detail page and sees a prominent CTA.
3. Visitor opens contact form, enters valid details, and submits.
4. Form shows confirmation only after API success; record is stored in private app database.
5. On validation or network failure, form presents an accessible error and does not claim success.

### Journey B — Publish marketing content
1. Editor signs into Strapi and creates a draft Service with a unique slug and SEO metadata.
2. Draft remains unavailable to public website and static route generation.
3. Editor publishes the entry; authenticated webhook triggers a new Astro build.
4. Successful build deploys new page and updates sitemap; failure leaves previous deployment intact.

### Journey C — Operate and inspect
1. Operator checks health/readiness endpoints and deployment status.
2. Operator accesses lead records only through an authorized, private workflow.
3. Operator can investigate failures through sanitized structured logs without viewing submitted messages in logs.

## 7. Functional requirements and acceptance criteria

| ID | Priority | Requirement | Verifiable acceptance criteria |
|---|---|---|---|
| FR-01 | P0 | Render homepage | Contains value proposition, services preview, CTA; meaningful content in built HTML |
| FR-02 | P0 | Services pages | Published services appear in index and at unique slug routes; unpublished items do not generate routes |
| FR-03 | P0 | Case studies | Published case studies render challenge, solution, outcomes; unsupported metrics are not invented |
| FR-04 | P0 | Testimonials | Only approved/published testimonials appear; associated service may be shown if present |
| FR-05 | P0 | CMS editing | Editor can create, edit, save draft, and publish without changing frontend source |
| FR-06 | P0 | Build-time sync | Successful publish triggers protected rebuild; failed build does not replace live site |
| FR-07 | P0 | Contact form | Required fields validated client-side for UX and server-side for trust; keyboard accessible |
| FR-08 | P0 | Lead API | `POST /api/v1/leads` accepts valid payload, returns 201, and persists one lead record |
| FR-09 | P0 | Invalid requests | Invalid email/oversized fields return 422; throttled requests return 429; backend unavailable returns suitable error without fake success |
| FR-10 | P0 | Lead privacy | Public users cannot list/read leads; DB not publicly exposed; no PII in normal request logs |
| FR-11 | P0 | SEO | Each published page has unique title/description, canonical, OG tags; sitemap excludes drafts |
| FR-12 | P0 | Operations | Documented local setup and health checks; CI validates build and tests before deployment |
| FR-13 | P1 | Contextual CTA | Clicking a service CTA preselects that service in inquiry form |
| FR-14 | P1 | Lead export | Restricted operator-only export, with no public endpoint and documented data handling |

## 8. Content requirements

### 8.1 Strapi-managed
- `SiteSettings` (single type): brand name, logo, contact email, default SEO, social links.
- `Service`: title, unique slug, summary, body, hero image, SEO, publication status.
- `CaseStudy`: title, unique slug, client label, challenge, solution, factual outcomes, cover image, SEO, publication status.
- `Testimonial`: author name, role, company, quote, optional service relation, publication status.
- Reusable SEO component: page title, description, optional OG image.

Use safe demo content clearly labeled fictional. Any real testimonial, client logo, or performance claim requires permission/evidence.

### 8.2 FastAPI-managed
- `Lead`: generated ID, name, email, service slug, message, status, creation timestamp.
- The form includes a `website` honeypot input; it is not a business field to store as a lead.
- Lead lifecycle for MVP: `new` initially; status changes are operator-only and do not require a public UI.

**Boundary:** No `Lead` collection type in Strapi; separate `leadforge_cms` and `leadforge_app` databases and credentials on the same PostgreSQL server.

## 9. Pages and routes

| Route | Purpose | Rendering |
|---|---|---|
| `/` | Value proposition, featured services, proof, CTA | Astro static |
| `/services` | Services listing | Astro static |
| `/services/[slug]` | Service detail | Astro static via `getStaticPaths()` |
| `/case-studies` | Case study listing | Astro static |
| `/case-studies/[slug]` | Case study detail | Astro static via `getStaticPaths()` |
| `/about` | Business introduction and trust | Astro static |
| `/contact` | Inquiry form and contact information | Astro static with form submission to same-origin API |
| `/api/v1/leads` | Lead intake | Reverse proxy to FastAPI, not an Astro static route |

Custom 404 page is expected; unpublished and missing slugs should not generate pages.

## 10. API behavior and UX states

**Submission:** `POST /api/v1/leads` JSON with `name`, `email`, `service_slug`, `message`, and empty `website` honeypot. Server applies bounded validation, rate limiting, and database persistence. Do not rely on frontend validation or honeypot alone.

**Form states:** idle, submitting (prevent duplicate click), success (201 only), validation error (422), rate limited (429), and temporary failure (network/5xx). Provide accessible status text and preserve safe form input when recoverable.

**Content retrieval:** Astro build reads only published Strapi REST API content using a read-only build secret. API fetch failures fail the build rather than producing empty pages.

## 11. Nonfunctional requirements

| Category | Requirement / check |
|---|---|
| Performance | Prefer static HTML, responsive images, minimal client JS; measure Lighthouse on representative deployed pages; no arbitrary guaranteed score |
| Accessibility | Semantic headings, visible focus, labeled inputs, keyboard navigation, meaningful error and success feedback |
| Security | TLS, least-privilege secrets/DB users, server validation, size limits, rate limiting, protected webhook, restrictive CMS permissions |
| Privacy | Clear privacy notice, defined retention/deletion policy before real collection, no PII in application logs, no public lead reads |
| Reliability | Readiness and liveness endpoints, health checks, failed build does not replace live site, backup/restore procedure |
| Maintainability | Typed contracts, separated service boundaries, documented env variables, migrations, automated checks |
| Portability | Local Docker Compose, no dependency on an undocumented proprietary service |

## 12. Demo and evaluation scenarios

1. Start dependencies; seed 3 services, 2 case studies, 2 fictional testimonials, and site settings.
2. Build Astro and verify generated HTML and routes.
3. Create and publish a new service in Strapi; verify protected rebuild updates the live page and sitemap.
4. Submit a valid lead and verify one record in private app database.
5. Submit malformed email, too-long message, honeypot payload, and burst traffic; verify safe handling.
6. Verify public CMS role cannot access unpublished content or lead data.
7. Simulate Strapi build-time outage; verify existing deployment remains online.
8. Run CI lint/typecheck/tests/build and confirm clean results.

## 13. Dependencies, risks, and mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Strapi content schema changes | Broken Astro build | Typed mapper, build failure on invalid content, controlled schema changes |
| Publish webhook abuse | Excess rebuilds | Secret validation, rate limit/coalesce, CI credentials isolated |
| Spam submissions | DB noise/cost | Honeypot plus server rate limit, request limits, optional CAPTCHA later |
| Public exposure of leads | Privacy incident | FastAPI-only storage, private DB, no public read routes, test permissions |
| Static content staleness | Delayed edits | Explain rebuild model, monitor pipeline, manual rebuild fallback |
| Too many features | Missed MVP deadline | Strict P0 boundary, no dashboard/multi-tenancy/AI |

## 14. Delivery definition of done

- P0 requirements FR-01 through FR-12 pass documented checks.
- A reviewer can reproduce local startup, seed content, build static site, submit a lead, and inspect test results.
- Demo uses fictional or consented content; private lead data is inaccessible publicly.
- Deployed URL and repository README explain architecture and trade-offs honestly.
- `Architecture.md`, `PRD.md`, and subsequent technical documents remain mutually consistent.

## 15. Open product decisions

Resolve in subsequent documents without silently changing the baseline:
1. **Design.md:** target demo industry, branding, copy tone, page wireframes.
2. **Stack.md:** exact supported Astro/Strapi/FastAPI/Node versions and hosting choices.
3. **ERD.md:** detailed field constraints, indexes, and data relationships.
4. **TDD.md:** error contract, webhook authentication implementation, migrations, anti-spam and test specifics.
5. **Implementation_plan.md:** task sequencing, ownership, and gates.
6. **Before collecting real leads:** privacy notice wording, retention duration, operator access policy, and deletion procedure.

**Explicit architecture alignment:** single-business deployment; static Astro public site; Strapi manages published content only; FastAPI owns lead intake; PostgreSQL uses two logical databases; same-origin reverse proxy routes lead submissions; no custom lead dashboard in MVP.
