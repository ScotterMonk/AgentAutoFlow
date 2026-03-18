---
name: testing
description: When creating tests and using tests for testing of application operation. Use this skill any time you are writing, running, or verifying tests — including pytest unit tests, integration tests, terminal verification scripts, or browser-based E2E flows. Trigger even for partial requests like "run the tests", "write a test for X", "verify this works", "check that the sync works", or "does this pass?". If any form of testing or verification is involved, use this skill.
---

# Testing instructions

For creating, running, and verifying tests for this application.

**Constraint**: Do not execute multi-line Python scripts directly in the terminal.

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
**One-line tests**: Run directly in the terminal (PowerShell).
**Multi-line tests**:
- Search the codebase and memory to see if an equivalent script already exists.
    - If exact: reuse it.
    - If similar: create or modify a `.py` script in `{base folder}/tests/`.
- Run the script from its `.py` file instead of pasting multiple lines.

### Python tests
**Framework**: `pytest` (see `pytest.ini` at project root).
**Test locations**:
- Unit tests: `{base folder}/tests/`
- Integration tests: `{base folder}/test_integration/` (uses `project_a/` and `project_b/` fixture folders)
- Utility/verification scripts: `{base folder}/utils_sync/` (e.g., `verify_cli_test.py`)

**Running tests**:
```powershell
# All unit tests
pytest

# Specific test file
pytest tests/test_sync_core.py

# Specific test by name
pytest tests/test_sync_core.py::test_function_name -v
```

**Creating tests**:
- Use `pytest` as the testing library.
- There is no database — do not add DB setup/teardown or connection logic.
- Tests should be self-contained: use `tmp_path` fixtures or `test_integration/` folder structures.
- Create tests so that success/green yields only the test name and "pass" for output — no descriptions or explanations in the output.

### Browser
- Use `browser-use` skill for E2E flows.
- If logging in to this application's site, use `login-using-querystring` skill.