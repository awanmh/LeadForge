# LeadForge — Implementation Plan

**Version:** 1.0 | **Status:** Ready for implementation planning (not executed) | **Date:** 2026-10-10

## 1. Purpose and authority

Turn `Architecture.md`, `PRD.md`, `ERD.md`, `Stack.md`, `Design.md`, and `TDD.md` into an ordered, verifiable implementation backlog. This is a **plan**, not a claim that application code, deployments, or tests already exist.

**Priority:** P0 is required for a portfolio-ready end-to-end MVP; P1 is optional and must not delay P0. **Task state:** all tasks below start unchecked. **Execution rule:** never mark a task complete without evidence from a real command, screenshot, test, or inspected artifact.

### Immutable boundaries

- Astro static frontend; no Astro SSR requirement or separate frontend application server.
- Strapi 5 owns *public editorial content* only. FastAPI owns *private lead data* only.
- PostgreSQL with separate logical databases/roles (`leadforge_cms`, `leadforge_app`); no cross-database joins.
- `POST /api/v1/leads` is the only public lead endpoint; no anonymous read/export.
- Same-origin `/api/v1/*` routing must be proven on the chosen host before production release.
- UI uses only Ink `#171717` and Paper `#F7F6F2` (plus opacity variants), with minimal motion and no gradients, glows, glassmorphism, or fake social proof.
- Keep scope to PRD FR-01–FR-12 (P0); FR-13 and FR-14 are P1.

## 2. Repository contract

```text
leadforge/
├── README.md
├── TODO.md
├── docs/
│   ├── Architecture.md
│   ├── Build_Prompt.md
│   ├── Design.md
│   ├── ERD.md
│   ├── PRD.md
│   ├── Stack.md
│   ├── TDD.md
│   └── Implementation_plan.md
├── frontend/                 # Astro 5 + TypeScript + Tailwind
├── cms/                      # Strapi 5 content types, seed scripts
├── api/                      # Python 3.12 + FastAPI + SQLAlchemy + Alembic
├── infra/                    # Compose, Nginx, deployment configuration
└── .github/workflows/        # CI checks
```

Do not scaffold extra services or dashboards. Generated and secret files stay out of git. Lockfiles are mandatory once dependencies are installed.

## 3. Delivery milestones and task dependency map

| Milestone | Scope | Depends on | Exit gate |
|---|---|---|---|
| M0 | Toolchain, repository, security baseline | None | G0: reproducible bootstrap |
| M1 | PostgreSQL and Strapi content | M0 | G1: published-only CMS read |
| M2 | FastAPI lead intake | M0 | G2: tested DB persistence |
| M3 | Astro UI and static SEO | M1 | G3: real CMS-backed static build |
| M4 | Full-stack integration | M2 + M3 | G4: browser lead submission through proxy |
| M5 | Hardening and CI/CD | M4 | G5: security and deployment safety |
| M6 | Demo, documentation and handoff | M5 | G6: clean-checkout reproduction |

M1 and M2 can proceed in parallel after M0. No deployment gate may be skipped because a page looks finished.

## 4. Implementation backlog

### M0 — Foundation (P0; estimated 2–4 hours)

- [ ] **LF-001** Inspect all six approved design/technical docs; record inconsistencies in an implementation decision log. **Done:** decisions documented, no silent contract changes.
- [ ] **LF-002** Verify official compatibility for Astro, Strapi 5, Node, Tailwind, Python and PostgreSQL; choose supported patch versions. **Done:** actual versions recorded, no guessed package versions.
- [ ] **LF-003** Create `frontend/`, `cms/`, `api/`, `infra/`, `.github/workflows/`, `.gitignore`, and `.env.example` files. **Done:** tracked layout matches contract; no credentials committed.
- [ ] **LF-004** Set up separate PostgreSQL databases and least-privilege roles with Compose, healthchecks, named volumes, and internal network. **Done:** both DBs reachable by designated services; PostgreSQL port not published publicly.
- [ ] **LF-005** Bootstrap Astro, Strapi, FastAPI and exact lockfiles. **Done:** dependency installation reproducible from clean checkout.

**G0:** `docker compose config` validates; database healthchecks pass; frontend/CMS/API startup or build commands run without unresolved dependencies; secrets scan passes. Record exact commands and outputs.

### M1 — CMS and editorial contracts (P0; estimated 4–7 hours)

- [ ] **LF-101** Implement Strapi `SiteSettings`, `Service`, `CaseStudy`, `Testimonial`, reusable SEO/CTA components and relations per ERD. **Done:** fields, validation, slug uniqueness and draft/publish behavior match ERD.
- [ ] **LF-102** Configure private admin roles and a narrowly scoped content read token. **Done:** anonymous draft/admin reads fail; lead data does not exist in CMS.
- [ ] **LF-103** Seed realistic but explicitly fictional agency content: 3 services, 2 case studies, optional approved testimonials, site settings. **Done:** no fabricated performance metrics or real client endorsements.
- [ ] **LF-104** Implement typed CMS adapter/normalization and schema validation in frontend with explicit pagination, relations, optional media, Strapi 5 `documentId` handling. **Done:** tests cover missing required fields and valid published records.
- [ ] **LF-105** Configure protected content-change build trigger, with signature/token verification and safe failure behavior. **Done:** publish causes a test rebuild; unauthorized trigger rejected; failing rebuild never replaces live output.

**G1:** editor publishes an item; authenticated content API exposes only intended published content; adapter converts response into typed view models; T-07/T-08/T-13 relevant checks pass.

### M2 — FastAPI private lead service (P0; estimated 4–7 hours)

- [ ] **LF-201** Implement layered API modules (router → validation/service → repository → SQLAlchemy model) and request correlation IDs. **Done:** clear boundaries; no PII in routine logs.
- [ ] **LF-202** Add Alembic migration for `leads` table and constraints/indexes from ERD; use `leadforge_app` credentials only. **Done:** upgrade on empty database and downgrade/recovery tested.
- [ ] **LF-203** Implement `POST /api/v1/leads` with Pydantic input validation, length limits, honeypot, normalized status `new`, and safe 201/422/429/503 responses. **Done:** exact payload and error schema match TDD.
- [ ] **LF-204** Add bounded rate limiting, body size protection, trusted proxy/IP policy and database outage handling. **Done:** abusive traffic does not create extra records; no false success when DB is down.
- [ ] **LF-205** Implement `/health/live` and `/health/ready`, and pytest/httpx unit + real PostgreSQL integration tests. **Done:** T-01 through T-06 pass.

**G2:** one valid request creates exactly one private row; invalid/honeypot/rate-limited requests do not; no public GET leads endpoint; migrations and tests pass.

### M3 — Astro website and SEO (P0; estimated 6–10 hours)

- [ ] **LF-301** Implement two-color tokens, typography, grid, focus styles and responsive primitives exactly per `Design.md`. **Done:** visual review on mobile/tablet/desktop shows no forbidden effects.
- [ ] **LF-302** Build semantic shared components: navigation, footer, section heading, service rows, case-study previews, CTA, SEO head, accessible form states. **Done:** keyboard and screen reader behavior tested.
- [ ] **LF-303** Implement seven routes: `/`, `/services`, `/services/[slug]`, `/case-studies`, `/case-studies/[slug]`, `/contact`, `/404`. **Done:** static HTML builds from published Strapi content; drafts excluded.
- [ ] **LF-304** Implement SEO: unique titles/descriptions, canonical, Open Graph, sitemap, robots, accessible headings, structured data only where truthful. **Done:** generated HTML inspection passes T-10.
- [ ] **LF-305** Build contact form with field labels, client validation, pending/success/error states and accessible announcements. **Done:** no invented success; retries and errors usable on narrow screens.
- [ ] **LF-306** Add build-time content failure policy: fail on required CMS contract failures, safely omit optional fields, never ship stale placeholders silently. **Done:** broken CMS schema fails build and preserves previous deployed site.

**G3:** Astro static build succeeds with real published CMS data; all routes, 404, metadata and responsive behavior verified; T-09/T-10/T-11 pass.

### M4 — End-to-end integration (P0; estimated 3–5 hours)

- [ ] **LF-401** Configure Nginx/local gateway for same-origin `/api/v1/*` → FastAPI and static Astro assets; select a production host that supports equivalent routing. **Done:** request path proven, not assumed.
- [ ] **LF-402** Wire frontend form to `/api/v1/leads` using a relative URL; handle 201/422/429/503 and timeout without leaking details. **Done:** browser submission creates one DB row.
- [ ] **LF-403** Test CMS edit → publish → protected rebuild → changed static page; ensure unpublished content never appears. **Done:** documented before/after evidence.
- [ ] **LF-404** Run browser E2E for service browsing, case-study navigation and lead submission; test 404, mobile navigation and failure states. **Done:** T-12 passes and regression suite saved.

**G4:** one reproducible complete demo: editor publishes content; visitor views static pages; visitor submits inquiry; lead persists privately; frontend does not expose CMS token or DB credentials.

### M5 — Security, operations and CI/CD (P0; estimated 4–7 hours)

- [ ] **LF-501** Enforce least privilege and secret separation across Strapi, API, DB and build pipeline. **Done:** T-13/T-14 pass; no secrets in frontend bundle, Git history or logs.
- [ ] **LF-502** Harden Compose/proxy: internal-only DB, health/readiness checks, restart policy, bounded logs, secure headers, request size and timeout limits. **Done:** T-15 passes.
- [ ] **LF-503** Add CI jobs for locked install, typecheck/lint, API unit/integration tests, Astro build, secret checks and migration checks. **Done:** failure blocks deployment.
- [ ] **LF-504** Implement protected deployment workflow with immutable artifact or atomic release and rollback to last-good site. **Done:** simulated failing CMS fetch/build does not replace live site; T-16 passes.
- [ ] **LF-505** Check Lighthouse/performance, keyboard accessibility, mobile layouts, robots/sitemap, privacy notice and lead retention policy. **Done:** issues recorded and P0 regressions fixed; do not invent scores.
- [ ] **LF-506** Document PostgreSQL backup and one restore rehearsal; verify no personal data is placed in demo fixtures. **Done:** restore proof and sanitized sample data available.

**G5:** T-01 through T-16 all pass; PRD FR-01–FR-12 pass; failure and rollback tested; security review complete.

### M6 — Portfolio delivery (P0; estimated 2–4 hours)

- [ ] **LF-601** Write root `README.md` with truthful feature inventory, architecture diagram, setup commands, env reference, screenshots, demo flow and troubleshooting. **Done:** clean-checkout reader can reproduce.
- [ ] **LF-602** Record actual versions, known limitations, local and deployment URLs (only when real), CI status and privacy/data ownership notes. **Done:** no aspirational commands presented as working.
- [ ] **LF-603** Execute final scripted demo and record evidence for every PRD requirement and TDD test ID. **Done:** evidence matrix contains command/result/artifact per gate.
- [ ] **LF-604** Finalize `Build_Prompt.md` as coding-agent instructions with phase gates and no scope creep. **Done:** agent can follow task IDs without making unsupported assumptions.

**G6:** fresh clone + documented environment reproduces CMS publishing, static build and private lead submission. Only then label MVP complete.

### Optional P1 after G6

- [ ] **LF-701** FR-13: service CTA preselects inquiry service using validated query/route context.
- [ ] **LF-702** FR-14: restricted operator-only lead export with documented audit/privacy controls; no public endpoint.

## 5. Acceptance traceability

| Product requirements | Implementation tasks | Test evidence |
|---|---|---|
| FR-01–FR-04 | LF-101–104, LF-301–303 | T-07, T-08, T-09 |
| FR-05–FR-06 | LF-101, LF-105, LF-403, LF-504 | T-08, T-16 |
| FR-07–FR-09 | LF-201–205, LF-305, LF-402 | T-01–T-05, T-11, T-12 |
| FR-10 | LF-102, LF-201, LF-501–502 | T-13, T-14, T-15 |
| FR-11 | LF-303–304, LF-505 | T-09, T-10 |
| FR-12 | LF-003–005, LF-503–604 | T-06, T-15, T-16 |
| FR-13 (P1) | LF-701 | New optional E2E check |
| FR-14 (P1) | LF-702 | New restricted-access test |

## 6. Timebox and critical path

**Planning estimate, not a commitment:** ~25–44 focused engineering hours for P0 with existing backend experience but first-time Astro/Strapi usage. Setup/debugging, hosting and content model compatibility can extend this. The critical path is **M0 → M1 → M3 → M4 → M5 → M6**; M2 runs in parallel with M1/M3 where practical.

For a faster portfolio demonstration, stop after **G4** and present it as a *working local prototype*, not a production-ready application. Never claim completion of G5/G6 before evidence exists.

## 7. Known decisions to validate, not silently invent

1. Exact supported Node/Astro/Strapi/Tailwind patch versions and lockfiles (LF-002).
2. Strapi 5 REST response shape, relation populate syntax and permissions on a running instance (LF-104).
3. Hosting provider and same-origin proxy route (LF-401).
4. Protected publish webhook verification and atomic deployment behavior (LF-105, LF-504).
5. Lead retention period, privacy notice, authorized operator and consent language (LF-505).
6. Whether testimonials are published at all; never create fictitious endorsements (LF-103).

If a verification fails, log the issue, revise the relevant contract document explicitly, and rerun dependent gates.

## 8. Definition of done and reporting format

A task may be checked only when it has: (1) changed files, (2) commands/tests actually run, (3) observed results, and (4) any residual risk recorded. Suggested progress log:

```text
Task: LF-203
Status: TODO | IN_PROGRESS | BLOCKED | DONE
Files changed: ...
Verification command: ...
Observed result: ...
Blockers / next action: ...
```

**Final release rule:** no invented screenshots, testimonials, analytics, security guarantees, or claimed test results. The approved PRD, architecture, ERD, stack, design and TDD remain the sources of truth.
