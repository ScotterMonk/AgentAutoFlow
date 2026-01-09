---
name: useful-discoveries-use
description: For (1) finding solutions, patterns, and workarounds to issues when encountering unexpected behavior, or when stuck after trying initial approaches; (2) saving solutions, patterns, and workarounds discovered during development; (3) paring down useful-discoveries, keeping only the most valuable.
---

# Useful Discoveries System

**Purpose**: `.roo/docs/useful.md` is a knowledge base for solutions, patterns, and workarounds discovered during development. If missing, create it.
**Definitions**: At bottom of this file.

## Finding solutions; when to READ from useful.md
- Before starting complex or unfamiliar tasks
- When encountering errors or unexpected behavior
- When stuck after trying initial approaches
- Before implementing workarounds or non-obvious solutions

## Saving solutions; When to WRITE to useful.md
- After solving a non-obvious bug or error
- When discovering a workaround for a limitation
- After finding an effective pattern or approach worth reusing
- When learning something about the environment, tools, or dependencies
- After resolving a problem that took significant investigation

## PARING useful.md
This involves reading through all 
**THIS SECTION IS A WORK IN PROGRESS**
**Execute sequentially. Skip nothing.**

### 1. Find redundant or similar items
**Loop**: Read through all `Items` one at a time.
Conditions:
- **You found redundant `Items` (exactly same except for date/time)**:
    **Action**: Delete the older one(s) from `Discoveries`.
- **You found similar items**:
    **Action**: Combine into one cohesive `Item` and give a new date.
    
---

## Definitions
**Item(s)**: One discovery.
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
2025-12-18 14:23 | Python | Multi-line scripts must be run from .py files, not pasted into terminal
- Context: Terminal would fail when pasting complex database queries
- Solution: Always create temporary .py files in utils_db/ for multi-line operations
- Related files: utils_db/*.py
```