---
name: coding-markdown
description: When markdown being written or edited, including rules, skills, and documentation. Trigger any time a .md file is being created or modified, a skill's SKILL.md is being updated, rules files (.roo/rules/) are being edited, or a user says "update the docs", "fix the readme", "edit this skill", "write documentation", or "format this markdown".
---

# Markdown Instructions

These rules apply to the **content of project markdown files** (README, rules, skills, docs) — not to how the AI formats its own responses.

## File Path References
Strictly enforce minimalist path references to reduce noise:
- **No links**: Never use `[name](path)` syntax. Use plain backticks only.
- **No line numbers**: Strip all line number suffixes (e.g., `:22`).
- **No redundancy**: Do not repeat the filename in both brackets and parentheses.
- **Contextual pointers**: Reference section names instead of line numbers.

**Exception**: Planner modes (`/architect`, `/planner-a`, `/planner-b`, `/planner-c`) may use links when creating or modifying a plan.

Examples:
- Bad: `[app/models/user.py](app/models/user.py)` → Good: `` `app/models/user.py` ``
- Bad: `[user.py](app/models/user.py:50)` → Good: `` `app/models/user.py` ``
- Bad: `See \`rules/01-general.md\`` → Good: `See 'Critical Resources' in \`rules/01-general.md\``

## Formatting Standards

**Style & Typography**
- *Files/code*: Always use inline backtick (`file.py`). Never use brackets or links.
- *Indentation*: Use exactly 4 spaces for nested items.

**Lists & Spacing**
- *Numbering*: Use `)` as separator (e.g., `1)`, `2)`). Never use periods (`1.`).
- *Density*: No empty lines between list items. Group related items tightly.
- *Headers*: Start content on the very next line after a header — no blank line between them.
- *Punctuation*: Period at the end of every list item line.
- *Sections*: Single empty line between major sections only.

**Ordered list example**
*Bad* (wrong separator, extra spacing, missing punctuation):
```markdown
## Steps

1. First item

2. Second item
```
*Good* (correct separator, compact, punctuated):
```markdown
## Steps
1) First item.
    - Nested detail.
2) Second item.
```

**Un-ordered list example**
*Good*:
```markdown
## Points
- First item.
    - Nested detail.
- Second item.
```
