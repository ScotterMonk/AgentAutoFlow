---
name: coding-init
description: When a coding or scripting mode needs to initiate coding execution. The modes include "code", "code-monkey", "debug", "front-end", "tester". Use this skill to set up context, understand the task, locate any existing plan, and establish the testing type before beginning work.
---

# Coding instructions

## Folders and files
- `plans folder`: `{base folder}/.roo/docs/plans/`.
- `backups folder`: `{base folder}/.roo/docs/old_versions/[filename]_[timestamp]`
- `completed plans folder`: `{base folder}/.roo/docs/plans_completed/`
- `user query file`: `{base folder}/.roo/docs/plans/p_[timestamp]_[short name]-user.md`.
- `log file`: `{base folder}/.roo/docs/plans/p_[timestamp]_[short name]-log.md`.
- `plan file`: `{base folder}/.roo/docs/plans/p_[timestamp]_[short name].md`.

## Variables
- `testing type`.

## Workflow

**Execute every step sequentially. Skip nothing.**
**Steps**:

### 1: Get input from user or delegating mode
- Seek a deep understanding of their issue and goals. Ask for guidance if necessary.

### 2. Pre-planning
- Use `app-knowledge` skill.
1) **Search**: Search for similar planning documents and architectural decisions.
2) **Recall**: Retrieve project history/memory.
3) **Risk**: Identify potential challenges.
4) **Analysis**: Define problem, intent, scope, constraints, and dependencies (routes, models, utils, APIs).
5) **Configuration**: If following config item is empty:
   - *Question: `testing type`*.
       - Display all 7 options verbatim in the question text, one per line, in exactly this order — **do not omit, merge, reorder, or summarize any of them**.
       - Follow-up suggestion buttons are optional quick-picks; they are not a substitute for showing all 7 in the question text.
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
   **Stop and wait for user response before proceeding.**

### 3. Locate existing plan
- Check the `plans folder` for a plan file matching the current task (by name or recent timestamp).
- If a relevant `plan file` exists, **read it fully** — use it as the primary guide for your work.
- If no plan file exists, that is fine — proceed without one.

### 4. Capture the request
- Create the `user query file` containing:
  - The original user request (verbatim or summarized accurately).
  - The `testing type` selected.
  - Timestamp.
- This file serves as a reference anchor if the task runs long or context drifts.

### 5. Begin
- Return to the calling mode's next workflow step. You are now initialized.
