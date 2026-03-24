---
name: learning
description: Self-improvement system for managing (finding/using, saving/adding, and pruning) solutions, patterns, lessons learned, and workarounds. Use this skill whenever a mode says "check learnings", "check memories", "prior solutions", "remember this", "save this pattern", or when you discover a non-obvious fix after 2+ failed attempts. Also trigger when encountering unexpected behavior that others might hit.
---

# Learning System
**Purpose**: Knowledge base for solutions, patterns, lessons, and workarounds.

## Definitions
**`learnings folder`**: `{base folder}/{scaffold folder}/docs/learning/` (Create if missing).
**File format**: `{category}-{subcategory}.md` (all lowercase, hyphen-separated).

**Category examples**: `python`, `flask`, `javascript`, `sql`, `css`, `testing`, `sync`, `config`, `git`, `patterns`.
**Subcategory examples**: `imports`, `routing`, `async`, `errors`, `performance`, `edge-cases`.
*(Example: `python-imports.md`, `flask-routing.md`, `testing-edge-cases.md`)*

## Workflow
**Entry routing**:
- Caller says "check learnings", "prior solutions", "patterns", "memories" → Start at **Phase 1: Find**.
- Caller says "save this", "remember this", "lesson learned", or you discover a non-obvious insight → Start at **Phase 2: Evaluate**.

---

### Phase 1: Find Learnings (when stuck or researching)
1) **Search** the `{learnings folder}` using keyword search matching the current problem domain.
2) **Read** only the matching file(s) or relevant sections.
3) **Apply** any matching Fix/Correct entries to the current task.
4) If nothing relevant found, continue without learnings — do not block progress.

---

### Phase 2: Evaluate (Fast Fail)
Analyze the conversation for reusable, non-obvious insights.
Assign a Tier:
- **Tier 1 (Global/Critical)**: Highly reusable, prevents major errors. (Save to learnings folder)
- **Tier 2 (Domain/Useful)**: Feature-specific, nice-to-know. (Save to learnings folder)
- **Tier 3 (Local/Obvious)**: One-off edge case, standard documentation. (**Skip/Exit immediately**)

*If Tier 3, exit the learning skill immediately without prompting the user.*

### Phase 3: Draft Content
For any file writes, follow `## Formatting Standards` in the `coding-markdown` skill.

**Before drafting, check for duplicates**:
- Search existing learning files for similar entries.
- **Exact match found** → Exit skill (already captured).
- **Overlapping/related found** → Append to or update the existing entry instead of creating a new file.

Use telegraphic language (→ ✅ ❌ ⚠️).
**Hard limit**: ≤30 lines per entry.

**Unified Template** (for bug fixes, errors, and gotchas):
```markdown
## [Topic/Issue Name]
<!-- meta: date=YYYY-MM-DD, tier=[1|2], status=active -->
- **Trigger/Symptom**: [What happened or when to use]
- **Cause/Mistake**: [Why it failed or common wrong approach]
- **Fix/Correct**: [The solution or right approach]
- **Why**: [1-line reason]
```
*(Optional: If the issue took 3+ attempts to solve, append a brief `Timeline:` and `Blind Spots:` section.)*

For **patterns and techniques** (not errors), a prose format with a "Recommended pattern" section is acceptable — but still include the `<!-- meta -->` comment for date tracking.

### Phase 4: Micro-Approval (BLOCKING)
Present a highly condensed summary to the user for approval:

**💡 Proposed Learning: [Category]**
- **Issue**: [1-line description]
- **Fix**: [1-line solution]
*Save to `[File]`? (y/n)*

- User approves → Save to file.
- User declines → Discard silently. Do not re-propose the same learning.
- User requests changes → Revise the draft and re-present for approval.

### Phase 5: Just-in-Time (JIT) Maintenance
Agents do not run on a schedule. Maintenance happens during active use:
- **When reading an existing learning file** to solve a current problem, check the `date` metadata.
- If an entry is > 6 months old AND you determine it is obsolete/superseded, propose to the user as part of your current response:
    - **Archive**: Move the entry to `{learnings folder}/archive/` (unchanged filename).
    - **Delete**: Remove entirely (only if the entry is proven incorrect, not just outdated).
