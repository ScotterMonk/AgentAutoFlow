---
name: coding-lifecycle
description: Use when a coding-capable agent is starting or finishing implementation work. At start, clarify intent, scope, context, and verification strategy. At finish, run appropriate quality checks, assess impact, capture lessons, and produce a concise completion report. Trigger for both implementation intake and implementation closeout.
---

# Coding Lifecycle

This skill is the portable coding-work wrapper. Use the entrypoint that matches the current phase.

Before applying project-specific lifecycle checks, read the local `AGENTS.md` in this skill folder if it exists.

## Constraints

- Execute the selected entrypoint sequentially. Skip nothing.
- You are a builder, not a planner. Do not use planning-only workflows unless the user explicitly asks for planning.
- Prefer harness-neutral behavior: use the available clarification, codebase discovery, testing, memory, and completion mechanisms rather than assuming specific tool names.

## Entrypoint: Start coding work

1. **Read the task or delegation request.**
   - Identify the objective, target behavior, known files or components, constraints, and success criteria.
   - If the task came from a coordinator, preserve the coordinator's scope and acceptance criteria.

2. **Run the ambiguity gate silently.**
   - Can you state the objective in one sentence without "probably", "likely", or "I assume"?
   - Is there exactly one plausible interpretation of what should be done?
   - Are the target files, components, or discovery path known?

3. **Resolve uncertainty before editing.**
   - If any ambiguity-gate answer is "no", use the harness's clarification or ambiguity-resolution mechanism before proceeding.
   - Do not guess when a wrong interpretation would waste implementation work.

4. **Discover relevant context.**
   - Search for similar code, tests, documentation, architectural decisions, and existing utilities to reuse or extend.
   - Check available project memory or prior lessons if the harness supports it.
   - Identify dependencies, side effects, risky areas, and affected routes, models, services, utilities, or external APIs.

5. **Choose a verification strategy.**
   - Select the lightest reliable verification for the change: focused tests, lint or type checks, browser/manual checks, CLI checks, inspection-only review, or a combination.
   - If new tests are appropriate, first look for similar tests to emulate or extend.

6. **Begin implementation.**
   - Return to the calling workflow's implementation step with scope, context, risks, and verification strategy established.

## Entrypoint: Finish coding work

1. **Review the changed scope.**
   - Confirm the implementation matches the requested behavior and stayed within scope.
   - Perform impact analysis for dependent routes, models, services, utilities, tests, docs, and configured workflows.

2. **Run quality checks.**
   - Run the project-appropriate quality checks that match the verification strategy.
   - Resolve relevant failures introduced by the change before proceeding.
   - If a check cannot be run, record why and use the next-best available verification.

3. **Refactor only if needed.**
   - Keep refactoring small, relevant, and reversible.
   - Do not broaden the task unless required to make the implementation correct.

4. **Capture reusable lessons when warranted.**
   - If the task revealed a non-obvious fix, repeatable pattern, or harness/project behavior others may hit, use the available memory or learning mechanism to decide whether to save it.

5. **Complete the task.**
   - If returning to a coordinator, report changed files/components, rationale, verification performed, and risks or follow-ups through the harness's completion mechanism.
   - If responding directly to the user, provide a brief final summary of changed files/components, logic, and verification performed.
