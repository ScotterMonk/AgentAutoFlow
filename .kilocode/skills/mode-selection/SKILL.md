---
name: mode-selection
description: For understanding what each mode does, which mode is best (most appropriate mode) for a given situation, and establishing a pattern for choosing when and how a mode delegates or passes operation to another mode. This skill provides `mode selection strategy`.
---

# Mode selection

## Mode descriptions

**Location**
- Mode-specific rules live under `{base folder}/{scaffold folder}/rules-*/0*-*.md`.

**For Planning & Orchestration**
- `/architect`: All-in-one planning. Create phases and tasks -> QA -> User Approval -> Switch to `/dispatcher`.
- `/planner-a`: Complex Planing Stage 1. Create phases -> Brainstorm -> Switch to `/planner-b`.
- `/planner-b`: Complex Planning Stage 2. Create detailed tasks -> User Approval -> Switch to `/planner-c`.
- `/planner-c`: Complex Planning Stage 3. QA -> Finalize -> User Approval -> Switch to `/dispatcher`.
- `/dispatcher`: Manage execution. Coordinate implementation modes. Log. Fullfill the plan.
**For Implementation & Ops**
- `/coder-sr`: Complex engineering, analysis, debugging, test creation, test execution, deep error investigation and diagnosis. Front-end and back-end.
- `/coder-jr`: Routine coding, test creation, test execution, strict instruction adherence. Front-end and back-end.
- `/githubber`: Git/GitHub operations.
- `/tasky`: Small, isolated work, including simple file operations.
- `/ask`: General inquiries.

## Mode selection strategy
**Evaluate** the current `task`. If another mode is more appropriate, **pass** the `task` and payload to that mode.
**Payload Requirements**:
- **Context**: Include relevant bug/issue details. If a `plan` is active, include pertinent sections.
- **Instructions**: Provide specific, actionable implementation steps.
- **Completion Trigger**: Specify the exact command to return when the task is finished.
**Response Protocol**:
- Mandate a reply via the `result` parameter containing a concise summary of the outcome.

**Prioritize** budget-friendly modes in this order (Low to High):
1.  **Low Budget** (Renaming, moving files, simple text replacement, DB column copying)
    - Use `/tasky`.
2.  **Medium Budget** (Refactoring, simple function creation, writing, or if Low fails)
    - Use `/coder-jr`.
3.  **High Budget** (Complex modification, test creation and use, debugging, or if Medium fails)
    - Use `/coder-sr`.
 