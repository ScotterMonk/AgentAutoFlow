# Plan: Refactor `main_gui.py` → ~850 Lines

**Short plan name:** `refactor-main-gui`  
**Plan file:** `p_20260310T211413Z_refactor-main-gui.md`  
**Log file:** `p_20260310T211413Z_refactor-main-gui-log.md`  
**User query file:** `p_20260310T211413Z_refactor-main-gui-user.md`  
**Complexity:** One Phase (Small/Med)  
**Autonomy level:** High (rare checks)  
**Testing type:** Use what is appropriate per task  

---

## Problem / Solution Summary

`main_gui.py` is 1,525 lines — nearly 3× the 550-line app standard. Four cohesive subsystems (TTK styles, settings dialog, file-delete I/O, rescan logic) are inlined inside `MainApp`. Extracting them to dedicated utility modules brings the file toward ~850 lines, improves testability, and enforces the app's modularization standard.

---

## Phase 1 — Extract & Clean `main_gui.py`

**Implementation order (lowest-to-highest risk):**
1. Task 1 — styles (pure config data, zero coupling to `MainApp`)
2. Task 3 — file delete utils (pure I/O, no Tkinter)
3. Task 4 — merge rescan methods (trivial, alongside Task 3)
4. Task 2 — settings window (most complex, do last)

---

### Task 01 — Backup `main_gui.py`

**Goal:** Safe backup before any edits.
- Task 01: Backup `main_gui.py` to the backups folder.
    Mode hint: /coder-jr
    Actions:
      - Copy `main_gui.py` to `.roo/docs/old_versions/main_gui_[timestamp].py`.
    Testing: None
    **Log progress** to `p_20260310T211413Z_refactor-main-gui-log.md`.

---

### Task 02 — Create `utils_sync/ui_styles.py`

**Goal:** Extract the entire TTK style block (lines 99–218) from `_create_widgets()` into a standalone module with zero coupling to `MainApp`.
- Task 02: Create new file `utils_sync/ui_styles.py` with `apply_dark_theme()`.
    Mode hint: /coder-jr
    Actions:
      - Create `utils_sync/ui_styles.py`.
      - Add module docstring: "TTK dark-theme style configuration for AgentAutoFlow."
      - Import: `import tkinter as tk` and `from tkinter import ttk`.
      - Implement:
        ```python
        def apply_dark_theme(style: ttk.Style, config: dict) -> None:
            """Configure all AF.* TTK styles for the dark theme.
            
            Args:
                style: The ttk.Style instance to configure.
                config: The application config dict for color/font keys.
            """
        ```
      - Move lines 100–218 verbatim into the function body (start at `try: style.theme_use("clam")` — do NOT copy line 99 `style = ttk.Style()` since `style` is already the function parameter).
      - The first line of the function body is the `try/except tk.TclError` block for `theme_use("clam")`.
      - Do NOT reference `self` or `MainApp` anywhere.
    Testing: Terminal — run `python -c "import utils_sync.ui_styles; print('OK')"` to confirm importable.
    **Log progress** to `p_20260310T211413Z_refactor-main-gui-log.md`.

---

### Task 03 — Update `main_gui.py` for Task 02 (styles)

**Goal:** Replace the 120-line style block in `_create_widgets()` with a single call to `ui_styles.apply_dark_theme()`.
- Task 03: Edit `main_gui.py` to call `ui_styles.apply_dark_theme()`.
    Mode hint: /coder-jr
    Actions:
      - Add import at top of file (line ~13 with other utils_sync imports):
        `from utils_sync import ui_styles`
      - In `_create_widgets()` (line 94), replace lines 99–221 (the style block ending just before `# Main frame with padding`) with:
        ```python
        # Apply dark theme to all TTK widgets
        style = ttk.Style()
        ui_styles.apply_dark_theme(style, self.config)
        ```
      - Keep line 221: `self.root.configure(bg=self.config["ui_dark_bg"])` (this line stays in `_create_widgets`).
      - Verify `_create_widgets` now starts at the style call then immediately continues to the main frame setup.
    Testing: Terminal — run `python -c "import main_gui; print('OK')"` to confirm no import errors.
    **Log progress** to `p_20260310T211413Z_refactor-main-gui-log.md`.

---

### Task 04 — Create `utils_sync/file_delete_utils.py`

**Goal:** Extract pure file-I/O logic from both delete methods into a Tkinter-free utility module.
- Task 04: Create new file `utils_sync/file_delete_utils.py` with two public functions.
    Mode hint: /coder-sr
    Actions:
      - Create `utils_sync/file_delete_utils.py`.
      - Add module docstring: "File deletion utilities for synced .roo folders (no Tkinter dependency)."
      - Imports: `from pathlib import Path`, `import shutil`.
      - Implement `delete_file_across_folders`:
        ```python
        def delete_file_across_folders(
            relative_path: str,
            action: dict,
            favorite_folders: list[str],
        ) -> tuple[int, list[str]]:
            """Delete a .roo-relative file from every favorite folder plus source/dest.

            Args:
                relative_path: Path relative to the .roo/ subdirectory.
                action: Sync action dict with optional 'source_path' and 'destination_path'.
                favorite_folders: List of absolute folder paths to search.

            Returns:
                (deleted_count, errors): count of files deleted and list of error strings.
            """
        ```
        - Move the loop body + source/dest deletion logic verbatim from `_delete_file_from_preview_row()` (lines 516–561).
        - Remove all `print("DEBUG: ...")` calls — pure I/O only.
        - Return `(deleted_count, errors)`.
      - Implement `delete_file_and_folder_across_folders`:
        ```python
        def delete_file_and_folder_across_folders(
            relative_path: str,
            action: dict,
            favorite_folders: list[str],
        ) -> tuple[int, int, list[str]]:
            """Delete a .roo-relative file AND its parent folder from every favorite folder.

            Returns:
                (deleted_files, deleted_folders, errors).
            """
        ```
        - Move the loop body + nested `_delete_file_and_parent` helper verbatim from `_delete_file_and_folder_from_preview_row()` (lines 615–706).
        - Remove all `print("DEBUG: ...")` calls.
        - Return `(deleted_files, deleted_folders, errors)`.
      - No references to `self`, `MainApp`, or any Tkinter symbol.
    Testing: Python — add `tests/test_file_delete_utils.py` with at least 2 pytest cases: (a) deletes file from a temp `.roo/` dir and returns correct count, (b) returns error string when file is a directory. Run `pytest tests/test_file_delete_utils.py -v`.
    **Log progress** to `p_20260310T211413Z_refactor-main-gui-log.md`.

---

### Task 05 — Update `main_gui.py` for Task 04 (delete utils) + Task 04 (merge rescan)

**Goal:** Slim both delete methods to ~15 lines each, add import, and replace the two near-identical `_rescan_after_*` methods with a single `_rescan()`.
- Task 05: Edit `main_gui.py` — slim delete methods, add `_rescan()`, remove old rescan methods.
    Mode hint: /coder-sr
    Actions:
      - Add import (line ~13): `from utils_sync import file_delete_utils`
      - **Rewrite `_delete_file_from_preview_row()`** (line 480):
        - Keep guard checks (lines 492–505).
        - Replace the I/O block (lines 513–575) with:
          ```python
          deleted_count, errors = file_delete_utils.delete_file_across_folders(
              relative_path, action, self.favorite_folders
          )
          if errors:
              messagebox.showerror(
                  "Delete Files - Partial Failure",
                  f"Deleted {deleted_count} file(s) with errors:\n\n" + "\n\n".join(errors[:3])
              )
          elif deleted_count == 0:
              messagebox.showinfo("No Files Deleted", "No files were found to delete.")
          self._rescan()
          ```
      - **Rewrite `_delete_file_and_folder_from_preview_row()`** (line 581):
        - Keep guard checks.
        - Replace I/O block with:
          ```python
          deleted_files, deleted_folders, errors = file_delete_utils.delete_file_and_folder_across_folders(
              relative_path, action, self.favorite_folders
          )
          if errors:
              messagebox.showerror(
                  "Delete Files - Partial Failure",
                  f"Deleted {deleted_files} file(s) and {deleted_folders} folder(s) with errors:\n\n"
                  + "\n\n".join(errors[:3])
              )
          elif deleted_files == 0 and deleted_folders == 0:
              messagebox.showinfo("Nothing Deleted", "No files or folders were found to delete.")
          self._rescan()
          ```
      - **Add new `_rescan()` method** (insert after the rewritten delete methods, before `_format_mtime`):
        ```python
        def _rescan(self, *, refresh_bak: bool = True) -> None:
            """Re-scan folders and rebuild previews. Called after any delete operation.
            
            Args:
                refresh_bak: If True (default), also refreshes the .bak backup preview panel.
            """
            if self.is_syncing:
                return
            if len(self.selected_folders) < 2:
                return
            try:
                folder_paths = [Path(p) for p in self.selected_folders]
                file_index = self.sync_engine.scan_folders(folder_paths)
                actions = self.sync_engine.plan_actions(file_index, scanned_folders=folder_paths)
            except Exception as exc:
                print(f"Rescan failed: {exc}")
                return
            self.planned_actions = actions
            self._update_overwrite_previews()
            if refresh_bak:
                self._update_bak_previews()
            # Clear stale queued scan events
            while not self.event_queue.empty():
                try:
                    self.event_queue.get_nowait()
                except queue.Empty:
                    break
        ```
      - **Search all call sites** for `_rescan_after_delete` and `_rescan_after_bak_delete` in `main_gui.py` before removing them. Update any call sites found to use `_rescan()` (with `refresh_bak=False` for the bak-delete path if needed).
      - **Delete** `_rescan_after_delete()` (line 713) and `_rescan_after_bak_delete()` (line 1461).
    Testing: Terminal — run `python -c "import main_gui; print('OK')"`. Run `pytest tests/ -v`.
    **Log progress** to `p_20260310T211413Z_refactor-main-gui-log.md`.

---

### Task 06 — Create `utils_sync/settings_window.py`

**Goal:** Extract the modal settings dialog into a standalone module. Zero `MainApp` coupling; communicates results via `on_saved` callback.
- Task 06: Create new file `utils_sync/settings_window.py`.
    Mode hint: /coder-sr
    Actions:
      - Create `utils_sync/settings_window.py`.
      - Add module docstring: "Modal settings dialog for AgentAutoFlow sync configuration."
      - Imports: `import tkinter as tk`, `from tkinter import ttk, messagebox`, `from utils_sync import config_sync, file_path_utils`.
      - Implement:
        ```python
        def open_settings_window(
            root: tk.Tk,
            config: dict,
            on_saved: callable,
        ) -> None:
            """Build and show the modal settings dialog.

            Args:
                root: The parent Tk window (for centering and transient binding).
                config: Current application config dict (read-only reference for defaults).
                on_saved: Callback receiving the updated config dict after Save is confirmed.
                          Signature: on_saved(updated_config: dict) -> None
            """
        ```
      - Move the entire body of `_open_settings_window()` (lines 1088–1235) into this function, replacing all `self.config` references with `config`, and `self.root` with `root`.
      - The Save button lambda must call an internal `_save(...)` function (not `self._save_settings`). Move the entire body of `_save_settings()` (lines 1258–1305) into a nested `_save(...)` closure inside `open_settings_window`. At the end of `_save`, instead of calling `self._update_dry_run_status()` and `self._update_ignore_patterns_display()`, call `on_saved(updated_config)` passing the mutated config dict.
      - Remove the `window.destroy()` call from the save path — this is now handled by returning via `on_saved`.
        **Correction**: Keep `window.destroy()` in `_save` (it must still close the dialog); call `on_saved(updated_config)` after.
      - No references to `self` or `MainApp`.
    Testing: Terminal — run `python -c "import utils_sync.settings_window; print('OK')"`.
    **Log progress** to `p_20260310T211413Z_refactor-main-gui-log.md`.

---

### Task 07 — Update `main_gui.py` for Task 06 (settings window)

**Goal:** Replace the two large settings methods with a thin dispatcher and a new `_on_settings_saved` callback method.
- Task 07: Edit `main_gui.py` — slim settings methods, wire callback, add import.
    Mode hint: /coder-jr
    Actions:
      - Add import (line ~13): `from utils_sync import settings_window`
      - **Replace `_open_settings_window()`** (line 1083) with:
        ```python
        def _open_settings_window(self) -> None:
            """Open the settings configuration window."""
            settings_window.open_settings_window(
                self.root, self.config, self._on_settings_saved
            )
        ```
      - **Delete `_save_settings()`** (lines 1237–1305) entirely.
      - **Add new method `_on_settings_saved()`** immediately after `_open_settings_window`:
        ```python
        def _on_settings_saved(self, updated_config: dict) -> None:
            """Receive updated config from the settings dialog and sync app state.
            
            Args:
                updated_config: The mutated config dict returned from the settings dialog.
            """
            self.config = updated_config
            self.favorite_folders = list(updated_config.get("folders_faves", []))
            self._update_dry_run_status()
            self._update_ignore_patterns_display()
        ```
    Testing: Terminal — run `python -c "import main_gui; print('OK')"`. Run `pytest tests/ -v`.
    **Log progress** to `p_20260310T211413Z_refactor-main-gui-log.md`.

---

### Task 08 — Verify Final Line Count & Full Test Run

**Goal:** Confirm refactoring is complete, line count is at target, no regressions.
- Task 08: Count lines, run all tests, do a final import smoke-test.
    Mode hint: /coder-jr
    Actions:
      - Run: `(Get-Content main_gui.py).Count` — confirm result is ≤ 900 lines.
      - Run: `python -c "import main_gui; import utils_sync.ui_styles; import utils_sync.settings_window; import utils_sync.file_delete_utils; print('All imports OK')"`.
      - Run: `pytest tests/ -v` — all tests must pass, no new failures.
      - If line count > 900, scan for dead code, orphaned comments, or missed Debug `print()` calls and remove them.
      - Verify `utils_sync/__init__.py` does not need updating (new modules are imported directly, not re-exported).
    Testing: Python — `pytest tests/ -v`. Terminal — line count check.
    **Log progress** to `p_20260310T211413Z_refactor-main-gui-log.md`.

---

## Projected Line Counts (reference)

| Action | Lines removed from `main_gui.py` |
|---|---|
| Task 1: `ui_styles.py` | ~115 |
| Task 2: `settings_window.py` | ~185 |
| Task 3: `file_delete_utils.py` | ~175 |
| Task 4: Merge rescan methods | ~25 |
| Subtotal | ~500 |
| Buffer (debug prints, dead code) | ~175 |
| **Estimated final** | **~850** |

---

## Files Affected

| File | Change |
|---|---|
| [`main_gui.py`](../../main_gui.py) | Shrinks 1,525 → ~850 lines |
| [`utils_sync/ui_styles.py`](../../utils_sync/ui_styles.py) | **New** (~125 lines) |
| [`utils_sync/settings_window.py`](../../utils_sync/settings_window.py) | **New** (~200 lines) |
| [`utils_sync/file_delete_utils.py`](../../utils_sync/file_delete_utils.py) | **New** (~120 lines) |
| [`tests/test_file_delete_utils.py`](../../tests/test_file_delete_utils.py) | **New** (pytest cases) |
| [`utils_sync/ui_utils.py`](../../utils_sync/ui_utils.py) | No change |
