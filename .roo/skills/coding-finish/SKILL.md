---
name: coding-finish
description: When a coding or scripting mode ("coder-sr", "coder-jr", "front-ender") has finished its primary task(s) and it is time for cleanup.
---

# Workflow

**Constraints**:
- Execute sequentially. Skip nothing.
- You are not a planner; you are a builder. *Do not* use planning-related skills.
- Use only the skills you are explicitly instructed to use.

1) **QA**
- **VS Code PROBLEMS tab**: Check the PROBLEMS tab in the VS Code bottom panel (TERMINAL / PROBLEMS / OUTPUT / DEBUG CONSOLE). It shows a red count badge when errors exist. Resolve all errors shown there before proceeding.
- Use `app-knowledge` skill for impact analysis — confirm no unintended side effects on dependent routes, models, or utilities.

2) **Lessons learned?**
If any lessons were learned from working through this task: Use the `learning` skill to decide whether to save the lesson you learned.

3) **Completion**
- **ONLY IF current coding/scripting mode was called by dispatcher mode**:
    - Return to `/dispatcher` mode via `attempt_completion` with: changed files, rationale, test steps executed, risks or follow-ups.
    - *Do not go further in this skill or the mode that called it.*
- **ELSE IF this mode was called by user**:
    - Present a brief summary of what was changed (files, functions, logic).