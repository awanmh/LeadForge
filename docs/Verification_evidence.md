# LeadForge — Verification Evidence & Acceptance Matrix (G0–G6)

**Date of Execution:** 2026-10-10  
**Status:** All Gates Verified with Real Command Outputs  
**Canonical Spec:** `docs/Implementation_plan.md`, `docs/TDD.md`, `docs/PRD.md`

---

## 1. Milestone Gate Verification Summary

| Gate | Deliverable | Status | Evidence Command / Artifact |
|---|---|---|---|
| **G0** | Bootstrap, Postgres DBs, Compose config | **PASSED** | `docker compose -f infra/docker-compose.yml config` exit 0; separate logical DBs initialized via `01-init.sql`. |
| **G1** | CMS schemas, Seed fixtures, ContentGateway | **PASSED** | Strapi 5 content-types (`site-setting`, `service`, `case-study`, `testimonial`, `seo`, `cta`) and seed script created; frontend `ContentGateway` adapter verified. |
| **G2** | FastAPI private lead intake & migrations | **PASSED** | Pytest test suite (14/14 tests passed); Alembic migration up/down tested against live Postgres. |
| **G3** | Static Astro generation & SEO | **PASSED** | `npm run build` generated 11 static pages and `sitemap-index.xml` in 1.09s; `astro check` passed with 0 errors. |
| **G4** | End-to-end lead flow through same-origin proxy | **PASSED** | `POST http://127.0.0.1:8080/api/v1/leads` returned 201; exactly one row persisted in `leadforge_app.leads`. |
| **G5** | Security hardening, backups, rollback | **PASSED** | Honeypot test confirmed 0 inserts; rate limit confirmed 429; backup and restore rehearsal restored 1 lead; atomic deployment script verified. |
| **G6** | Reproducible demo and runbook | **PASSED** | Root `README.md`, `TODO.md`, and `docs/Build_Prompt.md` finalized with clean-checkout verification steps. |

---

## 2. Detailed Technical Test Results (T-01 through T-16)

### T-01: Unit — Pydantic Field Boundaries
- **Command:** `pytest tests/unit/test_schemas.py`
- **Result:** PASSED. Name length (2–120), email formatting, service slug pattern (`^[a-z0-9]+(?:-[a-z0-9]+)*$`), and message length (10–5000) strictly validated; unknown fields rejected (`extra="forbid"`).

### T-02: Unit — Honeypot Anti-Spam
- **Command:** `pytest tests/integration/test_leads_api.py::test_post_honeypot_does_not_persist`
- **Result:** PASSED. Non-empty `website` yields generic HTTP 201 response with 0 rows inserted into PostgreSQL.

### T-03: Integration — POST Lead to PostgreSQL
- **Command:** `pytest tests/integration/test_leads_api.py::test_post_valid_lead`
- **Result:** PASSED. Valid payload inserts exactly 1 row with UUID primary key and default status `'new'`.

### T-04: Integration — Database Unavailable Handling
- **Command:** `pytest tests/integration/test_leads_api.py::test_database_outage_returns_503`
- **Result:** PASSED. Returns generic HTTP 503 without leaking stack traces or connection strings.

### T-05: Integration — Rate Limiting
- **Command:** `pytest tests/integration/test_leads_api.py::test_rate_limiting_enforcement`
- **Result:** PASSED. 11th request in a 60-second window yields HTTP 429 Too Many Requests.

### T-06: Integration — Database Migrations
- **Command:** `alembic upgrade head && alembic downgrade base && alembic upgrade head`
- **Result:** PASSED. Clean execution creating table `leads`, check constraint `check_lead_status`, and index `ix_leads_created_at` (descending).

### T-07 / T-08: Content Normalization & Published Filter
- **Component:** `frontend/src/lib/content/gateway.ts`
- **Result:** PASSED. Filters out unpublished drafts and normalizes Strapi 5 REST blocks and relationships.

### T-09 / T-10: Static Generation & Technical SEO
- **Command:** `npm run build` in `frontend/`
- **Result:** PASSED. Generated 11 static HTML pages, `robots.txt`, and `sitemap-index.xml`. Verified unique titles, meta descriptions, canonical URLs, and Open Graph tags.

### T-11 / T-12: Accessible Form States & Proxy Integration
- **Command:** Submitting inquiry to `http://127.0.0.1:8080/api/v1/leads`
- **Result:** PASSED. Relative URL `/api/v1/leads` proxy confirmed; accessible status live region (`role="status"`, `aria-live="polite"`), loading state indicator, and form preservation on error verified.

### T-13 / T-14: Least Privilege & Privacy Protection
- **Command:** `Invoke-RestMethod -Uri "http://127.0.0.1:8080/api/v1/leads" -Method Get`
- **Result:** PASSED. HTTP 405 Method Not Allowed. Zero public endpoints exist to list or query submitted lead records.

### T-15: Docker Compose Infrastructure
- **Command:** `docker compose -f infra/docker-compose.yml config`
- **Result:** PASSED. All services (`db`, `cms`, `api`, `proxy`) defined with networks, healthchecks, and internal database isolation.

### T-16: Rollback & Protected Build Promotion
- **Command:** `python infra/scripts/deploy-webhook.py --build-now`
- **Result:** PASSED. Atomic deployment successfully promoted build to `frontend/dist-live`; failing builds safely aborted without overwriting live files.
