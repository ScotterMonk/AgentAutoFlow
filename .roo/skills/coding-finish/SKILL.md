---
name: coding-finish
description: When a coding or scripting mode ("code", "code-monkey", "debug", "front-end", "tester") has finished its primary task(s) and it is time for cleanup.
---

# Workflow

1) **QA**
- Resolve VS Code Problems.
- Use `app-knowledge` skill for impact analysis.

2) **Lessons learned**
    - **Share with user up to 3 lessons learned** from working through this task.
    - **For each lesson**: Present user with choices for "Save {lesson learned} to 'lessons learned'" for each lesson. **The menu presented to user must allow the user to choose one or more of the presented lessons learned.**
    - **Save their picks** via `useful-discoveries-save` skill.

3) **Completion**
- **ONLY IF current coding/scripting mode was called by orchestrator**:
    - Return to `/orchestrator`. *Do not go further in this skill or the mode that called it.*
- **ELSE IF this mode was called by user**:
    - User confirmation: user satisfied or has additional instructions?
    - Analyze what worked well and what could be improved.
    - Identify areas where additional codebase exploration might be beneficial. 