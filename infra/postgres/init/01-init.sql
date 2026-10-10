-- ==============================================================================
-- LeadForge: PostgreSQL Multi-Database and Least-Privilege Initialization
-- Executed on clean first boot of the Postgres container
-- ==============================================================================

-- 1. Create logical databases
SELECT 'CREATE DATABASE leadforge_cms'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'leadforge_cms')\gexec

SELECT 'CREATE DATABASE leadforge_app'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'leadforge_app')\gexec

-- 2. Create CMS service user
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'leadforge_cms_user') THEN
      CREATE ROLE leadforge_cms_user LOGIN PASSWORD 'cms_secure_pass_dev_only';
   END IF;
END
$do$;

-- 3. Create FastAPI app service user
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'leadforge_app_user') THEN
      CREATE ROLE leadforge_app_user LOGIN PASSWORD 'app_secure_pass_dev_only';
   END IF;
END
$do$;

-- 4. Grant ownership and scoped privileges
GRANT ALL PRIVILEGES ON DATABASE leadforge_cms TO leadforge_cms_user;
GRANT ALL PRIVILEGES ON DATABASE leadforge_app TO leadforge_app_user;

\connect leadforge_cms
GRANT ALL ON SCHEMA public TO leadforge_cms_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO leadforge_cms_user;

\connect leadforge_app
GRANT ALL ON SCHEMA public TO leadforge_app_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO leadforge_app_user;

-- Revoke cross-database privileges
REVOKE ALL ON DATABASE leadforge_cms FROM leadforge_app_user;
REVOKE ALL ON DATABASE leadforge_app FROM leadforge_cms_user;
