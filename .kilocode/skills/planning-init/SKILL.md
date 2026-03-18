---
name: planning-init
description: When a planning mode (architect, planner-a, planner-b, planner-c) starts its work. This skill is *not* to be loaded for use with any other modes unless specifically called.
---

# Planning instructions

## Folders and files
- `plans folder`: `{base folder}/{scaffold folder}/docs/plans/`. Create if non-existent.
- `backups folder`: `{base folder}/{scaffold folder}/docs/old_versions/[filename]_[timestamp]`. Create if non-existent.
- `completed plans folder`: `{base folder}/{scaffold folder}/docs/plans_completed/`. Create if non-existent.
- `user query file`: `{base folder}/{scaffold folder}/docs/plans/p_[timestamp]_[short name]-user.md`.
- `log file`: `{base folder}/{scaffold folder}/docs/plans/p_[timestamp]_[short name]-log.md`.
- `plan file`: `{base folder}/{scaffold folder}/docs/plans/p_[timestamp]_[short name].md`.

## Variables
- `complexity`.
- `autonomy level`.
- `testing type`.

## Workflow

**Execute every step sequentially. Skip nothing.**
**Steps**:

### 1. Input
1) **Determine Plan status**: 
    Check for existence and content of `log file` and `plan file` to determine:
    - **Plan = new**: Continue past the next to possible status actions to "`2) **Determine previous mode**`".
    - **Plan = incomplete**: 
        - *Determine where progress was interrupted*,
        - Use the `new_task` tool to switch to appropriate mode with `message` parameter containing **only**:
        - "**Continue working** on the `plan` in {`plan_file`}."
        - **Critical** to not include any other context.
     - **Plan = finished**: Move `log file`, `plan file`, `user query file` to `completed plans folder`, inform user, **STOP**.

### 1.5: Ambiguity gate
After capturing the `user query`, answer these silently:
- Can I state the user's goal in one sentence without "probably" or "I assume"?
- Is there exactly one plausible interpretation?
- Are scope boundaries clear (what's in vs. out)?

**If any answer is "no"**: Use `resolve-ambiguity` skill. Do not proceed to pre-planning until resolved.

2) **Determine previous mode**:
    The following input instructions depend on which mode called the current mode (user or a planning mode):
    - IF **Previous mode = query from user**:
        - **Action**:
            - Capture input as `user query`. 
            - Intuit the "why" in/for the `user query`.
            - Confirm your "why" guess with the user.
            - Modify `user query` to include the "why".
            - Save `user query` to `user query file`.
    - ELSE **Previous mode = architect, planner-a or planner-b**: 
        - **Action**: Load into context:
            - `plan` & `short plan name`.
            - `log file` name.
            - `user query` & `user query file` name.
            - `complexity`.
            - `autonomy level`.
            - `testing type`.
        - **Validation**: If context is incomplete, alert user and **halt** immediately.
        - **Skip remaining instructions in this `### 1. Input` section down to continue at `### 2. Pre-planning`.

3) **Short plan name**: If empty `short plan name`, derive from `user query`.
    - Create/use `user query file`.
    - Create/use `log file`.
    - Create/use `plan file`.

4) **Configuration**: If following 3 config items are empty:
    Ask user the following three questions *separately*:
    **Vital that you give exactly the choices listed below for each question**.
    - *Question 1: `complexity`*: `[] One Phase (Tiny/Small), [] One Phase (Small/Med), [] Few Phases (Med), [] Multi-Phase (Large)`. Recommend best option for this `plan`.
    *Stop and wait for user response before proceeding to next question.*
    - *Question 2: `autonomy level`*: `[] High (rare checks), [] Medium, [] Low (frequent checks)`. Default to High.
    *Stop and wait for user response before proceeding to next question.*
    - *Question 3: `testing type`*.
        - Display all 7 options verbatim in the question text, one per line, in exactly this order — **do not omit, merge, reorder, or summarize any of them**.
        - Accept either the option number or the exact option text as a valid answer.
        - Self-check before sending: confirm all 7 appear exactly once in the question text.
        - Canonical list:
            1) Use what is appropriate per task.
            2) All
            3) None
            4) Browser.
            5) Terminal commands or short scripts.
            6) Python tests.
            7) Custom.
        - Default: option 1 ("Use what is appropriate per task").
        - **Buttons** — tool allows max 4; use exactly these follow-up suggestions in this order:
            1. `1) Use what is appropriate per task ← DEFAULT`
            2. `2) All`
            3. `3) None`
            4. `Enter 4, 5, 6, or 7 → Browser / Terminal / Python tests / Custom`
   **Stop and wait for user response before proceeding.**

### 2. Pre-planning
1) **Search**: Search for similar planning documents and architectural decisions.
2) **Recall**: Retrieve project history/memory.
3) **Risk**: Identify potential challenges.
4) **Analysis**: Define problem, intent, scope, constraints, and dependencies.

### 3. **Analysis 2**: 
- Double-check problem (`user query file`), intent, scope, constraints, and dependencies.
- Find and inform user of redundancies or other issues before continuing.
 
