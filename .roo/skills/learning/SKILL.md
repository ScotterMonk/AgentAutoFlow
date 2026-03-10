---
name: learning
description: Self-improvement system for managing (finding/using, saving/adding, and pruning) solutions, patterns, lessons learned, and workarounds to issues when stuck or encountering unexpected behavior.
---

# Learning System
**Purpose**: Knowledge base for solutions, patterns, lessons, and workarounds.

## Definitions
**Learnings folder**: `{base folder}/.roo/docs/learning/` (Create if missing).
**File format**: `{Category}-{subcategory}.md`.

**Category examples**: `python`, `flask`, `javascript`, `sql`, `css`, `testing`, `sync`, `config`, `git`, `patterns`.
**Subcategory examples**: `imports`, `routing`, `async`, `errors`, `performance`, `edge-cases`.
*(Example: `python-imports.md`, `flask-routing.md`, `testing-edge-cases.md`)*

## Workflow

For any file writes, be sure to follow `## Formatting Rules` section in the `coding-markdown` skill.

---

### Phase 0: Find Learnings (when stuck or researching)
*Use this phase when the calling mode asks you to "check learning skill for prior solutions" or "patterns that apply to your current task" or similar instruction involving the learning skill.*

1. **List** files in `{learnings folder}` to see what categories exist.
2. **Read** the most relevant file(s) based on the current problem domain.
3. **Apply** any matching Fix/Correct entries to the current task.
4. If nothing relevant found, continue without learnings — do not block progress.

---

### Phase 1: Evaluate (Fast Fail)
Analyze the conversation for reusable, non-obvious insights.
Assign a Tier:
- **Tier 1 (Global/Critical)**: Highly reusable, prevents major errors. (Save to main folder)
- **Tier 2 (Domain/Useful)**: Feature-specific, nice-to-know. (Save to subfolder)
- **Tier 3 (Local/Obvious)**: One-off edge case, standard documentation. (**Skip/Exit immediately**)

*If Tier 3, exit the learning skill immediately without prompting the user.*

### Phase 2: Draft Content
Use telegraphic language (→ ✅ ❌ ⚠️). 
**Hard Limits**: ≤30 lines per entry.

**Unified Template**:
## [Topic/Issue Name]
<!-- meta: date=YYYY-MM-DD, tier=[1|2], status=active -->
- **Trigger/Symptom**: [What happened or when to use]
- **Cause/Mistake**: [Why it failed or common wrong approach]
- **Fix/Correct**: [The solution or right approach]
- **Why**: [1-line reason]
*(Optional: If the issue took 3+ attempts to solve, append a brief `Timeline:` and `Blind Spots:` section).*

### Phase 3: Micro-Approval (BLOCKING)
Present a highly condensed summary to the user for approval:

**💡 Proposed Learning: [Category]**
- **Issue**: [1-line description]
- **Fix**: [1-line solution]
*Save to `[File]`? (Y/N)*
*Wait for explicit user approval before saving.*

### Phase 4: Just-in-Time (JIT) Maintenance
Agents do not run on a schedule. Maintenance happens during active use:
- **When reading an existing learning file** to solve a current problem, check the `date` metadata.
- If an entry is > 6 months old AND you determine it is obsolete/superseded, propose archiving or deleting it to the user as part of your current response.
