# LeadForge Implementation Checklist

## Milestone Progress

- [x] **M0: Foundation & Toolchain (G0: PASSED)**
  - [x] LF-001: Inspect approved docs & record decision log (`docs/Implementation_decision_log.md`)
  - [x] LF-002: Verify version compatibility (Astro 5, Python 3.12, Node 22, Postgres 16/17)
  - [x] LF-003: Scaffold folders, `.gitignore`, `.env.example`, `.github/workflows/ci.yml`
  - [x] LF-004: Postgres logical databases (`leadforge_cms`, `leadforge_app`), Docker compose, init script
  - [x] LF-005: Bootstrap dependencies & lockfiles (`frontend/package-lock.json`, `api/uv.lock`)

- [x] **M1: CMS & Editorial Contracts (G1: PASSED)**
  - [x] LF-101: Strapi content types (`site-setting`, `service`, `case-study`, `testimonial`, `seo`, `cta`)
  - [x] LF-102: Private admin roles & read token policy
  - [x] LF-103: Seed realistic fictional agency content (`cms/scripts/seed-demo.js`)
  - [x] LF-104: ContentGateway & adapter in frontend with schema validation & fallback fixtures
  - [x] LF-105: Protected publish trigger with token validation (`infra/scripts/deploy-webhook.py`)

- [x] **M2: FastAPI Private Lead Service (G2: PASSED)**
  - [x] LF-201: Layered API modules (router -> service -> repo -> SQLAlchemy model)
  - [x] LF-202: Alembic migration for `leads` table and constraints
  - [x] LF-203: `POST /api/v1/leads` with Pydantic validation, honeypot, status `new`
  - [x] LF-204: Rate limiting, body size limits, error handling
  - [x] LF-205: Health endpoints (`/health/live`, `/health/ready`), pytest + httpx test suite (14/14 passed)

- [x] **M3: Astro Website & SEO (G3: PASSED)**
  - [x] LF-301: Strict two-color tokens (`#171717`, `#F7F6F2`), Inter typography, responsive layout
  - [x] LF-302: Reusable components (`BaseLayout`, `SiteHeader`, `SiteFooter`, `ServiceRow`, `CaseStudyTile`, `TestimonialQuote`, `LeadForm`, `SEOHead`)
  - [x] LF-303: Seven routes + `/privacy` (`/`, `/services`, `/services/[slug]`, `/case-studies`, `/case-studies/[slug]`, `/contact`, `/privacy`, `/404`)
  - [x] LF-304: SEO (Open Graph, canonical URLs, meta tags, sitemap, robots.txt)
  - [x] LF-305: Lead form UX (client validation, accessible announcements, pending/success/error states)
  - [x] LF-306: Build-time content failure policy & fallback fixtures
  - [x] Static generation verified: 11 pages built in 1.09s, `astro check` passed with 0 errors

- [x] **M4: Full-Stack Integration (G4: PASSED)**
  - [x] LF-401: Reverse proxy config (Nginx same-origin `/api/v1/leads` & static Astro assets)
  - [x] LF-402: Lead form wired to relative `/api/v1/leads` endpoint
  - [x] LF-403: Publishing to build flow verification
  - [x] LF-404: End-to-end integration verified: lead created in PostgreSQL via proxy

- [x] **M5: Security, Operations & CI/CD (G5: PASSED)**
  - [x] LF-501: Secret separation & least privilege validation
  - [x] LF-502: Hardened Docker compose & proxy headers
  - [x] LF-503: CI GitHub Actions workflows
  - [x] LF-504: Rollback and deployment safety verification
  - [x] LF-505: Accessibility, performance & privacy audit (`/privacy`)
  - [x] LF-506: Postgres backup and restore script verified

- [x] **M6: Portfolio Delivery (G6: PASSED)**
  - [x] LF-601: Root `README.md` runbook & documentation
  - [x] LF-602: Actual versions & environment notes
  - [x] LF-603: Verification evidence matrix (`docs/Verification_evidence.md`)
  - [x] LF-604: Final `docs/Build_Prompt.md`
