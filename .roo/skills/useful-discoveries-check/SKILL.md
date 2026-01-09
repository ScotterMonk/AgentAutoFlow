---
name: useful-discoveries-check
description: For finding solutions, patterns, and workarounds to issues when encountering unexpected behavior, or when stuck after trying initial approaches
---

# Useful Discoveries System
**Purpose**: `.roo/docs/useful.md` is a knowledge base for solutions, patterns, and workarounds discovered during development. If missing, create it.

**When to READ from useful.md**:
- Before starting complex or unfamiliar tasks
- When encountering errors or unexpected behavior
- When stuck after trying initial approaches
- Before implementing workarounds or non-obvious solutions

**Example Entry**:
```
2025-12-18 14:23 | Python | Multi-line scripts must be run from .py files, not pasted into terminal
- Context: Terminal would fail when pasting complex database queries
- Solution: Always create temporary .py files in utils_db/ for multi-line operations
- Related files: utils_db/*.py
```