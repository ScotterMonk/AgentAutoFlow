# Standards-all-modes instructions

**app-standards**: "app-standards" are for all modes that plan or write scripts or code follow these app standards for communication, modularization, creation, editing, naming conventions, refactoring.

## Application knowledge
Use `app-knowledge` skill when appropriate.

## Communication
Be brief; don't echo user requests.

## Modularization
**Scope**: All logic files, including Python, JS, etc.
- **Exception**: Do NOT apply this to CSS.

**Hard Limit**:
- **Enforce** a maximum of **550 lines of code** per file (exception: main.css)
- **Split** larger files: Create more files with fewer functions rather than exceeding this limit.

**Utility Strategy**:
- **Extract** logic liberally into utility folders.
- **Location Naming Convention**: Use `{base folder}/utils/` or `{base folder}/utils_db/`.
For JS in Flask:
- **Location Naming Convention**: Use `{base folder}/static/js/utils/`.

**Build Abstractly, Reuse Aggressively**:
Take the time needed to think and search before coding.

**Before writing any code**:
- Search the codebase (and memory) to find exact *or similar* components.
  Re-use or extend existing components, templates, layout patterns, CSS patterns, and JS utilities.
- If creating a test: confirm it does not already exist.

**When building new features**, design for future equivalents or replacements using abstraction layers — not provider-specific implementations:
- **Wrong**: Separate functions per provider (e.g., `api_call_provider_a`, `api_call_provider_b`).
- **Right**: A universal abstraction layer flexible enough to handle multiple providers.
- **Wrong**: A payment system that only works with provider A.
- **Right**: A universal payment layer, extensible to plug in other providers.

**Guiding principles**:
- *Extend or generalize* existing utilities instead of duplicating.
- **Simplicity**: Choose the simplest working solution.
- Be thorough and accurate — doing this right upfront saves rework later.

## Naming Conventions: Domain-First
**Rationale**: Group related code by **Domain** (Subject) first, then **Specific** (Action/Qualifier).

### Core Pattern
**Invert the standard naming order**:
- **Bad**: `{specific}_{domain}` (e.g., `edit_user`)
- **Good**: `{domain}_{specific}` (e.g., `user_edit`)

**Casing Rules**:
- **snake_case**: Files, functions, variables, DB tables/columns.
- **PascalCase**: Classes.

### Transformation Examples
**Pattern**: *Old Pattern* --> *New Pattern (Target)*
Examples:
**Files**: `admin_dashboard_utils.py` --> `dashboard_utils_admin.py`. Domain is `dashboard`.
**Functions**: `edit_user` --> `user_edit`. Domain is `user`.
**Classes**: `AdminPerson` --> `PersonAdmin`. Better for class would be: `Person(type)`.

### Scope & Restrictions
**When to Apply**:
- **New Code**: **Always** apply this pattern.
- **Existing Code**: Apply **only** if you are already actively editing the file.

**Do NOT rename without explicit approval**:
- **Public APIs**: HTTP routes, library exports, CLI flags.
- **Database**: Tables and columns (requires migration).
- **Standards**: `__init__.py`, `setUp()`, `settings.py` (Django).

## Comments
**Preserve comments**: Do NOT delete existing, still relevant comments.
**Comment liberally**: Explain why, not just what.

## Logic & Operations
- **File Collisions**: If a file exists, append _[timestamp] to the new filename.
- **Real implementations only**: Unless otherwise specified, work should specify real functionality.
- **Avoid broad, global edits** unless explicitly planned and approved. Keep changes as small and reversible as reasonable.
- **Logging**: For complex code, build in a logging call.
- **Avoid complex CMD and PowerShell scripts**: Prefer writing python script files and then executing them, *not* trying to run python scripts in the terminal.

## Refactoring
**If you rename a symbol, you MUST fix all references.**
Before finishing, verify:
1.  [ ] **Imports**: Updated in all other files?
2.  [ ] **Calls**: Function/Class usage updated everywhere?
3.  [ ] **Tests**: Do tests still pass?
4.  [ ] **Docs**: Updated agents.md, docstrings, and comments?
5.  [ ] **VS Code**: No errors in the Problems panel?
 