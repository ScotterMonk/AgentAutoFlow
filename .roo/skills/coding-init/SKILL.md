---
name: coding-init
description: When a coding or scripting mode needs to initiate coding execution. The modes include "coder-sr", "coder-sr". Use this skill to set up context, understand the task, locate any existing plan, and establish the testing type before beginning work.
---

# Coding instructions

## Variables
- `testing type`.

## Workflow

**Execute every step sequentially. Skip nothing.**
**Steps**:

### 1: Get input from user or delegating mode
1) Read the task description.
2) **Ambiguity check** — answer these silently:
   - Can I state the objective in one sentence without "probably" or "I assume"?
   - Is there exactly one plausible interpretation?
   - Do I know the target files/components?
3) **If any answer is "no"**: Use `resolve-ambiguity` skill now. Do not proceed until resolved.
4) **If all answers are "yes"**: Continue to Step 2.
5) **Check for `testing type`** from user or delegating mode. 

### 2. Pre-planning
- Use `app-knowledge` skill.
1) **Search**: Search for similar planning documents and architectural decisions.
2) **Recall**: Retrieve project history/memory.
3) **Risk**: Identify potential challenges.
4) **Analysis**: Define problem, intent, scope, constraints, and dependencies (routes, models, utils, APIs).
5) **Configuration**: 
6) **If `testing type` is empty**:
   - *Question: `testing type`*.
      - Display all 7 options verbatim in the question text, one per line, in exactly this order - **do not omit, merge, reorder, or summarize any of them**.
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

### 3. Begin
- Return to the calling mode's next workflow step. You are now initialized.
