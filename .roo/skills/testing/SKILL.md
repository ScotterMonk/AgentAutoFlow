---
name: testing
description: When creating tests and using tests for testing of application operation
---

# Testing instructions

For creating tests and using tests for testing of application operation.

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
    - Terminal Scripts, Python Tests, Browser, Use what is appropriate per task, All, None, or Custom.

### Terminal Scripts
**One-line tests**: Run directly in the terminal.
**Multi-line tests**:
- Search the codebase and memory to see if an equivalent script already exists.
    - If exact: reuse it.
    - If similar: create or modify a `.py` script in an appropriate location (default to `tests/` but `utils_db/` for DB-related tasks).
- Run the script from its `.py` file instead of pasting multiple lines.

### Python tests
Note: Uses live PostgreSQL database, not a separate test DB.
**Creating tests**:
- Use `pytest` 

### browser
- Use `browser_action` for E2E flows.
- Local querystring-based auth helper is available:
    - `http://localhost:5000/auth/login?email=[creds]&password=[hashed]`

