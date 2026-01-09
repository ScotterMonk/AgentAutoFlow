---
name: useful-discoveries-save
description: For saving solutions, patterns, and workarounds discovered during development
---

# Useful Discoveries System
**Purpose**: `.roo/docs/useful.md` is a knowledge base for solutions, patterns, and workarounds discovered during development. If missing, create it.

**When to WRITE to useful.md**:
- After solving a non-obvious bug or error
- When discovering a workaround for a limitation
- After finding an effective pattern or approach worth reusing
- When learning something about the environment, tools, or dependencies
- After resolving a problem that took significant investigation

**Entry Format** (use exactly this format):
```
YYYY-MM-DD HH:MM | [Category] | [Brief description of discovery]
- Context: [What task/situation led to this]
- Solution: [What worked and why]
- Related files: [Affected or relevant files]
```

**Category Examples**:
- `Testing`, `Database`, `Flask`, `Python`, `Config`, `Dependencies`, `Performance`, `UI/UX`, `Debugging`, `Workflow`

**Example Entry**:
```
2025-12-18 14:23 | Python | Multi-line scripts must be run from .py files, not pasted into terminal
- Context: Terminal would fail when pasting complex database queries
- Solution: Always create temporary .py files in utils_db/ for multi-line operations
- Related files: utils_db/*.py
```