# LeadForge — Implementation Decision Log (ADR & Compatibility)

**Date:** 2026-10-10  
**Tasks:** LF-001, LF-002  
**Status:** Approved & Frozen

---

## 1. Documentation Reconciliation (LF-001)

| Area | Variation Across Docs | Resolved Canonical Contract | Rationale |
|---|---|---|---|
| Health Check Paths | `Architecture.md` mentions `/health` & `/ready`; `TDD.md` specifies `/health/live` & `/health/ready`. | `/health/live` (process liveness) and `/health/ready` (DB readiness). | README line 121 and TDD Section 6.4 declare this the authoritative contract. |
| Lead Endpoint Architecture | `Architecture.md` discusses either SSR Astro endpoint or reverse proxy; `TDD.md` & `PRD.md` require same-origin reverse proxy. | Relative `POST /api/v1/leads` reverse-proxied via Nginx to FastAPI; Astro frontend remains purely static. | Satisfies requirement for static-first frontend with zero secrets or SSR complexity in client build. |
| Palette & Tokens | Modern web aesthetics vs strict two-color mandate. | Exactly `--ink: #171717` and `--paper: #F7F6F2`, plus opacity variants (e.g. `rgba(23,23,23,0.15)`). No third brand accent color. | `Design.md` section 2 non-negotiable rule. |
| Public Routes | PRD lists 7 pages plus `/about` in some tables; `Design.md` & `TDD.md` specify 7 baseline routes + `/privacy`. | Baseline: `/`, `/services`, `/services/[slug]`, `/case-studies`, `/case-studies/[slug]`, `/contact`, `/privacy`, `/404`. | Matches `Design.md` blueprint and `TDD.md` section 5.1. |
| Lead Honeypot Handling | Empty string validation. | Field `website` must be empty. If filled, API responds with HTTP 201 without persisting to DB. | Prevents confirming anti-bot heuristics to automated scrapers. |

---

## 2. Version Verification & Compatibility Matrix (LF-002)

| Dependency / Runtime | Verified Environment Version | Release Target | Compatibility Confirmation |
|---|---|---|---|
| **Node.js** | `v22.12.0` (Host) / `node:22-alpine` (Docker) | Node 22 LTS | Compatible with Astro 5 and Strapi 5. |
| **npm** | `11.6.2` | npm 11.x | Standard lockfile format. |
| **Astro** | `astro@^5.0.0` | Astro 5 | Static HTML output mode (`output: 'static'`). |
| **Tailwind CSS** | `@tailwindcss/vite` or `@astrojs/tailwind` | Tailwind CSS | Zero runtime JS; compiles static utility CSS. |
| **Python** | `3.12.10` (via `py -3.12`) / `python:3.12-slim` | Python 3.12 | Supported by FastAPI, SQLAlchemy 2.x, Alembic, and Pydantic 2.x. |
| **Package Manager (Python)** | `uv 0.13.0` | `uv` with `pyproject.toml` | Fast, deterministic dependency resolution. |
| **PostgreSQL** | `16-alpine` (Docker) / `17.5` (Host fallback) | PostgreSQL 16 | Supported by both Strapi 5 and SQLAlchemy 2.0 / Psycopg 3. |
| **Reverse Proxy** | `nginx:1.27-alpine` | Nginx stable | Tested reverse proxy for same-origin routing and rate limiting. |

---

## 3. Decision Sign-Off

All boundaries confirmed per `Architecture.md` v1.0, `PRD.md` v1.0, `ERD.md` v1.0, `Design.md` v1.0, `Stack.md` v1.0, and `TDD.md` v1.0. No architectural compromises permitted.
