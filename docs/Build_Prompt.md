# LeadForge — Autonomous Coding Agent Execution Guide

**Target Scope:** LeadForge MVP  
**Demo Identity:** Forma Studio  
**Architectural Contract:** Static Astro Frontend, Strapi 5 Editorial CMS, FastAPI Private Lead Intake, PostgreSQL Isolated Databases

---

## 1. Prime Directive

As an autonomous agent, you must execute the tasks defined in `docs/Implementation_plan.md` in strict chronological order (M0 &rarr; M1/M2 &rarr; M3 &rarr; M4 &rarr; M5 &rarr; M6).

Never claim a task or milestone gate is complete without real, reproducible command output or inspected artifact evidence.

---

## 2. Inviolable Architectural Boundaries

1. **Frontend:** Astro 5 static site generation (`output: 'static'`). Do not add Astro SSR or client-side single-page framework hydration solely for forms.
2. **Design System:** Strictly two solid base colors: `--ink: #171717` and `--paper: #F7F6F2`. Use only opacity variations for secondary text, borders, or muted backgrounds. No third brand accent color. No gradients, glows, or glassmorphism.
3. **Data Isolation:** PostgreSQL contains two logically separate databases:
   - `leadforge_cms` (managed exclusively by Strapi)
   - `leadforge_app` (managed exclusively by FastAPI + Alembic)
   - There are zero cross-database queries or shared credentials.
4. **Lead Ingestion:** Visitors submit inquiries via relative, same-origin `POST /api/v1/leads`. Reverse proxy (Nginx or Vite proxy) routes this to FastAPI. No public `GET /leads` endpoint exists.
5. **Editorial Safety:** CMS Draft & Publish must exclude unpublished entries from the static build. Rebuild failures must never overwrite the last known-good live deployment.

---

## 3. Milestone Execution Sequence

### Phase 1: Foundation (M0)
- Verify dependencies (`node >= 22`, `python >= 3.12`, `postgres >= 16`).
- Scaffold `frontend/`, `cms/`, `api/`, `infra/`, `.github/workflows/`, `.gitignore`, `.env.example`.
- Generate lockfiles (`frontend/package-lock.json`, `api/uv.lock`).
- Verify `docker compose -f infra/docker-compose.yml config`.

### Phase 2: CMS & Private Lead Service (M1 & M2)
- Define Strapi content types: `site-setting`, `service`, `case-study`, `testimonial`, `shared.seo`, `shared.cta`.
- Create seed script with realistic, explicitly fictional agency content.
- Implement FastAPI layered architecture (`router` &rarr; `service` &rarr; `repository` &rarr; `SQLAlchemy model`).
- Create and test Alembic migration for `leads` table.
- Implement `/health/live` and `/health/ready` endpoints.
- Execute unit and integration tests (`pytest`).

### Phase 3: Astro Website & SEO (M3)
- Implement two-color tokens in `tailwind.config.mjs` and `global.css`.
- Build semantic shared components (`SiteHeader`, `SiteFooter`, `ServiceRow`, `CaseStudyTile`, `TestimonialQuote`, `LeadForm`, `SEOHead`).
- Generate 7 baseline routes + `/privacy` using `getStaticPaths()`.
- Validate metadata, canonical URLs, and `sitemap-index.xml`.
- Execute static build (`npm run build`) and type check (`npm run check`).

### Phase 4: Integration & Security (M4 & M5)
- Validate same-origin proxy forwarding to FastAPI.
- Submit test inquiry and verify PostgreSQL row creation.
- Verify honeypot discard, schema 422 errors, and rate limit 429 response.
- Execute database backup and restore rehearsal.
- Verify atomic build promotion script (`deploy-webhook.py`).

### Phase 5: Handoff & Documentation (M6)
- Maintain honest documentation in root `README.md` and `docs/Verification_evidence.md`.
- Never invent metrics, testimonials, or performance guarantees.
