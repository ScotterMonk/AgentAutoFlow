# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Type
Python file synchronization utility for `.roo` directories across multiple project folders.

## Run Commands
GUI: `py main_gui.py`
CLI: `python cli_sync.py <folder1> <folder2> ...`
Tests: `pytest tests/`

## Common paths through app

### GUI: app startup
1) `main_gui.py` (module entrypoint): creates the Tk root window.
2) `MainApp.__init__()`: loads config, creates the event queue, and constructs the sync engine.
3) `MainApp._create_widgets()`: builds the UI.
4) `MainApp._process_events()`: starts periodic polling of the event queue.
5) Tkinter event loop: `root.mainloop()`.

### GUI: "Load favorites"

1) User clicks **Load Favorites** → `MainApp._load_favorite_folders()`.
2) Loads the favorites list from in-memory `MainApp.favorite_folders` (initialized from config during `MainApp.__init__()`).
3) For each favorite folder:
   - `file_path_utils.normalize_path(fav)`
   - `file_path_utils.ensure_roo_dir(normalized)` (creates `.roo/` for new projects)
   - `file_path_utils.has_roo_dir(normalized)` (validates folder has `.roo/`)
   - if valid and not already selected, appends to `MainApp.selected_folders`.
4) If any folders were added, refreshes the folder list via `MainApp._update_folder_list_ui()`.
5) If any favorites were invalid, shows an informational dialog via `messagebox.showinfo("Favorites Skipped", ...)`.

### GUI: "Scan" (plan/preview only)
1) User clicks **Scan** → `MainApp._start_sync()`.
2) `SyncEngine.scan_folders(folders)`
   - emits `EventType.SCAN_START`, then many `EventType.SCAN_FILE` events while walking each `{folder}/.roo/**`.
   - also scans any `root_allowlist` files at the folder root.
3) `SyncEngine.plan_actions(file_index, scanned_folders=folders)`
   - computes the newest source file per relative path, then creates a list of copy actions for older/missing destinations.
4) GUI stores the planned actions and renders previews via `MainApp._update_overwrite_previews()`.

### GUI: "Execute" (apply planned actions)
1) User clicks **Execute** → `MainApp._confirm_sync()`.
2) `SyncWorker.__init__(sync_engine, folders, actions=planned_actions)` then `SyncWorker.start()`.
3) Background thread runs `SyncWorker.run()`:
   - calls `SyncEngine.execute_actions(actions)`.
   - for each copy action, emits `EventType.COPY` (or `EventType.SKIP` in dry-run) and finally `EventType.COMPLETE`.
4) GUI receives updates in `MainApp._process_events()` and updates folder row statuses.

### CLI: headless sync
1) `cli_sync.py` (module entrypoint) → `_parse_args()` → `run_cli_sync(args.folders)`.
2) `load_config(args.config)`.
3) Ensures each folder has a `.roo/` directory (creates it if missing).
4) Constructs `SyncEngine(config, event_queue)`.
5) Runs sync:
   - tries `SyncEngine.run_sync(folders)` if present; otherwise falls back to:
   - `SyncEngine.scan_folders(folders)` → `SyncEngine.plan_actions(file_index, scanned_folders=folders)` → `SyncEngine.execute_actions(actions)`.
6) Drains the queue and prints events via `_print_event()`.

## Environment & Shell
Windows 11, VS Code, PowerShell.
**Base folder**: "d:\Dropbox\Projects\AgentFlow\app\". Convert between "\" and "/" as necessary.
**Prefer PowerShell**: This project is developed on Windows. Agents should assume a PowerShell environment (`pwsh`) for terminal commands.
**Avoid cmd.exe pitfalls**: Be aware that `cmd.exe` does not treat `;` as a command separator (use `&` or `&&` instead). If a command fails with "shell is treating ; as an argument", it likely ran in `cmd.exe`.
**VS Code Settings**: The workspace is configured to default to PowerShell (`.vscode/settings.json`).

## Critical Non-Standard Patterns

### File Sync Behavior
- Scans `{base folder}/.roo/` subdirectories ONLY (not entire project folders)
- Uses mtime (modification time) to determine newest file as source
- Root-level files require explicit `root_allowlist` in config.txt
- Atomic copy: temp file + rename (not direct copy)
- Timestamped backups: `filename_YYYYMMDDTHHMMSSZ.bak` format
- Dry-run mode emits EventType.SKIP events without file operations

### Configuration
Settings in `config.txt` (NOT .ini, .json, or .yaml):
- `root_allowlist`: Comma-separated list of root files to sync (e.g., `.roomodes`)
- `backup_mode`: "timestamped" or "none"
- `preserve_mtime`: Must be true to maintain file timestamps

### Database
There is no database for this project. Ignore any references to a database.

### Progress Events
- Thread-safe event queue system for GUI/CLI coordination
- EventType enum in utils_sync/progress_events.py
- Workers use SyncWorker.run() on background threads

### Testing
- Integration tests use `test_integration/` with project_a and project_b folders
- Tests verify .roo sync behavior, not general file sync
- pytest fixtures in tests/ create temporary .roo structures

## Tooling Preference (Web)
Primary: browser_action (ALWAYS try this first).
Fallback: Other browser tools (Only if browser_action fails).
