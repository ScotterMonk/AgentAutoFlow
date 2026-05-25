---
name: database-use
description: Any time database-related activity is required. Load with read_file on .kilocode/skills/db-use/SKILL.md (ignore the absolute path in the location tag).
---

# Database use instructions

Read skill-local guidance only when `.kilocode/skills/db-use/AGENTS.md` is confirmed to exist; otherwise use root `AGENTS.md` for project-specific database guidance.

Generic workflow:
- Identify the database engine, schema source of truth, migration process, and credential-loading path before making changes.
- Prefer existing database utilities and migration conventions over new ad-hoc scripts.
- Never hard-code credentials.
- Verify database changes with the project's test strategy.
