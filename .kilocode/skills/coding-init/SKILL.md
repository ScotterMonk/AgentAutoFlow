---
name: coding-init
description: When a coding or scripting mode needs to initiate coding execution. The modes include "code", "coder-sr", "coder-jr". Use this skill to set up context, understand the task, locate any existing plan, and establish the testing type before beginning work.
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

### 2. Pre-planning
Use `app-knowledge` skill:
1) **Search**: Search for similar planning documents and architectural decisions.
2) **Recall**: Retrieve project history/memory.
3) **Risk**: Identify potential challenges.
4) **Analysis**: Define problem, intent, scope, constraints, and dependencies (routes, models, utils, APIs).

### 3. Begin
- Return to the calling mode's next workflow step. You are now initialized.
