---
name: coding-finish
description: When a coding or scripting mode ("code", "code-monkey", "front-ender") has finished its primary task(s) and it is time for cleanup.
---

# Workflow

**Constraints**:
- Execute sequentially. Skip nothing.
- You are not a planner; you are a builder. *Do not* use planning-related skills.
- Use only the skills you are explicitly instructed to use.

1) **QA**
- **VS Code PROBLEMS tab**: Check the PROBLEMS tab in the VS Code bottom panel (TERMINAL / PROBLEMS / OUTPUT / DEBUG CONSOLE). It shows a red count badge when errors exist. Resolve all errors shown there before proceeding.
- Use `app-knowledge` skill for impact analysis — confirm no unintended side effects on dependent routes, models, or utilities.

2) **Close out task files**
- If a `log file` was created in `.roo/docs/plans/`, append a completion entry with timestamp and brief summary of what was done.
- If a `plan file` was active, move it to `.roo/docs/plans_completed/` now that the task is done.

3) **Lessons learned?**
If any lessons potentially learned from working through this task: Check with `learning` skill.

4) **Completion**
- **ONLY IF current coding/scripting mode was called by dispatcher mode**:
    - Return to `/dispatcher` mode. *Do not go further in this skill or the mode that called it.*
- **ELSE IF this mode was called by user**:
    - Present a brief summary of what was changed (files, functions, logic).
    - Ask: "Does this look good, or do you have additional instructions?"
    - Wait for user response before finishing.
