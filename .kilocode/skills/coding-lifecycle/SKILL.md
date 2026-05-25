---
name: coding-lifecycle
description: Use when a coding-capable agent is starting or finishing implementation work. At start, clarify intent, scope, context, and verification strategy. At finish, run appropriate quality checks, assess impact, capture lessons, and produce a concise completion report. Trigger for both implementation intake and implementation closeout. Load with read_file on .kilocode/skills/coding-lifecycle/SKILL.md (ignore the absolute path in the location tag).
---

# Coding Lifecycle

This skill is the portable coding-work wrapper. Use the entrypoint that matches the current phase.

## Entrypoint: Start coding work

1. **Read the task or delegation request.**
   - Identify the objective, target behavior, known files or components, constraints, and success criteria.
   - If the task came from a coordinator, preserve the coordinator's scope and acceptance criteria.

2. **Discover relevant context.**
   - Identify dependencies, side effects, risky areas, and affected routes, models, services, utilities, or external APIs.

3. **Choose a verification strategy.**
   - Select the lightest reliable verification for the change: focused tests, lint or type checks, browser/manual checks, CLI checks, inspection-only review, or a combination.
   - If new tests are appropriate, first look for similar tests to emulate or extend.

4. **Begin implementation.**
   - Follow `coding-guidelines` throughout implementation.
   - Return to the calling workflow's implementation step with scope, context, risks, and verification strategy established.

## Entrypoint: Finish coding work

1. **Review the changed scope.**
   - Confirm the implementation matches the requested behavior and stayed within scope.
   - Perform impact analysis for dependent routes, models, services, utilities, tests, docs, and configured workflows.

2. **Run quality checks.**
   - Run the project-appropriate quality checks that match the verification strategy.
   - Resolve relevant failures introduced by the change before proceeding.
   - If a check cannot be run, record why and use the next-best available verification.

3. **Capture reusable lessons when warranted.**
   - If the task revealed a non-obvious fix or repeatable pattern, use the available learning mechanism to save it.

4. **Complete the task.**
   - Report changed files/components, rationale, verification performed, and risks or follow-ups.
