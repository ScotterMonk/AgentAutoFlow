# [Created-or-Modified] by [LLM model] | 2025-11-13_01
"""
utils_sync.file_path_utils

Utilities for normalizing file system paths and deduplicating path lists.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Union, Iterable, List, Optional


# Basic utilities for path handling used by file-sync tasks.


def normalize_path(p: Union[str, Path]) -> Path:
    # [Created-or-Modified] by [LLM model] | 2025-11-13_01
    """Return an absolute, canonical Path.

    - Expands environment variables and ~.
    - Resolves symlinks where possible without failing on missing files.
    - Returns a pathlib.Path that is absolute.

    Raises:
        ValueError: For invalid input types or empty strings.
    """
    if p is None:
        raise ValueError("p must not be None")
    if isinstance(p, Path):
        s = str(p)
    elif isinstance(p, str):
        s = p
    else:
        raise ValueError("p must be a str or pathlib.Path")
    s = s.strip()
    if not s:
        raise ValueError("p must not be empty")
    # Expand env vars and user (~)
    expanded = os.path.expandvars(os.path.expanduser(s))
    # Try to resolve symlinks safely; strict=False avoids raising on missing targets.
    try:
        resolved = Path(expanded).resolve(strict=False)
    except Exception:
        # Fallback to absolute path if resolve fails for any reason.
        resolved = Path(os.path.abspath(expanded))
    return resolved


def deduplicate_paths(paths: Iterable[Union[str, Path]]) -> List[Path]:
    # [Created-or-Modified] by [LLM model] | 2025-11-13_01
    """Normalize and deduplicate an iterable of paths, preserving insertion order.

    Returns a list of resolved Path objects (first occurrence kept).
    """
    if paths is None:
        raise ValueError("paths must not be None")
    seen = set()
    out: List[Path] = []
    for item in paths:
        np = normalize_path(item)
        key = str(np)
        if key not in seen:
            seen.add(key)
            out.append(np)
    return out


def ensure_folder(path: Union[str, Path]) -> Path:
    # [Created-or-Modified] by [LLM model] | 2025-11-13_01
    """Ensure a folder exists at the given path; create it if necessary.

    Returns the normalized Path to the folder.
    """
    if path is None:
        raise ValueError("path must not be None")
    p = normalize_path(path)
    # If path exists and is a file, raise.
    if p.exists() and not p.is_dir():
        raise ValueError(f"Path exists and is not a directory: {p}")
    # Create directory if missing.
    p.mkdir(parents=True, exist_ok=True)
    return p

def has_scaffold_dir(folder_path: Union[str, Path], scaffold_folder: str = ".kilocode") -> bool:
    # [Created-or-Modified] by claude-sonnet-4.6 | 2026-03-18_01
    """
    Return True if the scaffold directory exists directly under the provided folder_path.

    The scaffold directory name is controlled by the `scaffold_folder` config value
    (e.g. ".kilocode" for Kilo Code, ".roo" for Roo Code).

    - Accepts str or Path.
    - Normalizes path using normalize_path().
    - Returns False if folder_path doesn't exist or is not a directory.
    - Treats a symlinked scaffold dir as absent (symlinks are ignored).
    """
    if folder_path is None:
        raise ValueError("folder_path must not be None")
    # normalize_path will raise ValueError for empty/invalid inputs.
    base = normalize_path(folder_path)
    # If base doesn't exist or is not a directory, no scaffold dir can be present.
    if not base.exists() or not base.is_dir():
        return False
    candidate = base / scaffold_folder
    # Treat symlinked scaffold dir as absent: require it be a real directory and not a symlink.
    return candidate.exists() and candidate.is_dir() and not candidate.is_symlink()


def ensure_scaffold_dir(folder_path: Union[str, Path], scaffold_folder: str = ".kilocode") -> Path:
    # [Created-or-Modified] by claude-sonnet-4.6 | 2026-03-18_01
    """Ensure `<folder_path>/<scaffold_folder>` exists as a real directory (not a symlink).

    The scaffold directory name is controlled by the `scaffold_folder` config value
    (e.g. ".kilocode" for Kilo Code, ".roo" for Roo Code).

    If the scaffold directory is missing, it is created.

    Raises:
        ValueError: if folder_path is invalid, not a directory, or the scaffold dir exists but is not
            a real directory (e.g., is a file or a symlink).
        OSError: if the directory cannot be created.
    """
    if folder_path is None:
        raise ValueError("folder_path must not be None")

    base = normalize_path(folder_path)
    if not base.exists() or not base.is_dir():
        raise ValueError(f"Folder does not exist or is not a directory: {base}")

    scaffold_dir = base / scaffold_folder

    if scaffold_dir.exists():
        # Keep safety rail: never operate on a symlinked scaffold dir
        if scaffold_dir.is_symlink():
            raise ValueError(f"{scaffold_folder} is a symlink (not allowed): {scaffold_dir}")
        if not scaffold_dir.is_dir():
            raise ValueError(f"{scaffold_folder} exists but is not a directory: {scaffold_dir}")
        return scaffold_dir

    scaffold_dir.mkdir(parents=True, exist_ok=True)
    return scaffold_dir


# [Created-or-Modified] by claude-sonnet-4.6 | 2026-03-18_01
def get_scaffold_relative_path(
    full_path: Union[str, Path],
    base_folder: Union[str, Path],
    scaffold_folder: str = ".kilocode",
) -> Optional[str]:
    """
    If `full_path` is inside `<base_folder>/<scaffold_folder>/`, return the path relative
    to that scaffold directory as a POSIX-style string (no leading slash), e.g. "rules/01.md".
    If not under the scaffold directory, return None.

    The scaffold directory name is controlled by the `scaffold_folder` config value
    (e.g. ".kilocode" for Kilo Code, ".roo" for Roo Code).

    Behavior:
    - Accepts strings or pathlib.Path.
    - Uses normalize_path() to resolve inputs.
    - Ensures the scaffold directory must be a normal directory (not a symlink) under base_folder.
    - Handles case where full_path equals the scaffold directory itself (return None).
    - Returns None for invalid inputs (or raise ValueError for clearly invalid inputs like empty strings).
    """
    if full_path is None:
        raise ValueError("full_path must not be None")
    if base_folder is None:
        raise ValueError("base_folder must not be None")

    # Normalize inputs using existing utility
    fp = normalize_path(full_path)
    base = normalize_path(base_folder)

    scaffold_dir = base / scaffold_folder

    # Require scaffold dir to exist as a real directory and not be a symlink.
    if not scaffold_dir.exists() or not scaffold_dir.is_dir() or scaffold_dir.is_symlink():
        return None

    # If the provided path equals the scaffold directory itself, return None.
    if fp == scaffold_dir:
        return None

    # If full path is inside scaffold_dir, compute relative path.
    try:
        rel = fp.relative_to(scaffold_dir)
    except Exception:
        return None

    # Return as POSIX-style string with no leading slash.
    return rel.as_posix()


def get_project_folder_name(folder_path: Union[str, Path]) -> str:
    """Return a user-friendly "project folder" name for a selected sync folder.

    Definition (per GUI requirement):
    - If the path contains an "app" segment (case-insensitive), return the folder name
      immediately above that segment (the parent of "/app/").
      Example: "C:/work/MyProject/app" -> "MyProject".
    - Otherwise, fall back to the name of the folder that houses the `.roo/` directory.

    Notes:
    - The GUI typically selects the folder that *contains* the scaffold directory directly.
    - This function is purely for display; it does not touch the filesystem.
    """
    p = normalize_path(folder_path)

    parts = list(p.parts)
    if not parts:
        return str(p)

    parts_lower = [seg.lower() for seg in parts]

    # Prefer the last "app" segment, in case the path contains multiple occurrences.
    for i in range(len(parts_lower) - 1, -1, -1):
        if parts_lower[i] == "app":
            # Use the segment immediately above "app" if it exists.
            if i > 0 and parts[i - 1]:
                return parts[i - 1]
            break

    # Fallback: folder that houses `.roo/`.
    return p.name or str(p)
