---
name: learning
description: Self-improvement system for managing (finding/using, saving/adding, and paring) solutions, patterns, lessons learned, and workarounds to issues when stuck or encountering unexpected behavior.
---

# Learning System

**Purpose**: A knowledge base for solutions, patterns, lessons learned, and workarounds discovered during development. 

## Definitions

**Learnings folder**: `{base folder}/.roo/docs/learning/` (If missing, create it).
**File format** `{Category}-{subcategory}.md`
**Category examples**:
- `Testing`, `Database`, `Flask`, `Python`, `Config`, `Dependencies`, `Performance`, `UI/UX`, `Debugging`, `Workflow`
**Subcategory examples**:
- ``, ``, ``, ``, ``, ``, ``, ``, ``, ``

## Learn from Conversation

Analyze current conversation for insights worth preserving in the project's documentation.

**If a topic hint was provided via `$ARGUMENTS`, focus on capturing that specific learning.**
**If no hint provided, analyze the full conversation for valuable insights.**

### Phase 1: Deep Analysis

Think deeply about what was learned in this conversation:
- What new patterns or approaches were discovered?
- What gotchas or pitfalls were encountered?
- What architecture decisions were made and why?
- What conventions were established?
- What troubleshooting solutions were found?

Only capture insights that are:
1. **Reusable** - Will help in future similar situations
2. **Non-obvious** - Not already common knowledge
3. **Project-specific** - Relevant to this codebase

If nothing valuable was learned, say so (if asked directly by user) and exit gracefully.

### Phase 2: Categorize & Locate

Only within `learnings folder`: read existing docs to find the best home.
If no existing doc fits, propose a new doc file with `file format`.

### Phase 3: Draft the Learning

Format the insight to match existing doc style:
- Clear heading describing the topic
- Concise explanation of the insight
- Code examples if applicable
- Context on when this applies

### Phase 4: User Approval (BLOCKING)

Present your proposed changes:
1. What insight you identified
2. Where you'll save it (existing doc + section, or new file)
3. The exact content to add

**Wait for explicit user approval before saving.**

### Phase 5: Save

After approval, save the learning and confirm what was captured. 