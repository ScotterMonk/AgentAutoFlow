---
name: planning-init
description: When a planning mode (architect, planner-a, planner-b, planner-c) starts its work. This skill is *not* to be loaded for use with any other modes unless specifically called.
---

# Planning instructions

## Folders and files
- Read local `AGENTS.md` in this skill folder if it exists for project-specific plan, backup, and completed-plan folders.
- `plans folder`: Create if non-existent.
- `backups folder`: Create if non-existent.
- `completed plans folder`: Create if non-existent.
- `user query file`: Use the project plan folder and `p_[timestamp]_[short name]-user.md`.
- `log file`: Use the project plan folder and `p_[timestamp]_[short name]-log.md`.
- `plan file`: Use the project plan folder and `p_[timestamp]_[short name].md`.

## Variables
- `complexity`.
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
        - **Validation**: If context is incomplete, alert user and **halt** immediately.
        - **Skip remaining instructions in this `### 1. Input` section down to continue at `### 2. Pre-planning`.

3) **Short plan name**: If empty `short plan name`, derive from `user query`.
    - Create/use `user query file`.
    - Create/use `log file`.
    - Create/use `plan file`.

4) **Configuration**: If following 3 config items are empty:
    Recommend best `complexity` for this `plan`: One Phase (Tiny/Small), One Phase (Small/Med), Few Phases (Med), Multi-Phase (Large).
    Set `testing type` as `Use what is appropriate per task`

### 2. Pre-planning
1) **Search**: Search for similar planning documents and architectural decisions.
2) **Recall**: Retrieve project history/memory.
3) **Risk**: Identify potential challenges.
4) **Analysis**: Define problem, intent, scope, constraints, and dependencies.

### 3. **Analysis 2**: 
- Double-check problem (`user query file`), intent, scope, constraints, and dependencies.
- Find and inform user of redundancies or other issues before continuing.
 
