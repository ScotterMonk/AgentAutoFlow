"""Modal settings dialog for AgentAutoFlow sync configuration."""

import tkinter as tk
from tkinter import ttk, messagebox
from utils_sync import config_sync, file_path_utils


def open_settings_window(
    root: tk.Tk,
    config: dict,
    on_saved: callable,
) -> None:
    """Build and show the modal settings dialog.

    Args:
        root: The parent Tk window (for centering and transient binding).
        config: Current application config dict (read-only reference for defaults).
        on_saved: Callback invoked with the updated config dict after Save.
                  Signature: on_saved(updated_config: dict) -> None
    """
    # [Created-or-Modified] by openai/gpt-5.1 | 2025-11-16_01

    # Create modal window
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.transient(root)
    settings_window.configure(bg=config["ui_dark_bg"])

    # Calculate centered position on main window
    root.update_idletasks()

    # Settings window dimensions
    settings_width = 600
    settings_height = 560

    # Get main window position and size
    main_x = root.winfo_x()
    main_y = root.winfo_y()
    main_width = root.winfo_width()
    main_height = root.winfo_height()

    # Calculate center position
    center_x = main_x + (main_width - settings_width) // 2
    center_y = main_y + (main_height - settings_height) // 2

    # Set geometry with centered position
    settings_window.geometry(f"{settings_width}x{settings_height}+{center_x}+{center_y}")
    settings_window.grab_set()

    # Main frame with padding
    main_frame = ttk.Frame(settings_window, padding="15")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Title
    title_label = ttk.Label(
        main_frame,
        text="Sync Configuration",
        font=("TkDefaultFont", config["ui_font_size_section_title"], "bold")
    )
    title_label.pack(pady=(0, 10))

    # Backup mode
    backup_frame = ttk.Frame(main_frame)
    backup_frame.pack(fill=tk.X, pady=5)
    ttk.Label(backup_frame, text="Backup Mode:").pack(side=tk.LEFT)
    backup_var = tk.StringVar(value=config.get("backup_mode", "timestamped"))
    backup_combo = ttk.Combobox(
        backup_frame,
        textvariable=backup_var,
        values=["timestamped", "none"],
        state="readonly",
        width=15
    )
    backup_combo.pack(side=tk.LEFT, padx=(10, 0))

    # Dry run
    dryrun_var = tk.BooleanVar(value=config.get("dry_run", False))
    dryrun_check = ttk.Checkbutton(
        main_frame,
        text="Dry run (preview changes only)",
        variable=dryrun_var
    )
    dryrun_check.pack(fill=tk.X, pady=5)

    # File compare threshold (seconds)
    threshold_frame = ttk.Frame(main_frame)
    threshold_frame.pack(fill=tk.X, pady=5)
    ttk.Label(threshold_frame, text="File compare threshold (seconds):").pack(side=tk.LEFT)
    threshold_var = tk.StringVar(value=str(config.get("file_compare_threshold_sec", 2)))
    threshold_entry = ttk.Entry(threshold_frame, textvariable=threshold_var, width=8)
    threshold_entry.pack(side=tk.LEFT, padx=(10, 0))
    ttk.Label(
        main_frame,
        text="Files with timestamps within this many seconds are treated as equal (milliseconds ignored).",
        font=("TkDefaultFont", config["ui_font_size_hint"]),
    ).pack(anchor=tk.W)

    # Ignore patterns
    ignore_frame = ttk.Frame(main_frame)
    ignore_frame.pack(fill=tk.X, pady=5)
    ttk.Label(ignore_frame, text="Ignore Patterns:").pack(anchor=tk.W)
    ttk.Label(
        ignore_frame,
        text="(comma-separated; wraps automatically)",
        font=("TkDefaultFont", config["ui_font_size_hint"])
    ).pack(anchor=tk.W)

    current_patterns = config.get("ignore_patterns", [])
    patterns_str = ", ".join(current_patterns) if current_patterns else ""
    ignore_text = tk.Text(
        ignore_frame,
        height=5,
        wrap="word",
        bg=config["ui_dark_bg_alt"],
        fg=config["ui_fg_primary"],
        insertbackground=config["ui_fg_primary"],
    )
    ignore_text.insert("1.0", patterns_str)
    ignore_text.pack(fill=tk.X, pady=(5, 0))

    # Favorite folders from config (folders_faves)
    faves_frame = ttk.Frame(main_frame)
    faves_frame.pack(fill=tk.X, pady=5)
    ttk.Label(faves_frame, text="Favorite Folders (config.txt):").pack(anchor=tk.W)
    ttk.Label(
        faves_frame,
        text="(comma-separated folder paths; wraps automatically)",
        font=("TkDefaultFont", config["ui_font_size_hint"])
    ).pack(anchor=tk.W)

    current_faves = config.get("folders_faves", [])
    faves_str = ", ".join(current_faves) if current_faves else ""
    faves_text = tk.Text(
        faves_frame,
        height=8,
        wrap="word",
        bg=config["ui_dark_bg_alt"],
        fg=config["ui_fg_primary"],
        insertbackground=config["ui_fg_primary"],
    )
    faves_text.insert("1.0", faves_str)
    faves_text.pack(fill=tk.X, pady=(5, 0))

    # Nested save function — no self/MainApp references
    def _save(window, backup_mode, dry_run, file_compare_threshold_sec,
              ignore_patterns_str, folders_faves_str):
        """Validate, persist, and notify via on_saved callback.

        Args:
            window: The settings Toplevel to destroy after saving.
            backup_mode: The selected backup mode string.
            dry_run: Boolean; whether dry-run mode is active.
            file_compare_threshold_sec: Raw string value from threshold entry.
            ignore_patterns_str: Comma-separated ignore patterns from text widget.
            folders_faves_str: Comma-separated favorite folder paths from text widget.
        """
        # Parse ignore patterns
        patterns = [p.strip() for p in ignore_patterns_str.split(",") if p.strip()]

        # Parse favorite folders (folders_faves)
        raw_faves = [p.strip() for p in folders_faves_str.split(",") if p.strip()]
        normalized_faves = []
        for fav in raw_faves:
            try:
                normalized_faves.append(file_path_utils.normalize_path(fav))
            except Exception as exc:
                # Fail soft on bad paths; keep original string
                print(f"Error normalizing favorite folder from settings {fav!r}: {exc}")
                normalized_faves.append(fav)

        # Update config (mutates the passed-in dict in-place — intentional)
        config["backup_mode"] = backup_mode
        config["dry_run"] = dry_run

        # Parse compare threshold
        try:
            thr = int(str(file_compare_threshold_sec).strip())
            if thr < 0:
                thr = 0
        except Exception:
            thr = int(config.get("file_compare_threshold_sec", 2) or 2)
        config["file_compare_threshold_sec"] = thr

        config["ignore_patterns"] = patterns
        config["folders_faves"] = normalized_faves

        # Persist to file
        config_sync.save_config(config)

        # Close window, then notify caller so MainApp can refresh its UI
        window.destroy()
        on_saved(config)

        # Show confirmation after callback so MainApp state is resolved first
        messagebox.showinfo("Settings Saved", "Configuration has been saved successfully.")

    # Button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=(15, 0))

    # Cancel button
    cancel_button = ttk.Button(
        button_frame,
        text="Cancel",
        command=settings_window.destroy,
        style="AF.TButton",
    )
    cancel_button.pack(side=tk.LEFT, padx=5)

    # Save button — calls nested _save; no self references
    save_button = ttk.Button(
        button_frame,
        text="Save",
        style="AF.TButton",
        command=lambda: _save(
            settings_window,
            backup_var.get(),
            dryrun_var.get(),
            threshold_var.get(),
            ignore_text.get("1.0", "end"),
            faves_text.get("1.0", "end")
        )
    )
    save_button.pack(side=tk.LEFT, padx=5)
