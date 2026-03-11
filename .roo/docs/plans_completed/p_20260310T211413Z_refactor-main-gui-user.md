# User Query — Refactor `main_gui.py`

**Captured:** 2026-03-10T21:14Z  
**Why:** `main_gui.py` is at 1,525 lines — well over the 550-line app standard. Extracting cohesive subsystems into utility modules reduces cognitive load, improves testability, and brings the file into compliance.

---

## Original Request

Refactor `main_gui.py` from 1,525 lines down to ~850 lines (~675 lines extracted) via 4 targeted extractions:

### Task 1 — Create `utils_sync/ui_styles.py` (~115 lines moved)
Extract the entire TTK style block from `_create_widgets()` (lines 99–218) into a new file.
New API: `apply_dark_theme(style: ttk.Style, config: dict) -> None`
`_create_widgets` calls `ui_styles.apply_dark_theme(style, self.config)` in place of those 120 lines.

### Task 2 — Create `utils_sync/settings_window.py` (~185 lines moved)
Extract `_open_settings_window()` (line 1083) and `_save_settings()` (line 1237) entirely.
New API: `open_settings_window(root, config, on_saved) -> None`
`main_gui.py` retains a thin 10-line `_open_settings_window` and a new `_on_settings_saved(updated_config)` (~8 lines).

### Task 3 — Create `utils_sync/file_delete_utils.py` (~175 lines moved)
Extract the file I/O core from `_delete_file_from_preview_row()` (line 480) and `_delete_file_and_folder_from_preview_row()` (line 581).
New APIs: `delete_file_across_folders(...)` and `delete_file_and_folder_across_folders(...)`.
Each method in `main_gui.py` shrinks to ~15 lines: validate, call util, show messagebox, call `self._rescan()`.

### Task 4 — Merge `_rescan_after_delete` + `_rescan_after_bak_delete` (~25 lines saved)
`_rescan_after_delete()` (line 713) and `_rescan_after_bak_delete()` (line 1461) are nearly identical.
Replace both with: `_rescan(self, *, refresh_bak: bool = True) -> None`

## Implementation Order
1. Task 1 (styles) — lowest risk, pure config data
2. Task 3 (file delete utils) — pure I/O, easy to unit test
3. Task 4 (merge rescans) — trivial, do alongside Task 3
4. Task 2 (settings window) — most complex, do last

## Files Affected
- `main_gui.py`: shrinks 1,525 → ~850 lines
- `utils_sync/ui_styles.py`: NEW (~125 lines)
- `utils_sync/settings_window.py`: NEW (~200 lines)
- `utils_sync/file_delete_utils.py`: NEW (~120 lines)
- `utils_sync/ui_utils.py`: no change
