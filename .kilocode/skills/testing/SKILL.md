---
name: testing
description: When creating tests and using tests for testing of application operation. Use this skill any time you are writing, running, or verifying tests — including pytest unit tests, integration tests, terminal verification scripts, or browser-based E2E flows. Trigger even for partial requests like "run the tests", "write a test for X", "verify this works", "check that the sync works", or "does this pass?". If any form of testing or verification is involved, use this skill.
---

# Testing instructions

For creating, running, and verifying tests. Read local `AGENTS.md` in this skill folder if it exists for project-specific commands, paths, and environment notes.

**Constraint**: Do not execute multi-line Python scripts directly in the terminal.

**Hard rule — silent stdout means write a script**:
- If `python -c "..."` produces no terminal output, do NOT keep tweaking the same one-liner. After 2 silent runs (first = warning, second = trigger), STOP and save it as a `.py` file in an appropriate project folder, then run that file.
- Multi-line `python -c` invocations are forbidden inline. Even when they appear to work, output can be unreliable in some terminal environments.
- Pipelines that mix `python -c` with `Select-String`, `Out-File`, etc. can also drop stdout. Same rule: write a script.
- Quick shell sanity checks (`python --version`, path existence checks, single short prints) are fine and do not count.

**Procedure for Multi-line Scripts**:
1) **Search**: Check codebase and memory for existing scripts.
2) **Evaluate**:
    - **Exact Match Found**: Execute the existing script.
    - **Similar Match Found**:
        - Analyze dependencies (what relies on this script?).
        - Determine strategy: Modify existing vs. Duplicate new.
        - Execute the modified or duplicated script.
    - **No Match**: Create a new script file, then execute it.

## Testing types
    Index: Terminal Scripts, Python Tests, Browser.

### Terminal Scripts
**One-line tests**: Run directly in the terminal.
**Multi-line tests**:
- Search the codebase and memory to see if an equivalent script already exists.
    - If exact: reuse it.
    - If similar: create or modify an appropriate `.py` script.
- Run the script from its `.py` file instead of pasting multiple lines.

### Python tests
**Framework**: Use the project's existing Python test framework.
**Test locations**: Use the project's established test folders.

**Running tests**:
Use the commands documented in local `AGENTS.md` or the project root guidance.

**Creating tests**:
- Use the existing test library and project fixtures.
- Do not add database setup/teardown unless the project has a database and the test requires it.
- Tests should be self-contained; prefer temporary paths and fixtures over real project paths.
- Create tests so that success/green yields only the test name and "pass" for output — no descriptions or explanations in the output.

### Browser
- Use `browser-use` skill for E2E flows.
- If logging in to this application's site, use `login-using-querystring` skill.
