---
name: db-postgres
description: Use when the task is specifically about PostgreSQL or Supabase behavior such as slow queries, EXPLAIN plans, index design, JSONB querying, pg_stat analysis, VACUUM/autovacuum, replication, extensions, pgvector, pg_trgm, or PostGIS. Invoke whenever the user needs Postgres-specific diagnosis or exact SQL/config guidance rather than generic database advice, including cases framed as query tuning, replication lag, database bloat, managed Postgres limits, or production-safe performance work. Load with read_file on .kilocode/skills/db-postgres/SKILL.md (ignore the absolute path in the location tag).
license: MIT
metadata:
  author: https://github.com/Jeffallan
  version: "1.1.0"
  domain: infrastructure
  triggers: PostgreSQL, Postgres, Supabase, slow query, EXPLAIN ANALYZE, query plan, pg_stat_statements, JSONB, GIN index, replication lag, autovacuum, VACUUM, PostGIS, pgvector, pg_trgm
  role: specialist
  scope: analysis+implementation
  output-format: code
  related-skills: database-optimizer, devops-engineer, sre-engineer
---

# PostgreSQL Specialist

Use this skill to produce evidence-driven PostgreSQL guidance that is safe for production and efficient for the user's environment. Favor the smallest change with the highest likely impact.

## Primary Use Cases

- Optimize slow PostgreSQL or Supabase queries
- Interpret `EXPLAIN` or `EXPLAIN ANALYZE`
- Design or validate indexes
- Diagnose planner misestimates and stale statistics
- Implement or tune JSONB storage, operators, and indexing
- Configure or evaluate extensions such as `pg_stat_statements`, `pg_trgm`, `pgvector`, and PostGIS
- Diagnose replication topology, lag, and WAL retention
- Tune VACUUM, ANALYZE, autovacuum, and bloat monitoring

## First Classify the Request

Choose the primary lane, then load only the matching reference file(s):

- **Performance / query tuning** — `references/performance.md`
- **JSONB / document-style querying** — `references/jsonb.md`
- **Extensions** — `references/extensions.md`
- **Replication / HA** — `references/replication.md`
- **Maintenance / autovacuum / bloat / monitoring** — `references/maintenance.md`

Load a second reference only when the issue clearly spans two lanes, such as JSONB plus performance or replication plus maintenance. Do not load every reference file by default.

## Core Workflow

1. **Confirm environment constraints**
   - PostgreSQL version
   - Managed vs self-hosted
   - Supabase or standard PostgreSQL
   - Read/write profile, table size, query frequency, latency target
   - What the user can actually change: SQL only, indexes/migrations, extensions, database settings, or infrastructure

2. **Collect evidence before recommending changes**
   - Query text
   - Schema and current indexes
   - Relevant `EXPLAIN` or `EXPLAIN ANALYZE`
   - Cardinality and selectivity clues
   - `pg_stat_statements`, `pg_stat_user_tables`, replication, or autovacuum stats when relevant

3. **Diagnose the bottleneck**
   Common causes include:
   - Missing or poorly ordered index
   - Query shape forcing expensive scans, joins, sorts, or aggregates
   - Stale statistics or skewed data distribution
   - JSONB operator and index mismatch
   - Table or index bloat
   - Autovacuum starvation or long transactions
   - Replication slot lag or WAL retention growth
   - Managed-service limits or unsupported config changes

4. **Propose the smallest high-leverage fix**
   Prefer this order unless evidence points elsewhere:
   - Query rewrite
   - Better index or index removal
   - Statistics refresh or planner-target adjustment
   - Table-level autovacuum tuning
   - Extension enablement or operator change
   - Infrastructure or server-config changes only when truly needed

5. **Define validation and rollback**
   - What should improve
   - How to measure it
   - How to undo the change if it regresses behavior

If critical evidence is missing, state what is missing, separate confirmed findings from hypotheses, and still offer the safest low-risk next step.

## Safety and Accuracy Rules

- Use `EXPLAIN (ANALYZE, BUFFERS)` for read queries when safe.
- For write queries in production, do not casually run `EXPLAIN ANALYZE`; prefer plain `EXPLAIN`, or use an explicit transaction with rollback if the environment allows it.
- Do not prescribe indexes unless they map to actual predicates, joins, sort order, or operator usage.
- Do not disable autovacuum globally.
- Do not jump to `VACUUM FULL` on active production tables without warning about locks and considering safer alternatives.
- Do not assume superuser access or direct config-file control on Supabase or other managed PostgreSQL providers.
- Do not recommend provider-unsupported extensions or settings without saying they must be verified first.
- Prefer exact column lists over `SELECT *` in tuned production queries.
- Mention write amplification, storage cost, lock risk, and migration impact for every new index or config change.
- Never fabricate execution-plan details or monitoring output that were not provided.

## Lane-Specific Guidance

### Performance

Load `references/performance.md`.
Focus on:
- estimated vs actual row mismatch
- scan type, join type, sort, and aggregate hot spots
- buffer reads vs cache hits
- composite index order
- partial, expression, covering, GIN, GiST, or BRIN index fit
- `ANALYZE` after bulk changes

### JSONB

Load `references/jsonb.md`.
Focus on:
- operator choice such as `@>`, `?`, `->>`, and path operators
- default GIN vs `jsonb_path_ops`
- expression indexes or generated columns for hot scalar filters
- when JSONB should be normalized into first-class columns

### Extensions

Load `references/extensions.md`.
Focus on:
- whether the extension is installable in the target environment
- `pg_stat_statements` for evidence collection
- `pg_trgm`, `pgvector`, `uuid-ossp`, and PostGIS fit and tradeoffs
- extension-specific index and operator patterns

### Replication

Load `references/replication.md`.
Focus on:
- physical vs logical replication choice
- RPO/RTO and sync vs async tradeoffs
- lag measurement, slot retention, and WAL growth
- failover and client-routing implications

### Maintenance

Load `references/maintenance.md`.
Focus on:
- dead tuples, bloat risk, and last vacuum/analyze times
- per-table autovacuum tuning for high-churn tables
- long-running transactions preventing cleanup
- monitoring queries that show whether the fix is working

## Response Contract

When using this skill, provide:
1. **Diagnosis** — likely root cause and why
2. **Evidence used** — plan stats, pg_stat output, or the exact missing data needed
3. **Recommended change** — SQL, index DDL, config change, or maintenance/replication action
4. **Tradeoffs** — write overhead, lock risk, storage cost, and operational risk
5. **Validation** — exact queries or metrics to rerun
6. **Rollback** — how to undo the change when applicable

## Default Output Shape

Use this format unless the user asked for something else:

```markdown
## Findings
- ...

## Recommended SQL / config
```sql
...
```

## Why this should help
- ...

## Validation
```sql
...
```

## Risks / rollback
- ...
```

## Knowledge Reference

PostgreSQL 12-16, EXPLAIN, EXPLAIN ANALYZE, B-tree/GIN/GiST/BRIN indexes, JSONB operators, streaming replication, logical replication, VACUUM/ANALYZE, pg_stat views, PostGIS, pgvector, pg_trgm, WAL archiving, PITR
