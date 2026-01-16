---
name: planning-init
description: When a mode needs to initiate or continue plan creation for continuation or execution by user or other modes. All planner modes (architect, planner-a, planner-b, and planner-c) *start* work.
---

# Planning instructions

## Folders and files
- `plans folder`: `{base folder}/.roo/docs/plans/`.
- `backups folder`: `{base folder}/.roo/docs/old_versions/[filename]_[timestamp]`
- `completed plans folder`: `{base folder}/.roo/docs/plans_completed/`
- `user query file`: `{base folder}/.roo/docs/plans/p_[timestamp]_[short name]-user.md`.
- `log file`: `{base folder}/.roo/docs/plans/p_[timestamp]_[short name]-log.md`.
- `plan file`: `{base folder}/.roo/docs/plans/p_[timestamp]_[short name].md`.

## Workflow

**Execute every step sequentially. Skip nothing.**
**Steps**:

### 1. Input
1) **Determine Plan status**: 
    Check `log file` and `plan file` to determine:
    - **Plan = new**: Continue past the next to possible status actions to "`2) **Determine previous mode**`".
    - **Plan = incomplete**: 
        - *Determine where progress was interrupted*,
        - Use the `new_task` tool to switch to appropriate mode with `message` parameter containing **only**:
        - "**Continue working** on the `plan` in {`plan_file`}."
        - **Critical** to not include any other context.
     - **Plan = finished**: Move `log file`, `plan file`, `user query file` to `completed plans folder`, inform user, **STOP**.

2) **Determine previous mode**:
    The following input instructions depend on which mode called current mode:
    - **Previous mode = user query**: Capture input as `user query`. Save `user query` to `user query file`.
    - **Previous mode = planner-a or planner-b**: 
        - **Action**: Load into context:
            - `plan` & `short plan name`.
            - `log file` name.
            - `user query` & `user query file` name.
            - `autonomy level`.
            - `testing type`.
        - **Validation**: If context is incomplete, alert user and **halt** immediately.
        - **Skip remaining `### 1. Input` steps down to `### 2. Pre-planning`.

3) **Short plan name**: If empty `short plan name`, derive from `user query`.
    - Create/use `user query file`.
    - Create/use `log file`.
    - Create/use `plan file`.

4) **Configuration**: If following 3 config items are empty:
    Ask user the following three questions *separately*:
    **Vital that you give exactly the choices below for each question**.
    - **Question 1: Complexity**: [] One Phase (Tiny/Small), [] One Phase (Small/Med), [] Few Phases (Med), or [] Multi-Phase (Large). Recommend best option for this `plan`.
    *Stop and wait for user response before proceeding to next question.*
    - **Question 2: Autonomy**: [] Low (frequent checks), [] Med, or [] High (rare checks).
    *Stop and wait for user response before proceeding to next question.*
    - **Question 3: Testing**: [] Terminal commands or short scripts, [] Python tests, [] Browser, [] Use what is appropriate per task, [] All, [] None, or [] Custom.
    *Stop and wait for user response before proceeding.*

### 2. Pre-planning
1) **Search**: Search for similar planning documents and architectural decisions.
2) **Recall**: Retrieve project history/memory.
3) **Risk**: Identify potential challenges.
4) **Analysis**: Define problem, intent, scope, constraints, and dependencies.

### 3. **Analysis 2**: 
- Double-check problem (`user_query`), intent, scope, constraints, and dependencies.
- Find and inform user of redundancies or other issues before continuing.
