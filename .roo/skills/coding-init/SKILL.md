---
name: coding-init
description: When a coding or scripting mode needs to initiate coding execution. The modes include "code", "code-monkey", "debug", "front-end", "tester"
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
- `autonomy level`.
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
5) **Configuration**: If following 2 config items are empty:
   Ask user the following three questions *separately*:
   **For each question below, vital that you show the user exactly the choices below**.
   - **Question 1: `autonomy level`**: [] Low (frequent checks), [] Med, or [] High (rare checks).
   *Stop and wait for user response before proceeding to next question.*
   - **Question 2: `testing type`** - **For user choices, use exactly all 7 of the following testing types listed as a choice here**: [] Browser, [] Terminal commands or short scripts, [] Python tests, [] Use what is appropriate per task, [] All, [] None, or [] Custom.
   *Stop and wait for user response before proceeding.*
