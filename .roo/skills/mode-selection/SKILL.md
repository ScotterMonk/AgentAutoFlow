---
name: mode-selection
description: For understanding what each mode does, which mode is best (most appropriate mode) for a given situation, and establishing a pattern for choosing when and how a mode delegates or passes operation to another mode
---

# Mode selection

## Mode descriptions

**Location**
- Mode-specific rules live under `{base folder}/.roo/rules-*/0*-*.md`.

**For Planning & Orchestration**
- `/architect`: All-in-one planning. Create phases and tasks -> QA -> User Approval -> Switch to `/dispatcher`.
- `/planner-a`: Complex Planing Stage 1. Create phases -> Brainstorm -> Switch to `/planner-b`.
- `/planner-b`: Complex Planning Stage 2. Create detailed tasks -> User Approval -> Switch to `/planner-c`.
- `/planner-c`: Complex Planning Stage 3. QA -> Finalize -> User Approval -> Switch to `/dispatcher`.
- `/dispatcher`: Manage execution. Coordinate implementation modes. Log. Fullfill the plan.
**For Implementation & Ops**
- `/code`: Complex engineering, analysis, debugging, test creation, test execution, deep error investigation and diagnosis.
- `/code-monkey`: Routine coding, strict instruction adherence.
- `/Front-ender`: UI implementation.
- `/githubber`: GitHub CLI operations.
- `/task-simple`: Small, isolated operations.
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
    - Use `/task-simple`
2.  **Medium Budget** (Refactoring, simple function creation, writing)
    - Use `/code-monkey`
3.  **High Budget** (Complex modification, test creation and use, debugging, or if Medium fails)
    - Use `/code`.
**Special Exception**:
- **Front-ender Tasks** (Medium or High complexity): **Always use** `/Front-ender`
 