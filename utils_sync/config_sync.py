"""Utilities for sync configuration loading."""
import os
from typing import Dict, Any, List, Optional
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

DEFAULTS = {
    "window_width": 800,
    "window_height": 480,
    # When comparing mtimes across folders, treat files as "effectively equal" when
    # their mtimes differ by <= this many seconds. Milliseconds are ignored.
    "file_compare_threshold_sec": 2,
    "ignore_patterns": [".git", "__pycache__", ".venv", ".idea", ".vscode", "node_modules", "*.pyc"],
    "backup_mode": "timestamped",
    "dry_run": False,
    "root_allowlist": [],  # comma-separated list of root-level files to sync
    "folders_faves": [],  # comma-separated list of favorite folders for UI
    # UI Colors for dark mode
    "ui_dark_bg": "#000000",
    "ui_dark_bg_alt": "#111111",
    "ui_fg_primary": "#e0e0e0",
    "ui_button_bg": "#000000",
    "ui_button_bg_hover": "#111111",
    "ui_button_border": "#00ff5f",
    "ui_button_text": "#e0e0e0",
    # UI Font sizes
    "ui_font_size_title": 16,
    "ui_font_size_project": 12,
    "ui_font_size_section_title": 11,
    "ui_font_size_hint": 11,
    "ui_font_size_dry_run": 11,
    "ui_font_size_folder_preview_header": 11,
    "ui_font_size_folder_preview_row": 11,
}


def _to_bool(value: str) -> bool:
    # [Created-or-Modified] by [LLM model] | 2025-11-13_01
    """
    Convert common truthy/falsy string values to bool.
    """
    return str(value).strip().lower() in ("1", "true", "yes", "y", "on")


def resolve_config_path(config_path: Optional[str] = None) -> str:
    # [Created-or-Modified] by [LLM model] | 2025-11-13_01
    """
    Resolve the config file path, checking .env for AgentAutoFlow_CONFIG.

    Args:
        config_path: Optional explicit config path

    Returns:
        Resolved config file path
    """
    if config_path:
        return config_path

    # Try to load .env if available
    if DOTENV_AVAILABLE:
        load_dotenv()
        env_config = os.getenv("AgentAutoFlow_CONFIG")
        if env_config:
            return env_config

    # Default fallback
    return "config.txt"


def load_config(config_path: Optional[str] = None):
    # [Created-or-Modified] by gpt-5.2 | 2026-01-11_01
    """
    Load a simple key=value config file and return a dict with typed values
    and defaults applied.

    Args:
        config_path: Optional explicit config path. If None, resolves via resolve_config_path().

    Rules:
    - Lines beginning with '#' or empty lines are skipped.
    - Keys and values are trimmed of whitespace.
    - Integers: window_width, window_height (must be positive).
    - Integers: file_compare_threshold_sec (must be >= 0).
    - Booleans: dry_run (true/false, case-insensitive).
    - ignore_patterns: comma-separated list -> list of strings.
    - root_allowlist: comma-separated list -> list of strings.
    - folders_faves: comma-separated list -> list of strings.
    - Unknown keys are returned as strings.
    - If file missing or parsing error, defaults are returned.
    """
    config: Dict[str, Any] = DEFAULTS.copy()

    resolved_path = resolve_config_path(config_path)

    if not os.path.exists(resolved_path):
        return config.copy()

    try:
        # Always open the resolved config path (handles default, .env, or explicit paths)
        with open(resolved_path, "r", encoding="utf-8") as fh:
            for raw in fh:
                line = raw.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    # ignore malformed lines
                    continue
                key_part, val_part = line.split("=", 1)
                key = key_part.strip()
                val = val_part.strip()

                if key in ("window_width", "window_height"):
                    try:
                        ival = int(val)
                        if ival > 0:
                            config[key] = ival
                        # else: leave default
                    except ValueError:
                        # leave default on invalid int
                        pass
                elif key == "file_compare_threshold_sec":
                    try:
                        ival = int(val)
                        if ival >= 0:
                            config[key] = ival
                        # else: leave default
                    except ValueError:
                        # leave default on invalid int
                        pass
                elif key in ("ui_font_size_title", "ui_font_size_project", "ui_font_size_section_title",
                            "ui_font_size_hint", "ui_font_size_dry_run", "ui_font_size_folder_preview_header",
                            "ui_font_size_folder_preview_row"):
                    try:
                        ival = int(val)
                        if ival > 0:
                            config[key] = ival
                        # else: leave default
                    except ValueError:
                        # leave default on invalid int
                        pass
                elif key == "dry_run":
                    config[key] = _to_bool(val)
                elif key == "ignore_patterns":
                    parts: List[str] = [p.strip() for p in val.split(",") if p.strip()]
                    config[key] = parts
                elif key == "root_allowlist":
                    parts: List[str] = [p.strip() for p in val.split(",") if p.strip()]
                    config[key] = parts
                elif key == "folders_faves":
                    parts: List[str] = [p.strip() for p in val.split(",") if p.strip()]
                    config[key] = parts
                elif key.startswith("ui_"):
                    # UI color/string settings - store as string
                    config[key] = val
                else:
                    # store as string for unknown keys
                    config[key] = val
    except Exception:
        # On any IO/parsing error, return defaults to avoid crashing callers
        return config.copy()

    # Final validation and normalization
    if not isinstance(config.get("window_width"), int) or config["window_width"] <= 0:
        config["window_width"] = DEFAULTS["window_width"]
    if not isinstance(config.get("window_height"), int) or config["window_height"] <= 0:
        config["window_height"] = DEFAULTS["window_height"]
    if (
        not isinstance(config.get("file_compare_threshold_sec"), int)
        or config["file_compare_threshold_sec"] < 0
    ):
        config["file_compare_threshold_sec"] = DEFAULTS["file_compare_threshold_sec"]
    if not isinstance(config.get("ignore_patterns"), list):
        config["ignore_patterns"] = DEFAULTS["ignore_patterns"].copy()
    if not isinstance(config.get("root_allowlist"), list):
        config["root_allowlist"] = DEFAULTS["root_allowlist"].copy()
    if not isinstance(config.get("folders_faves"), list):
        config["folders_faves"] = DEFAULTS["folders_faves"].copy()

    if not isinstance(config.get("dry_run"), bool):
        config["dry_run"] = bool(config.get("dry_run"))

    return config


def save_config(config_dict: Dict[str, Any], path: str = "config.txt") -> bool:
    # [Created-or-Modified] by gpt-5.2 | 2026-01-11_01
    """
    Serialize config_dict to a simple key=value file.

    Serialization rules:
    - bool -> "true" or "false" (lowercase)
    - list -> comma-separated values with a single space after the comma
      (e.g., ".git, __pycache__")
    - int -> decimal string
    - other types -> str(value)

    Writes atomically by writing to a temp file in the same folder and then
    using os.replace to move the temp file into place. Ensures UTF-8
    encoding and unix-style newlines. Returns True on success, False on
    failure (exceptions are logged).
    """
    try:
        # create temp path in same folder to ensure atomic replace on same filesystem
        temp_path = f"{path}.tmp"
        # Write with explicit unix newlines
        with open(temp_path, "w", encoding="utf-8", newline="\n") as fh:
            for key, val in config_dict.items():
                # This setting is intentionally removed from the config surface.
                # The sync engine always preserves mtimes.
                if key == "preserve_mtime":
                    continue
                # bool -> "true"/"false"
                if isinstance(val, bool):
                    sval = "true" if val else "false"
                # int -> decimal
                elif isinstance(val, int) and not isinstance(val, bool):
                    sval = str(val)
                # list -> comma separated, single space after comma
                elif isinstance(val, (list, tuple)):
                    sval = ", ".join(str(x) for x in val)
                else:
                    sval = str(val)
                fh.write(f"{key}={sval}\n")
        # atomic replace
        os.replace(temp_path, path)
        return True
    except Exception:
        import logging
        logging.exception("save_config failed for path: %s", path)
        # best-effort cleanup of temp file
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass
        return False
