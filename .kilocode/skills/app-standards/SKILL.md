---
name: app-standards
description: When any mode needs to apply, reference, or verify app standards including modularization limits, naming conventions, communication style, utility strategy, path handling, and refactoring rules.
---

# App Standards

Use this skill when a workflow explicitly says to use `app-standards` or when you need the project's shared coding, planning, path, and communication standards.

## Source of truth
- Read `.kilocode/rules/01-general.md` using a project-relative path.
- Read root `AGENTS.md` for environment, shell, path, and project-specific operational guidance.
- Do not read a skill-local `AGENTS.md` for this skill unless `.kilocode/skills/app-standards/AGENTS.md` is confirmed to exist.

## Path handling reminder
- File tools require project-relative paths with forward slashes.
- Convert any absolute skill-registry path under the workspace to `.kilocode/skills/<skill-name>/...` before reading it.
- Use `plans/` for active plans and `plans/completed/` for completed plans unless a task explicitly names a historical scaffold path.
