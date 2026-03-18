"""
AgentAutoFlow File Sync - Main GUI Application
Provides a Tkinter-based interface for managing file synchronization.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import queue
from pathlib import Path
import datetime
from utils_sync import config_sync, file_path_utils
from utils_sync import ui_styles
from utils_sync import file_delete_utils
from utils_sync import settings_window
from utils_sync.sync_core import SyncEngine
from utils_sync.sync_worker import SyncWorker
from utils_sync.progress_events import EventType
from utils_sync.ui_utils import FolderItem

class MainApp:
    """Main application window for AgentAutoFlow File Sync."""
    def __init__(self, root: tk.Tk):
        """Initialize the main application window.
        Args:
            root: The root Tkinter window
        """
        self.root = root
        # Load configuration
        self.config = config_sync.load_config()
        # Initialize favorite folders from config, normalizing paths
        raw_faves = self.config.get("folders_faves", [])
        self.favorite_folders = [
            file_path_utils.normalize_path(p) for p in raw_faves
        ]
        # Set up main window
        self.root.title("AgentAutoFlow File Sync")
        window_width = self.config["window_width"]
        window_height = self.config["window_height"]
        # Calculate centered position on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2
        # Set geometry with centered position
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        # Apply base dark background to root window
        self.root.configure(bg=self.config["ui_dark_bg"])
        # Create event queue for progress updates
        self.event_queue = queue.Queue()
        # Initialize sync engine
        self.sync_engine = SyncEngine(self.config, self.event_queue)
        # Initialize selected folders list
        self.selected_folders = []
        # Initialize sync state
        self.is_syncing = False
        # Initialize folder widgets dictionary
        self.folder_widgets = {}
        # Store button references
        self.browse_button = None
        self.sync_button = None
        self.confirm_button = None
        self.load_favorites_button = None
        # Store status label references
        self.dry_run_label = None
        self.ignore_patterns_label = None
        # Store planned actions for two-stage sync (preview then execute)
        self.planned_actions = []
        # Create UI widgets
        self._create_widgets()
        # Update status displays
        self._update_dry_run_status()
        self._update_ignore_patterns_display()
        # Start periodic event processing
        self._process_events()

    def _create_widgets(self):
        """Create and layout all UI widgets."""
        # Configure a basic dark theme for ttk widgets
        # Apply dark theme to all TTK widgets
        style = ttk.Style()
        ui_styles.apply_dark_theme(style, self.config)
        # Ensure the root window background matches the dark theme
        self.root.configure(bg=self.config["ui_dark_bg"])
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="3")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        # Title label
        title_label = ttk.Label(
            main_frame,
            text="AgentAutoFlow File Sync",
            font=("TkDefaultFont", self.config["ui_font_size_title"], "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 2), sticky=tk.W)
        # Description label
        desc_label = ttk.Label(
            main_frame,
            text="Synchronize files across multiple folders with intelligent conflict resolution."
        )
        desc_label.grid(row=1, column=0, pady=(0, 0), sticky=tk.W)
        # Dry run status label
        self.dry_run_label = ttk.Label(main_frame, text="")
        self.dry_run_label.grid(row=2, column=0, pady=(0, 0), sticky=tk.W)
        # Ignore patterns label
        # Folder list frame
        folder_frame = tk.Frame(
            main_frame,
            relief=tk.SOLID,
            borderwidth=1,
            bg=self.config["ui_dark_bg"],
        )
        folder_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(1, 7))
        folder_frame.columnconfigure(0, weight=1)
        folder_frame.rowconfigure(0, weight=1)
        # Create scrollable canvas + frame for folder list
        self.folder_canvas = tk.Canvas(
            folder_frame,
            borderwidth=1,
            highlightthickness=0,
            bg=self.config["ui_dark_bg"],
        )
        self.folder_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        folder_scrollbar = ttk.Scrollbar(
            folder_frame,
            orient=tk.VERTICAL,
            command=self.folder_canvas.yview
        )
        folder_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.folder_canvas.configure(yscrollcommand=folder_scrollbar.set)
        # Inner frame that holds the per-folder widgets
        self.folder_list_frame = ttk.Frame(self.folder_canvas)
        self.folder_canvas.create_window((0, 0), window=self.folder_list_frame, anchor="nw")
        # Update scroll region whenever the inner frame size changes
        self.folder_list_frame.bind(
            "<Configure>",
            lambda e: self.folder_canvas.configure(scrollregion=self.folder_canvas.bbox("all"))
        )
        # Enable mouse wheel scrolling anywhere in the main window
        # Bind at the application level so scroll works even when child widgets have focus
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        # Bottom button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        # Browse button
        self.browse_button = ttk.Button(
            button_frame,
            text="Browse...",
            command=self._open_folder_dialog,
            style="AF.TButton",
        )
        self.browse_button.grid(row=0, column=0, padx=(0, 5))
        # Scan button (first stage: plan/preview, was "Preview")
        self.sync_button = ttk.Button(
            button_frame,
            text="Scan",
            command=self._start_sync,
            style="AF.TButton",
        )
        self.sync_button.grid(row=0, column=1, padx=(0, 5))
        # Execute button (second stage: execute planned actions, was "Confirm")
        self.confirm_button = ttk.Button(
            button_frame,
            text="Execute",
            state=tk.DISABLED,
            command=self._confirm_sync,
            style="AF.TButton",
        )
        self.confirm_button.grid(row=0, column=2, padx=(0, 5))
        # Load Favorites button
        self.load_favorites_button = ttk.Button(
            button_frame,
            text="Load Favorites",
            command=self._load_favorite_folders,
            style="AF.TButton",
        )
        self.load_favorites_button.grid(row=0, column=3, padx=(0, 5))
        # Save Favorites button
        self.save_favorites_button = ttk.Button(
            button_frame,
            text="Save Favorites",
            command=self._save_current_selection_as_favorites,
            style="AF.TButton",
        )
        self.save_favorites_button.grid(row=0, column=4, padx=(0, 5))
        # Delete .bak files button (disabled until at least one folder is selected)
        self.delete_bak_button = ttk.Button(
            button_frame,
            text="Delete .bak files",
            command=self._delete_bak_files,
            state=tk.DISABLED,
            style="AFDanger.TButton",
        )
        self.delete_bak_button.grid(row=0, column=5, padx=(0, 5))
        # Settings button
        self.settings_button = ttk.Button(
            button_frame,
            text="Settings",
            command=self._open_settings_window,
            style="AF.TButton",
        )
        self.settings_button.grid(row=0, column=6)

    def _open_folder_dialog(self):
        """Open folder selection dialog and add valid folder to list."""
        # Open folder selection dialog
        folder_path = filedialog.askdirectory(title="Select folder to sync")
        if folder_path:
            # Normalize the path
            normalized_path = file_path_utils.normalize_path(folder_path)
            # Validate folder has scaffold directory
            scaffold_folder = self.config.get("scaffold_folder", ".kilocode")
            if not file_path_utils.has_scaffold_dir(normalized_path, scaffold_folder):
                print(f"Error: Folder does not contain a {scaffold_folder} subdirectory: {normalized_path}")
                return
            # Check if folder is already in the list
            if normalized_path in self.selected_folders:
                print(f"Folder already selected: {normalized_path}")
                return
            # Add to selected folders and update UI
            self.selected_folders.append(normalized_path)
            self._update_folder_list_ui()

    def _remove_folder(self, folder_to_remove: str):
        """Remove a folder from the selected folders list.
        Args:
            folder_to_remove: The folder path to remove
        """
        if folder_to_remove in self.selected_folders:
            self.selected_folders.remove(folder_to_remove)
            self._update_folder_list_ui()

    def _reset_loaded_folder_state(self) -> None:
        """Reset folder selection UI/state so a new load starts from a clean slate."""
        self.selected_folders = []
        self.planned_actions = []
        self.is_syncing = False
        # Rebuild the folder list immediately so previous previews, statuses,
        # and backup rows disappear before new favorites are added.
        self._update_folder_list_ui()
        if self.confirm_button:
            self.confirm_button.config(state=tk.DISABLED)
        if getattr(self, "delete_bak_button", None) is not None:
            self.delete_bak_button.config(state=tk.DISABLED)
        if self.sync_button:
            self.sync_button.config(state=tk.NORMAL)
        if self.browse_button:
            self.browse_button.config(state=tk.NORMAL)
        # Clear any stale worker/scan events so they cannot repaint old status
        # text after the UI has been reset for a fresh cycle.
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except queue.Empty:
                break

    def _update_folder_list_ui(self):
        """Update the folder list UI to reflect current selected folders."""
        # Destroy all existing widgets in the folder list frame
        for widget in self.folder_list_frame.winfo_children():
            widget.destroy()
        # Clear folder widgets dictionary
        self.folder_widgets = {}
        # Create a FolderItem for each selected folder
        for folder_path in self.selected_folders:
            # Determine initial favorite state, normalizing paths when possible
            try:
                normalized_path = file_path_utils.normalize_path(folder_path)
                is_fav = normalized_path in self.favorite_folders
            except Exception as exc:
                # Fail soft if normalization fails; fall back to raw path membership
                print(
                    f"Error normalizing selected folder path {folder_path!r} "
                    f"for favorites: {exc}"
                )
                is_fav = folder_path in self.favorite_folders
            folder_item = FolderItem(
                self.folder_list_frame,
                folder_path,
                self._remove_folder,
                self._remove_planned_action,
                file_delete_callback=self._delete_file_from_preview_row,
                file_and_folder_delete_callback=self._delete_file_and_folder_from_preview_row,
                toggle_favorite_callback=lambda p, fav, fp=folder_path: self._set_folder_favorite(fp, fav),
                is_favorite=is_fav,
                project_name_font=("TkDefaultFont", self.config["ui_font_size_project"]),
                preview_header_font=("TkDefaultFont", self.config["ui_font_size_folder_preview_header"], "bold"),
                preview_row_font=("TkDefaultFont", self.config["ui_font_size_folder_preview_row"]),
                preview_bak_font=("TkDefaultFont", self.config["ui_font_size_folder_preview_row"]),
            )
            folder_item.frame.pack(fill=tk.X, padx=2, pady=2)
            # Store widget reference in dictionary
            self.folder_widgets[folder_path] = folder_item

    def _delete_file_from_preview_row(self, folder_path: str, action: dict) -> None:
        """Delete this file in ALL favorite folders plus source and destination.
        Critical behavior:
        - Deletes the file (by relative path) in EVERY folder in favorite_folders
        - Also deletes source and destination from the action
        - Checks for existence before deleting each
        - Never deletes folders
        - Fail-safe: continues even if files don't exist
        After deletion, triggers a rescan to refresh the UI.
        """
        if not folder_path:
            return
        if not isinstance(action, dict):
            return
        source_path = action.get("source_path")
        dest_path = action.get("destination_path")
        relative_path = action.get("relative_path", "")
        if not relative_path:
            return
        deleted_count, errors = file_delete_utils.delete_file_across_folders(
            relative_path, action, self.favorite_folders,
            scaffold_folder=self.config.get("scaffold_folder", ".kilocode")
        )
        if errors:
            messagebox.showerror(
                "Delete Files - Partial Failure",
                f"Deleted {deleted_count} file(s) with errors:\n\n" + "\n\n".join(errors[:3])
            )
        elif deleted_count == 0:
            messagebox.showinfo("No Files Deleted", "No files were found to delete.")
        self._rescan()

    def _delete_file_and_folder_from_preview_row(self, folder_path: str, action: dict) -> None:
        """Delete the file in ALL favorite folders AND delete its containing folder.
        Behavior:
        - Deletes the file (by relative path) in EVERY folder in favorite_folders
        - Also deletes source and destination from the action
        - After deleting each file, removes its immediate parent directory (within scaffold dir)
        using shutil.rmtree — skips if parent is the scaffold root itself
        - Fail-safe: continues even if files/folders don't exist
        After deletion, triggers a rescan to refresh the UI.
        """
        if not folder_path:
            return
        if not isinstance(action, dict):
            return
        source_path = action.get("source_path")
        dest_path = action.get("destination_path")
        relative_path = action.get("relative_path", "")
        if not relative_path:
            return
        deleted_files, deleted_folders, errors = file_delete_utils.delete_file_and_folder_across_folders(
            relative_path, action, self.favorite_folders,
            scaffold_folder=self.config.get("scaffold_folder", ".kilocode")
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

    def _format_mtime(self, mtime: float) -> str:
        """Format a POSIX mtime value for display in the preview."""
        try:
            dt = datetime.datetime.fromtimestamp(mtime)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            return ""

    def _update_overwrite_previews(self) -> None:
        """Rebuild per-folder overwrite previews from the current planned actions."""
        # Build per-folder list of planned overwrites, including timestamps and action refs
        overwrites_by_folder = {folder: [] for folder in self.selected_folders}
        for action in self.planned_actions:
            dest_path = action.get("destination_path")
            source_path = action.get("source_path")
            relative = str(action.get("relative_path", ""))
            dest_mtime = action.get("destination_mtime")
            # Pre-format timestamp once for display; use destination mtime snapshot from scan
            timestamp = self._format_mtime(dest_mtime) if dest_mtime is not None else ""
            if dest_path is None:
                continue
            # Compute a human-friendly source project/folder name so the GUI can show
            # which project will act as the overwrite source.
            source_project = ""
            try:
                if source_path is not None:
                    sp = Path(source_path)
                    for base in self.selected_folders:
                        base_path = Path(base)
                        try:
                            sp.relative_to(base_path)
                            source_project = file_path_utils.get_project_folder_name(base_path)
                            break
                        except ValueError:
                            continue
            except Exception:
                # Fail soft: source label is optional UI sugar; never break preview.
                source_project = ""
            for base in self.selected_folders:
                base_path = Path(base)
                try:
                    dest_path.relative_to(base_path)
                    overwrites_by_folder[base].append(
                        {
                            "relative": relative,
                            "timestamp": timestamp,
                            "source_project": source_project,
                            "action": action,
                        }
                    )
                    break
                except ValueError:
                    continue
        any_actions = False
        for folder_path, widget in self.folder_widgets.items():
            items = overwrites_by_folder.get(folder_path, [])
            # Update per-folder preview under the folder name
            if hasattr(widget, "update_preview"):
                widget.update_preview(items)
            # Track whether any actions are planned for enabling the Execute button
            if items:
                any_actions = True
            # Show a clear post-scan status for all folders
            widget.update_status("Scanned", "green")
        # Enable or disable Execute based on whether any actions remain
        if any_actions:
            if self.confirm_button:
                self.confirm_button.config(state=tk.NORMAL)
        else:
            if self.confirm_button:
                self.confirm_button.config(state=tk.DISABLED)

    def _update_bak_previews(self) -> None:
        """Refresh .bak backup file rows under each selected folder preview."""
        if not self.selected_folders or not self.folder_widgets:
            # No folders or widgets – ensure Delete .bak button is disabled.
            if getattr(self, "delete_bak_button", None) is not None:
                self.delete_bak_button.config(state=tk.DISABLED)
            return
        any_bak = False
        for folder_path, widget in self.folder_widgets.items():
            base_path = Path(folder_path)
            if not base_path.exists():
                # Folder no longer exists; clear any existing backup rows
                if hasattr(widget, "show_backup_files"):
                    widget.show_backup_files([])
                continue
            bak_relatives: list[str] = []
            try:
                for bak in base_path.rglob("*.bak"):
                    try:
                        rel = bak.relative_to(base_path)
                    except ValueError:
                        # Should not happen for descendants, but fail soft
                        continue
                    bak_relatives.append(str(rel))
            except OSError as exc:
                # Fail soft; log error and clear backups for this folder
                print(f"Error scanning for .bak files under {base_path!s}: {exc}")
                if hasattr(widget, "show_backup_files"):
                    widget.show_backup_files([])
                continue
            if bak_relatives:
                any_bak = True
            # Delegate to the folder widget to render (or clear) backup rows.
            # Passing an empty list will remove any previously displayed .bak rows.
            if hasattr(widget, "show_backup_files"):
                widget.show_backup_files(bak_relatives)
        # Enable Delete .bak files button only when at least one backup row is visible;
        # otherwise keep it disabled and its text grayed out.
        if getattr(self, "delete_bak_button", None) is not None:
            if any_bak:
                self.delete_bak_button.config(state=tk.NORMAL)
            else:
                self.delete_bak_button.config(state=tk.DISABLED)
        # Force geometry + scrollregion recalculation so the canvas collapses whitespace
        # after backup rows are removed (e.g., via "Delete .bak files").
        try:
            self.folder_list_frame.update_idletasks()
            self.folder_canvas.configure(scrollregion=self.folder_canvas.bbox("all"))
        except Exception:
            # Fail soft; UI refresh should never crash the app.
            pass

    def _remove_planned_action(self, action_to_remove: dict) -> None:
        """Remove a single planned action from the queue and refresh previews."""
        if not self.planned_actions:
            return
        # Remove by identity; callbacks receive the original action dict instance
        self.planned_actions = [
            a for a in self.planned_actions
            if a is not action_to_remove
        ]
        # Rebuild previews and update Execute button state
        self._update_overwrite_previews()

    def _start_sync(self):
        """Run planning phase and show per-folder preview before actual sync."""
        # Check if already syncing
        if self.is_syncing:
            return
        # Check if at least 2 folders are selected
        if len(self.selected_folders) < 2:
            messagebox.showerror(
                "Insufficient Folders",
                "Please select at least 2 folders to sync."
            )
            return
        # Set syncing state for planning phase
        self.is_syncing = True
        # Disable buttons during planning
        self.sync_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)
        if self.confirm_button:
            self.confirm_button.config(state=tk.DISABLED)
        # Reset status of all folder widgets and show planning state
        for widget in self.folder_widgets.values():
            widget.reset_status()
            widget.update_status("Planning...", "blue")
        try:
            # Run scan and plan synchronously to compute actions
            folder_paths = [Path(p) for p in self.selected_folders]
            file_index = self.sync_engine.scan_folders(folder_paths)
            actions = self.sync_engine.plan_actions(file_index, scanned_folders=folder_paths)
        except Exception as e:
            messagebox.showerror(
                "Preview Failed",
                f"Error while planning sync:\n{e}"
            )
            self.is_syncing = False
            self.sync_button.config(state=tk.NORMAL)
            self.browse_button.config(state=tk.NORMAL)
            return
        # Store planned actions for confirmation stage
        self.planned_actions = actions
        # Re-enable buttons after planning
        self.is_syncing = False
        self.browse_button.config(state=tk.NORMAL)
        self.sync_button.config(state=tk.NORMAL)
        # Build per-folder preview list of files that will be overwritten
        # including last-modified timestamps and per-file removal "X" controls.
        self._update_overwrite_previews()
        # Also refresh .bak previews and enable/disable the Delete .bak files button
        # based on whether any backups are present, even if there are zero planned actions.
        self._update_bak_previews()
        # Clear any queued scan events so they don't overwrite the preview status
        while not self.event_queue.empty():
            try:
                self.event_queue.get_nowait()
            except queue.Empty:
                break

    def _confirm_sync(self):
        """Execute the planned sync actions after user confirmation."""
        # Do not start if already syncing
        if self.is_syncing:
            return
        # Ensure we have planned actions
        if not self.planned_actions:
            messagebox.showinfo(
                "Nothing to Sync",
                "There are no planned actions to execute. Run Preview first."
            )
            return
        # Execute immediately without an extra confirmation dialog; UI already shows planned actions.
        # Set syncing state
        self.is_syncing = True
        # Disable buttons during execution
        self.sync_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)
        if self.confirm_button:
            self.confirm_button.config(state=tk.DISABLED)
        # Indicate execution phase has started without clearing the file preview lists
        for widget in self.folder_widgets.values():
            widget.update_status("Executing...", "orange")
        # Start background worker to execute planned actions
        folder_paths = [Path(p) for p in self.selected_folders]
        worker = SyncWorker(self.sync_engine, folder_paths, self.planned_actions)
        worker.start()

    def _process_events(self):
        """Process events from the event queue periodically."""
        # Process all events currently in the queue
        while not self.event_queue.empty():
            try:
                event = self.event_queue.get_nowait()
                # Handle different event types using the current ProgressEvent schema
                if event.event_type == EventType.SCAN_START:
                    # Global scan start – mark all folders as scanned
                    for widget in self.folder_widgets.values():
                        widget.update_status("Scanned", "green")
                elif event.event_type == EventType.SCAN_FILE:
                    # Per-folder scan notification when folder is available
                    folder_widget = self.folder_widgets.get(event.folder)
                    if folder_widget:
                        folder_widget.update_status("Scanned", "green")
                elif event.event_type == EventType.COPY:
                    # A file was copied; show generic syncing state
                    for widget in self.folder_widgets.values():
                        widget.update_status("Syncing...", "orange")
                elif event.event_type == EventType.SKIP:
                    # In dry-run, files are skipped; detailed per-file preview is handled
                    # in the planning stage, so we keep the UI unchanged here.
                    pass
                elif event.event_type == EventType.ERROR:
                    # Show a generic error state; detailed message goes to the log
                    for widget in self.folder_widgets.values():
                        widget.update_status("Error during sync", "red")
                elif event.event_type == EventType.COMPLETE:
                    # Re-enable buttons when the engine signals completion
                    self.is_syncing = False
                    self.sync_button.config(state=tk.NORMAL)
                    self.browse_button.config(state=tk.NORMAL)
                    # Update folder statuses to a clear completed state
                    if self.config.get("dry_run", False):
                        for widget in self.folder_widgets.values():
                            widget.update_status("Dry run complete", "blue")
                    else:
                        for widget in self.folder_widgets.values():
                            widget.update_status("Completed", "green")
                    # For real executions, update preview header and mark files as replaced
                    if not self.config.get("dry_run", False):
                        for widget in self.folder_widgets.values():
                            # The UI can be refreshed (folders removed, rescans) while a background
                            # worker is still running. Make these post-completion updates fail-soft
                            # so a single stale/destroyed widget doesn't crash the whole callback.
                            try:
                                # Update header from "will be" to "were"
                                if hasattr(widget, "update_preview_header_to_completed"):
                                    widget.update_preview_header_to_completed()
                                # Mark each file row with checkmark
                                preview_rows = getattr(widget, "_preview_rows", {})
                                for rel_key in list(preview_rows.keys()):
                                    if hasattr(widget, "mark_preview_replaced"):
                                        widget.mark_preview_replaced(rel_key)
                            except tk.TclError:
                                # Fail soft; destroyed widgets can raise TclError.
                                pass
                        # Also show any .bak backup files that now exist on disk
                        self._update_bak_previews()
                    # Completion status is communicated via folder status and preview updates.
            except queue.Empty:
                break
        # Schedule next check (100ms from now)
        self.root.after(100, self._process_events)

    def _open_settings_window(self) -> None:
        """Open the settings configuration window."""
        settings_window.open_settings_window(
            self.root, self.config, self._on_settings_saved
        )

    def _on_settings_saved(self, updated_config: dict) -> None:
        """Receive updated config from the settings dialog and sync app state.
        Args:
            updated_config: The mutated config dict returned from the settings dialog.
        """
        self.config = updated_config
        self.favorite_folders = list(updated_config.get("folders_faves", []))
        self._update_dry_run_status()
        self._update_ignore_patterns_display()

    def _set_folder_favorite(self, folder_path: str, is_favorite: bool) -> None:
        """Add or remove a folder from the favorites list and persist to config."""
        # Ignore missing or empty paths
        if not folder_path:
            return
        try:
            normalized = file_path_utils.normalize_path(folder_path)
        except Exception as exc:
            # Log and fail soft; GUI should not crash on bad path
            print(f"Error normalizing favorite folder path {folder_path!r}: {exc}")
            return
        changed = False
        if is_favorite:
            if normalized not in self.favorite_folders:
                self.favorite_folders.append(normalized)
                changed = True
        else:
            if normalized in self.favorite_folders:
                self.favorite_folders.remove(normalized)
                changed = True
        if changed:
            self._save_favorites_to_config()

    def _save_favorites_to_config(self) -> None:
        """Persist favorite folders to config."""
        self.config["folders_faves"] = list(self.favorite_folders)
        config_sync.save_config(self.config)

    def _load_favorite_folders(self) -> None:
        """Load favorite folders into the selected folders list and update UI."""
        if self.is_syncing:
            return
        if not self.favorite_folders:
            messagebox.showinfo(
                "No Favorites",
                "No favorite folders are configured in config.txt."
            )
            return
        # Always start over from a clean screen so clicking Load Favorites after a
        # completed cycle shows only the freshly loaded favorites and a fresh Scan state.
        self._reset_loaded_folder_state()
        # Keep this list strictly str for safe display/joining (favorites can be Path objects).
        skipped: list[str] = []
        added_any = False
        for fav in self.favorite_folders:
            try:
                normalized = file_path_utils.normalize_path(fav)
            except Exception as exc:
                print(f"Error normalizing favorite folder {fav!r}: {exc}")
                skipped.append(str(fav))
                continue
            # If the project doesn't have a scaffold dir yet, create it (user-friendly behavior for new projects).
            scaffold_folder = self.config.get("scaffold_folder", ".kilocode")
            try:
                file_path_utils.ensure_scaffold_dir(normalized, scaffold_folder)
            except Exception as exc:
                print(f"Error ensuring {scaffold_folder} directory under {normalized!s}: {exc}")
                skipped.append(str(normalized))
                continue
            # Validate folder has a scaffold directory
            if not file_path_utils.has_scaffold_dir(normalized, scaffold_folder):
                skipped.append(str(normalized))
                continue
            if normalized not in self.selected_folders:
                self.selected_folders.append(normalized)
                added_any = True
        if added_any:
            self._update_folder_list_ui()
        if skipped:
            msg_lines = ["Some favorites are invalid and were skipped:"] + skipped
            msg = "\n".join(msg_lines)
            print(msg)
            # Optional UX: inform the user once about skipped favorites
            messagebox.showinfo("Favorites Skipped", msg)

    def _save_current_selection_as_favorites(self) -> None:
        """Save the current selected_folders as the new favorites and persist."""
        favs: list[str] = []
        for p in self.selected_folders:
            try:
                favs.append(file_path_utils.normalize_path(p))
            except Exception as exc:
                print(f"Error normalizing selected folder for saving favorites {p!r}: {exc}")
        # Remove duplicates while preserving order
        seen = set()
        unique = []
        for p in favs:
            if p not in seen:
                seen.add(p)
                unique.append(p)
        self.favorite_folders = unique
        self._save_favorites_to_config()
        messagebox.showinfo("Favorites Saved", "Favorites saved from current selection.")

    def _delete_bak_files(self) -> None:
        """Delete all .bak backup files in the listed folders."""
        if not self.selected_folders:
            messagebox.showinfo(
                "Delete .bak Files",
                "No folders are selected. Select folders before deleting backups."
            )
            return
        # Proceed immediately without an extra confirmation dialog to keep cleanup fast.
        deleted_count = 0
        errors: list[str] = []
        for folder in self.selected_folders:
            base_path = Path(folder)
            if not base_path.exists():
                continue
            # Collect all .bak files first to avoid generator iteration issues during deletion
            bak_files = list(base_path.rglob("*.bak"))
            # Delete all .bak files anywhere under this base folder
            for bak in bak_files:
                try:
                    bak.unlink()
                    deleted_count += 1
                except OSError as exc:
                    errors.append(f"{bak}: {exc}")
        if deleted_count == 0:
            messagebox.showinfo(
                "Delete .bak Files",
                "No .bak backup files were found to delete in the listed folders."
            )
        else:
            if errors:
                print("Some .bak files could not be deleted:\n" + "\n".join(errors))
        # After deletion, refresh only the .bak backup previews
        # so the executed/updated file list remains visible until the next Scan.
        self._update_bak_previews()

    def _update_dry_run_status(self):
        """Update the dry run status label based on current config."""
        if self.dry_run_label:
            if self.config.get("dry_run", False):
                self.dry_run_label.config(
                    text="⚠ DRY RUN MODE: No files will be modified",
                    foreground="red",
                    font=("TkDefaultFont", self.config["ui_font_size_dry_run"], "bold")
                )
            else:
                self.dry_run_label.config(text="")

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling for the folder canvas.
        Args:
            event: The mouse wheel event
        """
        # Only respond to events originating from the main window (not modal dialogs)
        if event.widget.winfo_toplevel() is not self.root:
            return
        self.folder_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _update_ignore_patterns_display(self):
        """Update the ignore patterns display label based on current config."""
        if self.ignore_patterns_label:
            self.ignore_patterns_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
