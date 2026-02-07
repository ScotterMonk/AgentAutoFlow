---
name: useful-discoveries
description: Self-improvement system for managing (finding/using, saving/adding, and paring) solutions, patterns, and workarounds to issues when stuck or encountering unexpected behavior.
---

# Useful Discoveries System

**Purpose**: Useful discoveries is a knowledge base for solutions, patterns, and workarounds discovered during development. 

## Definitions

**Discoveries File**: `{base folder}/.roo/docs/useful.md` (If missing, create it).
**Item**: One discovery.
**Discoveries**: All useful discovery items in the file.
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
2025-02-18 14:23 | Python | Multi-line scripts must be run from .py files, not pasted into terminal
- Context: Terminal would fail when pasting complex database queries
- Solution: Always create temporary .py files in utils_db/ for multi-line operations
- Related files: utils_db/*.py
```

## Finding/using

### When to READ from Discoveries File
- Before starting complex or unfamiliar tasks.
- When encountering errors or unexpected behavior.
- When stuck after trying initial approaches.
- Before implementing workarounds or non-obvious solutions.

## Saving/adding 

### When to WRITE to Discoveries File
- After solving a non-obvious bug or error.
- When discovering a workaround for a limitation.
- After finding an effective pattern or approach worth reusing.
- When learning something about the environment, tools, or dependencies.
- After resolving a problem that took significant investigation.

**How to write to useful.md**
**Loop**: Read through all `Discoveries` one at a time. Execute sequentially. Skip nothing.
Conditions:
- **If You find `Item` exactly same as our new useful discovery except for date/time**:
    **Action**: Delete the older one(s) from `Discoveries`.
- **If You find `Item` similar to our new useful discovery**:
    **Action**: Combine into one cohesive `Item` and give a new date.
- **If our new useful discovery is unique**:
    **Action**: Add it to the top.

