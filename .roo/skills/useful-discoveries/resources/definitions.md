# Definitions

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