---
name: useful-discoveries-paring
description: For paring down useful-discoveries, removing redundancies, keeping only the most valuable useful-discoveries.
---

# Useful Discoveries System

**Purpose**: `{base folder}/.roo/docs/useful.md` is a knowledge base for solutions, patterns, and workarounds discovered during development. If missing, create it.
**Definitions**: At bottom of this file.

## Workflow for paring
This involves reading through all 
**DO NOT USE THIS PARING SKILL YET**
**PARING SECTION IS A WORK IN PROGRESS**

**FOR LATER:**
**Execute sequentially. Skip nothing.**

### 1. Find redundant or similar items
**Loop**: Read through all `Items` one at a time.
Conditions:
- **You found redundant `Items` (exactly same except for date/time)**:
    **Action**: Delete the older one(s) from `Discoveries`.
- **You found similar items**:
    **Action**: Combine into one cohesive `Item` and give a new date.
    
## Definitions
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