# Skill-local agent guidance: app-knowledge

## Project knowledge sources
- Root project overview: `AGENTS.md`.
- User-facing docs: `README.md`, `README-file-sync.md`, and `README-roo.md`.
- Configuration: `config.txt`.
- GUI entrypoints: `app.py` and `main_gui.py`.
- CLI entrypoint: `cli_sync.py`.
- Core sync utilities: `utils_sync/`.
- Tests: `tests/` and `test_integration/`.
- Skill and mode scaffold: `.kilocode/` and `.kilocodemodes`.

## Important application facts
- This app synchronizes scaffold directories across project folders.
- There is no database for this project.
- Root-level synchronized files require `root_allowlist` configuration.
- Use `codebase_search` first for unexplored implementation areas.

