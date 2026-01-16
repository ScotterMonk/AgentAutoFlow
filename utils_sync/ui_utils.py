# [Modified] by Claude Sonnet 4.5 | 2025-11-13_02
"""
UI utility components for the file sync application.
Provides reusable tkinter widgets and UI helpers.
"""
import tkinter as tk
from tkinter import ttk

from .time_utils import format_duration_hms


class ToolTip:
    """Tiny tooltip helper for Tk widgets.

    Shows a small hover popup near the cursor.
    """

    def __init__(
        self,
        widget: tk.Widget,
        text: str,
        *,
        delay_ms: int = 350,
        pad: tuple[int, int] = (10, 6),
        bg: str = "#1b1b1b",
        fg: str = "#e0e0e0",
        border: str = "#2a2a2a",
    ):
        self.widget = widget
        self.text = text
        self.delay_ms = delay_ms
        self.pad = pad
        self.bg = bg
        self.fg = fg
        self.border = border

        self._after_id: str | None = None
        self._tip: tk.Toplevel | None = None
        self._last_xy: tuple[int, int] | None = None

        widget.bind("<Enter>", self._on_enter, add=True)
        widget.bind("<Leave>", self._on_leave, add=True)
        widget.bind("<Motion>", self._on_motion, add=True)
        widget.bind("<ButtonPress>", self._on_leave, add=True)
        widget.bind("<Destroy>", self._on_destroy, add=True)

    def _on_motion(self, event):
        # Track cursor position so the tooltip can follow/appear near it.
        self._last_xy = (event.x_root, event.y_root)
        if self._tip is not None:
            self._reposition()

    def _on_enter(self, event=None):
        self._schedule()

    def _on_leave(self, event=None):
        self._unschedule()
        self._hide()

    def _on_destroy(self, event=None):
        self._unschedule()
        self._hide()

    def _schedule(self):
        self._unschedule()
        try:
            self._after_id = self.widget.after(self.delay_ms, self._show)
        except Exception:
            self._after_id = None

    def _unschedule(self):
        if not self._after_id:
            return
        try:
            self.widget.after_cancel(self._after_id)
        except Exception:
            pass
        self._after_id = None

    def _show(self):
        self._after_id = None
        if self._tip is not None:
            return

        # Fail-soft if the widget is gone.
        try:
            if not bool(self.widget.winfo_exists()):
                return
        except Exception:
            return

        self._tip = tk.Toplevel(self.widget)
        self._tip.wm_overrideredirect(True)
        self._tip.wm_attributes("-topmost", True)

        outer = tk.Frame(self._tip, bg=self.border, padx=1, pady=1)
        outer.pack(fill=tk.BOTH, expand=True)
        label = tk.Label(
            outer,
            text=self.text,
            bg=self.bg,
            fg=self.fg,
            justify=tk.LEFT,
            relief=tk.FLAT,
            padx=self.pad[0],
            pady=self.pad[1],
            font=("TkDefaultFont", 9),
        )
        label.pack()

        self._reposition()

    def _reposition(self):
        if self._tip is None:
            return
        x, y = self._last_xy or (self.widget.winfo_pointerx(), self.widget.winfo_pointery())
        # Slight offset so we don't sit directly under the cursor.
        x += 12
        y += 16
        try:
            self._tip.geometry(f"+{x}+{y}")
        except Exception:
            pass

    def _hide(self):
        if self._tip is None:
            return
        try:
            self._tip.destroy()
        except Exception:
            pass
        self._tip = None

class FolderItem:
    """A UI component representing a single folder in the folder list."""
    # [Modified] by openai/gpt-5.1 | 2025-11-14_02
    
    # [Created-or-Modified] by gpt-5.2 | 2026-01-01_01
    def __init__(
        self,
        parent,
        folder_path: str,
        remove_callback,
        overwrite_remove_callback=None,
        file_delete_callback=None,
        toggle_favorite_callback=None,
        is_favorite: bool = False,
        project_name_font=None,
        preview_header_font=None,
        preview_row_font=None,
        preview_bak_font=None,
        green_bright="#00ff5f",
        gray_preview="#b0b0b0",
        gray_bak="#9a9a9a",
        fg_primary="#e0e0e0",
    ):
        """Initialize a folder item widget.
        
        Args:
            parent: The parent tkinter widget
            folder_path: The full path to the folder
            remove_callback: Callback function to call when remove button is clicked
            overwrite_remove_callback: Callback when an individual planned overwrite is removed
            file_delete_callback: Callback when file delete button is clicked (receives folder_path, relative_path)
            toggle_favorite_callback: Callback when favorite star is toggled (receives folder_path, is_favorite)
            is_favorite: Whether this folder is currently marked as favorite
            project_name_font: Optional font tuple for the primary folder name label.
            preview_header_font: Optional font tuple for the preview header label.
            preview_row_font: Optional font tuple for preview row labels.
            preview_bak_font: Optional font tuple for .bak row labels.
            green_bright: Color for green status indicators
            gray_preview: Color for preview file list text
            gray_bak: Color for .bak file rows
            fg_primary: Primary foreground color
        """
        # [Created-or-Modified] by gpt-5.2 | 2026-01-07_01
        # Store theme colors locally (avoid relying on module-level constants)
        self._green_bright = green_bright
        self._gray_preview = gray_preview
        self._gray_bak = gray_bak
        self._fg_primary = fg_primary

        # Create main frame for this folder item
        self.frame = ttk.Frame(parent, relief=tk.FLAT, borderwidth=0)
        
        # Create a top row container for the main controls
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill=tk.X)
        
        # Store folder path, callbacks, and favorite state
        self.folder_path = folder_path
        self.overwrite_remove_callback = overwrite_remove_callback
        self.file_delete_callback = file_delete_callback
        self._toggle_favorite_callback = toggle_favorite_callback
        self.is_favorite = is_favorite

        # Fonts are configurable from the main GUI. We store full font tuples here so
        # callers can adjust sizes in one place without creating an import cycle.
        self._project_name_font = project_name_font or ("TkDefaultFont", 10)
        self._preview_header_font = preview_header_font or ("TkDefaultFont", 8, "bold")
        self._preview_row_font = preview_row_font or ("TkDefaultFont", 8)
        self._preview_bak_font = preview_bak_font or ("TkDefaultFont", 8)
        
        # Create favorite toggle button
        # [Created] by openai/gpt-5-mini | 2025-11-15_01
        self.favorite_button = ttk.Button(
            top_frame,
            text="★" if self.is_favorite else "☆",
            width=3,
            command=self._on_favorite_toggle,
            style="AFMini.TButton",
        )
        self.favorite_button.pack(side=tk.LEFT, padx=(5, 2), pady=2)
        
        # Create label showing the folder path
        self.label = ttk.Label(
            top_frame,
            text=folder_path,
            anchor=tk.W,
            font=self._project_name_font,
        )
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(2, 5), pady=2)
        
        # Create progress bar
        # Use the dark-mode progressbar style defined in main_gui so that:
        # - the trough matches the dark background and is effectively invisible at 0%
        # - the progressing bar is a bright neon green that fits the app's theme
        self.progress_bar = ttk.Progressbar(
            top_frame,
            mode="determinate",
            length=100,
            style="AF.Progressbar",
            maximum=100,
        )
        self.progress_bar.pack(side=tk.LEFT, padx=(0, 5), pady=2)
        self.progress_bar["value"] = 0
        
        # Create status label
        self.status_label = ttk.Label(
            top_frame,
            text="",
            anchor=tk.W,
            width=15
        )
        self.status_label.pack(side=tk.LEFT, padx=(0, 5), pady=2)
        
        # Create remove button for the entire folder
        self.remove_button = ttk.Button(
            top_frame,
            text="X",
            width=3,
            command=lambda: remove_callback(folder_path),
            style="AFMini.TButton",
        )
        self.remove_button.pack(side=tk.RIGHT, padx=(0, 5), pady=2)
        ToolTip(self.remove_button, "Do not update this item")
        
        # Container for planned overwrite rows (shown under the main row)
        self.preview_frame = ttk.Frame(self.frame)
        self.preview_frame.pack(fill=tk.X, padx=(20, 5), pady=(0, 2))
        # Header label is created only when we have preview items; keep a stable attribute
        # so later completion updates can safely no-op if the header isn't present.
        self._preview_header_label = None
        # Map relative file paths to the label widgets for their preview rows
        self._preview_rows = {}
        # Track row frames for .bak backup file display so we can clear only those
        self._backup_rows = []
    
    def update_status(self, text: str, color: str = "black"):
        """Update the status label text and color.
        
        Args:
            text: The status text to display
            color: The text color (default: "black")
        """
        # [Created-or-Modified] by openai/gpt-5.1 | 2025-12-04_02
        # Brighten specific colors for dark background while keeping API simple.
        if color == "green":
            fg = self._green_bright
        else:
            fg = color
        self.status_label.config(text=text, foreground=fg)
    
    def update_progress(self, current: int, total: int):
        """Update the progress bar value.
        
        Args:
            current: Current progress value
            total: Total value for completion
        """
        # [Created] by Claude Sonnet 4.5 | 2025-11-13_02
        if total > 0:
            percentage = (current / total) * 100
            self.progress_bar["value"] = percentage
        else:
            self.progress_bar["value"] = 0
    
    # [Created-or-Modified] by gpt-5.2 | 2026-01-01_01
    def update_preview(self, items):
        """Update the planned overwrite preview UI for this folder item.
        
        Each item in `items` should be a dict with:
            - relative: Relative file path within the sync scope
            - timestamp: Human-readable last modified timestamp string
            - action: The underlying planned action object
        """
        # [Created-or-Modified] by gpt-5.2 | 2026-01-07_01
        
        # Clear any existing rows and label mapping
        for child in self.preview_frame.winfo_children():
            child.destroy()
        
        # Reset preview mapping so executed rows can be marked later
        self._preview_rows = {}
        # The header label, if it existed, was destroyed above; clear the cached reference
        # to avoid later TclError when completion tries to reconfigure a stale widget.
        self._preview_header_label = None
        # Backup row frames may also have been destroyed above; clear tracking for consistency.
        self._backup_rows = []
        
        if not items:
            return
        
        # Header row showing planned updates (before execution)
        header_frame = ttk.Frame(self.preview_frame)
        header_frame.pack(fill=tk.X, pady=(0, 1))
        self._preview_header_label = ttk.Label(
            header_frame,
            text="These files will be updated:",
            anchor=tk.W,
            justify=tk.LEFT,
            font=self._preview_header_font,
        )
        self._preview_header_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Sort so that:
        # - Root-level files (no "/") appear first
        # - Then entries are grouped by their first path segment so "rules" comes before "rules-architect"
        # - Within each group, paths are sorted lexicographically, giving patterns like:
        #   "root" → "root/rules" → "root/rules-architect" → "root/rules-ask"
        def _sort_key(item):
            rel = item.get("relative", "") or ""
            rel_str = str(rel)
            
            # Root-level: no "/" in path
            if "/" not in rel_str:
                return (0, rel_str.lower())
            
            # Nested: group by first segment so "rules/..." sorts before "rules-architect/..."
            first_segment = rel_str.split("/", 1)[0]
            return (1, first_segment.lower(), rel_str.lower())
        
        sorted_items = sorted(items, key=_sort_key)
        
        for item in sorted_items:
            row_frame = ttk.Frame(self.preview_frame)
            row_frame.pack(fill=tk.X, pady=(0, 1))
            
            source_project = (item.get("source_project") or "").strip()
            # Use a small Unicode left-arrow glyph instead of ASCII "<--".
            # This keeps the UI compact and consistent with other glyph markers (e.g., "✓").
            newer_suffix = ""
            try:
                action = item.get("action") or {}
                src_mtime = action.get("source_mtime")
                dst_mtime = action.get("destination_mtime")
                if src_mtime is not None and dst_mtime is not None:
                    delta_sec = int(float(src_mtime)) - int(float(dst_mtime))
                    if delta_sec > 0:
                        newer_suffix = f" {format_duration_hms(delta_sec)} newer"
            except Exception:
                newer_suffix = ""

            suffix = f"  ← {source_project}{newer_suffix}" if source_project else ""

            text = f"- {item.get('relative', '')}  {item.get('timestamp', '')}{suffix}"
            label = ttk.Label(
                row_frame,
                text=text,
                anchor=tk.W,
                justify=tk.LEFT,
                font=self._preview_row_font,
                foreground=self._gray_preview,
            )
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # Track label widget by relative path for later updates (e.g., marking as replaced)
            rel_key = str(item.get("relative", "") or "")
            self._preview_rows[rel_key] = label

            # Per-file controls live ONLY on file rows (never on the folder header row):
            # - Skip update: existing black "X" (removes planned overwrite action)
            # - Delete file: new red "X" (deletes only this file in this folder)
            if "action" in item:
                # IMPORTANT (pack order): with pack(side=RIGHT), the first packed widget becomes
                # the right-most. We want the red delete X to appear to the RIGHT of the black
                # skip-update X, with 5px between them.
                if self.file_delete_callback is not None:
                    delete_button = ttk.Button(
                        row_frame,
                        text="X",
                        width=2,
                        command=lambda action=item["action"], fp=self.folder_path: self.file_delete_callback(fp, action),
                        style="AFDangerMini.TButton",
                    )
                    delete_button.pack(side=tk.RIGHT, padx=(5, 0))
                    ToolTip(delete_button, "Delete this file")

                # Per-file black "X" button to remove this planned overwrite from the queue
                if self.overwrite_remove_callback is not None:
                    remove_button = ttk.Button(
                        row_frame,
                        text="X",
                        width=2,
                        command=lambda action=item["action"]: self.overwrite_remove_callback(action),
                        style="AFMini.TButton",
                    )
                    remove_button.pack(side=tk.RIGHT, padx=(5, 0))
                    ToolTip(remove_button, "Do not update this item")
    
    # [Created-or-Modified] by gpt-5.2 | 2026-01-01_01
    def reset_status(self):
        """Reset the status label, progress bar, and preview area to initial states."""
        # [Created-or-Modified] by openai/gpt-5.1 | 2025-12-04_02
        self.status_label.config(text="", foreground=self._fg_primary)
        self.progress_bar["value"] = 0
        for child in self.preview_frame.winfo_children():
            child.destroy()
        # Reset preview label mapping as well
        self._preview_rows = {}
        # Clear header label reference (the widget was destroyed above)
        self._preview_header_label = None
        # Reset backup rows tracking
        self._backup_rows = []
    
    # [Created-or-Modified] by gpt-5.2 | 2026-01-01_01
    def update_preview_header_to_completed(self) -> None:
        """Update the preview header from 'will be' to 'were' after execution completes."""
        # [Created] by Sonnet 4.5 | 2025-12-04_03
        label = getattr(self, "_preview_header_label", None)
        if not label:
            return
        # The python object can outlive the underlying Tk widget if it was destroyed.
        # In that case any tk call (including .config) can raise TclError.
        try:
            if not bool(label.winfo_exists()):
                self._preview_header_label = None
                return
            label.config(text="These files were updated:")
        except tk.TclError:
            # Fail soft; this can happen if the UI was refreshed or folders changed
            # while the background worker is still emitting events.
            self._preview_header_label = None
    
    # [Created-or-Modified] by gpt-5.2 | 2026-01-01_01
    def mark_preview_replaced(self, relative_path: str) -> None:
        """Mark a single preview row as replaced for the given relative path."""
        # [Created-or-Modified] by Sonnet 4.5 | 2025-12-04_03
        if not relative_path:
            return
        key = str(relative_path)
        label = getattr(self, "_preview_rows", {}).get(key)
        if label is None:
            return
        # Prefix with a checkmark once and change color to green to indicate replacement
        try:
            if not bool(label.winfo_exists()):
                return
            current_text = label.cget("text")
            if not current_text.startswith("✓ "):
                # After execution, the "source project" suffix is no longer useful.
                # Strip any trailing "← <project> ..." info before adding the checkmark.
                trimmed = current_text
                try:
                    trimmed = trimmed.split("  ← ", 1)[0]
                except Exception:
                    trimmed = current_text
                label.config(text=f"✓ {trimmed}", foreground=self._green_bright)
        except tk.TclError:
            # Fail soft if the row was destroyed by a rescan/reset while events are processing.
            return
    
    def show_backup_files(self, relative_paths: list[str]) -> None:
        """Append rows for .bak backup files under this folder."""
        # [Created-or-Modified] by gpt-5.2 | 2026-01-07_01
        # First remove any existing backup rows so this call fully refreshes the .bak display
        for row in getattr(self, "_backup_rows", []):
            try:
                row.destroy()
            except Exception:
                # Fail soft; stale widgets should not break the GUI
                pass
        self._backup_rows = []

        if not relative_paths:
            return

        # Keep display ordering stable and case-insensitive
        for rel in sorted(relative_paths, key=lambda p: str(p).lower()):
            row_frame = ttk.Frame(self.preview_frame)
            row_frame.pack(fill=tk.X, pady=(0, 1))

            # Display the relative path only; it already includes the `.bak` extension.
            text = f"  {rel}"
            label = ttk.Label(
                row_frame,
                text=text,
                anchor=tk.W,
                justify=tk.LEFT,
                font=self._preview_bak_font,
                foreground=self._gray_bak,
            )
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            # Track backup rows so they can be cleared independently of main preview rows
            self._backup_rows.append(row_frame)
        # Note: we intentionally do not add these labels to _preview_rows so they
        # are not affected by checkmarks or per-file removal controls.
    
    def _on_favorite_toggle(self):
        """Handle favorite button toggle.
        
        Flips the favorite state, updates the button text, and calls the callback if provided.
        """
        # [Created] by openai/gpt-5-mini | 2025-11-15_01
        self.is_favorite = not self.is_favorite
        self.favorite_button.config(text="★" if self.is_favorite else "☆")
        
        if self._toggle_favorite_callback is not None:
            self._toggle_favorite_callback(self.folder_path, self.is_favorite)
