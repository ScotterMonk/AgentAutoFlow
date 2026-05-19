# Skill-local agent guidance: testing

## Project test commands
- Run all tests with `pytest`.
- Run a specific file with `pytest tests/test_sync_core.py`.
- Run a specific test with `pytest tests/test_sync_core.py::test_function_name -v`.

## Project test locations
- Unit tests: `tests/`.
- Integration fixtures: `test_integration/project_a/` and `test_integration/project_b/`.
- Utility verification scripts: `utils_sync/`, including `utils_sync/verify_cli_test.py`.

## Project constraints
- There is no database. Do not add DB setup, teardown, or connection logic.
- Tests should use temporary folders or the existing integration fixture structure.
- For browser login assumptions, first check whether a web UI exists for the task.

