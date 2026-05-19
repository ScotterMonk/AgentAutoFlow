# Skill-local agent guidance: coding-python

## Project Python layout
- GUI entrypoints: `app.py` and `main_gui.py`.
- CLI entrypoint: `cli_sync.py`.
- Core utilities: `utils_sync/`.
- Tests: `tests/` and `test_integration/`.

## Project notes
- This is a Python/Tkinter and CLI file synchronization utility.
- There is no Flask application structure or active Jinja template tree in this repository unless a future task adds one.
- File sync behavior centers on scaffold directories and `utils_sync/sync_core.py`.
- Use `tmp_path` or integration fixtures for filesystem tests.

