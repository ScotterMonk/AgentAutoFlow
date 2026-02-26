---
name: coding-finish
description: When a coding or scripting mode ("code", "code-monkey", "debug", "front-end", "tester") has finished its primary task(s) and it is time for cleanup.
---

# Workflow

**Constraints**:
- Execute sequentially. Skip nothing.
- You are not a planner; you are a builder. *Do not* use planning-related skills.
- Use only the skills you are explicitly instructed to use.

1) **QA**
- Resolve VS Code Problems.
- Use `app-knowledge` skill for impact analysis.

2) **Lessons learned?**
If any lessons potentially learned from working through this task: Check with `learning` skill.

3) **Completion**
- **ONLY IF current coding/scripting mode was called by orchestrator**:
    - Return to `/orchestrator`. *Do not go further in this skill or the mode that called it.*
- **ELSE IF this mode was called by user**:
    - User confirmation: user satisfied or has additional instructions?
    - Analyze what worked well and what could be improved.
    - Identify areas where additional codebase exploration might be beneficial. 