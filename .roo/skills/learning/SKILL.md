---
name: learning
description: Self-improvement system for managing (finding/using, saving/adding, and paring) solutions, patterns, lessons learned, and workarounds to issues when stuck or encountering unexpected behavior.
---

# Learning System
**Purpose**: Knowledge base for solutions, patterns, lessons, and workarounds with objective scoring and lifecycle management.

## Definitions
**Learnings folder**: `{base folder}/.roo/docs/learning/` (If missing, create it).
**File format**: `{Category}-{subcategory}.md`.
**Category examples**: `Testing`, `Database`, `Flask`, `Python`, `Config`, `Dependencies`, `Performance`, `UI/UX`, `Debugging`, `Workflow`.

## Learn from Conversation
Analyze current conversation for insights worth preserving.
**If topic hint provided via `$ARGUMENTS`**: Focus on capturing that specific learning.
**If no hint provided**: Analyze full conversation for valuable insights.

### Phase 1: Deep Analysis & Scoring
#### Conversation Timeline Reconstruction
Count problem-solving attempts to determine learning complexity:
- **1 attempt → Simple learning**: Document pattern only.
- **2-3 attempts → Moderate complexity**: Include troubleshooting steps.
- **3+ attempts → Complex problem**: Full cognitive retrospective with blind spots.

**Timeline pattern detection**:
- What information changed the approach?
- What assumption was disproven?
- What blind spot was revealed?

**Learning trigger classification**:
- Error Resolution: Error → Fix → Success.
- User Correction: "That's wrong", "It should be", "Incorrect".
- Multi-Round Debug: 3+ attempts with different approaches.

#### Importance Scoring
Calculate learning score (1-27): **S × I × R**.
**1. Scope (S)**:
- **Global (3)**: Affects all tasks/workflows (e.g., critical prohibition).
- **Domain (2)**: Affects specific feature area (e.g., API authentication).
- **Local (1)**: One-off issue or edge case.

**2. Impact (I)**:
- **Critical (3)**: Prevents errors, data loss, or security issues.
- **High (2)**: Significantly improves workflow or prevents common mistakes.
- **Medium (1)**: Minor optimization or nice-to-know.

**3. Reusability (R)**:
- **High (3)**: Will be referenced frequently.
- **Medium (2)**: Occasionally useful.
- **Low (1)**: Rare edge case.

**Documentation thresholds**:
- **18-27**: Document in primary learnings folder.
- **9-17**: Document in subdirectory (specialized topic).
- **1-8**: Skip unless user explicitly requests.

**Only capture insights that are**:
1) **Reusable**: Will help in future similar situations.
2) **Non-obvious**: Not already common knowledge.
3) **Project-specific**: Relevant to this codebase.

If nothing valuable was learned (score <9), say so (if asked directly) and exit gracefully.

### Phase 2: Categorize & Locate
Read existing folders and docs within `learnings folder` to find best home.
If no existing doc fits, propose new doc file with `file format`.

### Phase 3: Draft the Learning
#### Compact Format Templates
Use telegraphic language with symbols (→ ✅ ❌ ⚠️).
**Error Learning**:
```markdown
## Error: [name]
<!-- meta: created=YYYY-MM-DD, score=[N], status=active -->
Symptom: [observable behavior]
Cause: [component:location]
Fix: [action]
Prevent: [verification step]
Ref: [file:line | doc#section]
```

**Pattern Learning**:
```markdown
## Pattern: [name]
<!-- meta: created=YYYY-MM-DD, score=[N], status=active -->
Trigger: [when this happens]
Mistake: [common wrong approach]
Correct: [right approach]
Why: [1-line reason]
```

**Design Rule**:
```markdown
## Rule: [name]
<!-- meta: created=YYYY-MM-DD, score=[N], status=active -->
Check: [what to verify]
Miss: [common oversight]
Test: [verification method]
```

**Troubleshooting (3+ attempts)**:
```markdown
## Issue: [name]
<!-- meta: created=YYYY-MM-DD, score=[N], status=active, attempts=[N] -->
Timeline:
1) [Hypothesis] → [Action] → ❌ [Why failed]
2) [Hypothesis] → [Action] → ❌ [Why failed]
3) [Hypothesis] → [Action] → ✅

Blind Spots:
- Info: [What data was missed]
- Assumption: [False belief]
- System: [Architecture gap]

Solution: [Final action]
Verify: [How to confirm fixed]
```

#### Length Constraints (CRITICAL)
**Hard limits**:
- Per learning entry: **≤30 lines**.
- Per document update: **≤50 lines** added.
- Use symbols over prose.
- Structure over paragraphs (lists, tables, bullets).

If exceeded: Extract core only, archive details separately.

#### Metadata Format (Required)
Every learning entry MUST include metadata in hidden comment:
```markdown
<!-- meta: created=YYYY-MM-DD, score=[1-27], status=active|aging|archived -->
```

**Metadata fields**:
- `created`: Date when learning was first added (YYYY-MM-DD).
- `score`: Importance score (1-27).
- `status`: `active` (in use) | `aging` (needs review) | `archived` (moved to archive).

### Phase 4: Quality Checklist (Pre-Approval)
Before presenting to user, verify:
- [ ] Score calculated with reasoning (S × I × R).
- [ ] Attempt count identified (1, 2-3, or 3+).
- [ ] Format matches template (≤30 lines).
- [ ] Metadata included in hidden comment.
- [ ] Category/file location identified.
- [ ] Non-obvious and reusable insight.
- [ ] Telegraphic language used (symbols, not prose).

### Phase 5: User Approval (BLOCKING)
Present analysis before saving:
```markdown
## 📝 Learning Analysis Complete

**Type**: [Error Resolution | Design Pattern | Workflow Improvement]
**Score**: [X/27] (S:[X] × I:[X] × R:[X])
**Classification**: [Global | Domain | Local]
**Attempts**: [N]

**Timeline**:
1) [Attempt 1] → [Outcome]
2) [Attempt 2] → [Outcome]

**Root Cause**: [1-line explanation]

**Why It Matters**: [1-2 sentences explaining impact]

---

### Proposed Update

**File**: [Category-subcategory.md]
**Section**: [New | Existing section name]
**Lines**: [N] (limit: 30)
```diff
+ [New content in compact format]

Do you approve this update?
```

**Wait for explicit user approval before saving.**

### Phase 6: Save
After approval:
1) Save the learning to identified file.
2) Confirm what was captured.
3) Note file location and section.

## Lifecycle Management
**Aging detection**: Review learnings every 6 months.
**Freshness decay**:
- 0-3 months: Active (100% score).
- 3-6 months: Active (80% score).
- 6-12 months: Aging (50% score, review needed).
- 12+ months: Archive candidate (30% score).

**When score drops below threshold due to age**: Move from primary folder to archive or specialized docs.

## Output Constraints
**MUST**:
- Request user approval before ANY file modification.
- Follow compact format rules (telegraphic, lists, symbols).
- Include metadata in hidden comments.
- Stay within length limits (30 lines/entry, 50 lines/update).

**MUST NOT**:
- Modify files without explicit approval.
- Exceed length limits.
- Use prose over structured formats.
- Document low-value learnings (score <9).

**SHOULD**:
- Prioritize global learnings over local edge cases.
- Explain reasoning behind classification and scoring.
- Preserve existing documentation style.
- Extract blind spots from multi-round debugging (3+ attempts).