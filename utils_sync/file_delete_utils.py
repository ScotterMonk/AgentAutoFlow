"""File deletion utilities for synced scaffold folders (no Tkinter dependency)."""

from pathlib import Path
import shutil


def delete_file_across_folders(
    relative_path: str,
    action: dict,
    favorite_folders: list[str],
    scaffold_folder: str = ".kilocode",
) -> tuple[int, list[str]]:
    """Delete a scaffold-relative file from every favorite folder plus source/dest.

    Args:
        relative_path: Path relative to the scaffold subdirectory.
        action: Sync action dict with optional 'source_path' and 'destination_path'.
        favorite_folders: List of absolute folder paths to search.
        scaffold_folder: Scaffold subdirectory name (e.g. ".kilocode" or ".roo").

    Returns:
        (deleted_count, errors): count of files deleted and list of error strings.
    """
    source_path = action.get("source_path")
    dest_path = action.get("destination_path")

    deleted_count = 0
    errors = []

    # Delete in ALL favorite folders (files are in scaffold subdirectory)
    for fav_folder in favorite_folders:
        try:
            fav_base = Path(fav_folder) / scaffold_folder
            target = fav_base / relative_path

            if target.exists():
                if target.is_dir():
                    errors.append(f"Refusing to delete folder:\n{target}")
                else:
                    target.unlink()
                    deleted_count += 1
        except Exception as exc:
            errors.append(f"Delete failed:\n{fav_folder}/{relative_path}\n{exc}")

    # Also delete SOURCE file (if different from favorites)
    if source_path:
        try:
            source = Path(source_path)
            if source.exists() and not source.is_dir():
                source.unlink()
                deleted_count += 1
        except Exception as exc:
            errors.append(f"Source delete failed:\n{source_path}\n{exc}")

    # Also delete DESTINATION file (if different from favorites)
    if dest_path:
        try:
            dest = Path(dest_path)
            if dest.exists() and not dest.is_dir():
                dest.unlink()
                deleted_count += 1
        except Exception as exc:
            errors.append(f"Destination delete failed:\n{dest_path}\n{exc}")

    return (deleted_count, errors)


def delete_file_and_folder_across_folders(
    relative_path: str,
    action: dict,
    favorite_folders: list[str],
    scaffold_folder: str = ".kilocode",
) -> tuple[int, int, list[str]]:
    """Delete a scaffold-relative file AND its parent folder from every favorite folder.

    Args:
        relative_path: Path relative to the scaffold subdirectory.
        action: Sync action dict with optional 'source_path' and 'destination_path'.
        favorite_folders: List of absolute folder paths to search.
        scaffold_folder: Scaffold subdirectory name (e.g. ".kilocode" or ".roo").

    Returns:
        (deleted_files, deleted_folders, errors).
    """
    source_path = action.get("source_path")
    dest_path = action.get("destination_path")

    deleted_files = 0
    deleted_folders = 0
    errors = []

    def _delete_file_and_parent(target: Path, scaffold_base: Path) -> None:
        """Delete target file then its immediate parent folder (if not the scaffold root)."""
        nonlocal deleted_files, deleted_folders
        if target.exists():
            if target.is_dir():
                errors.append(f"Refusing to delete folder as file:\n{target}")
                return
            target.unlink()
            deleted_files += 1

        # Delete the immediate parent folder, but never the scaffold root itself
        parent = target.parent
        try:
            # Resolve both to compare safely
            if parent.resolve() != scaffold_base.resolve():
                if parent.exists():
                    shutil.rmtree(parent)
                    deleted_folders += 1
        except Exception as exc:
            errors.append(f"Folder delete failed:\n{parent}\n{exc}")

    # Delete in ALL favorite folders
    for fav_folder in favorite_folders:
        try:
            scaffold_base = Path(fav_folder) / scaffold_folder
            target = scaffold_base / relative_path
            _delete_file_and_parent(target, scaffold_base)
        except Exception as exc:
            errors.append(f"Failed in favorite:\n{fav_folder}/{relative_path}\n{exc}")

    # Also handle source path (if different from favorites)
    if source_path:
        try:
            source = Path(source_path)
            # Find the scaffold base for the source by walking up to find the scaffold parent
            scaffold_base = None
            for fav_folder in favorite_folders:
                candidate = Path(fav_folder) / scaffold_folder
                try:
                    source.relative_to(candidate)
                    scaffold_base = candidate
                    break
                except ValueError:
                    continue
            if scaffold_base and source.exists() and not source.is_dir():
                _delete_file_and_parent(source, scaffold_base)
            elif not scaffold_base and source.exists() and not source.is_dir():
                # Fallback: just delete the file, guess parent is not scaffold root
                source.unlink()
                deleted_files += 1
        except Exception as exc:
            errors.append(f"Source delete failed:\n{source_path}\n{exc}")

    # Also handle destination path
    if dest_path:
        try:
            dest = Path(dest_path)
            scaffold_base = None
            for fav_folder in favorite_folders:
                candidate = Path(fav_folder) / scaffold_folder
                try:
                    dest.relative_to(candidate)
                    scaffold_base = candidate
                    break
                except ValueError:
                    continue
            if scaffold_base and dest.exists() and not dest.is_dir():
                _delete_file_and_parent(dest, scaffold_base)
            elif not scaffold_base and dest.exists() and not dest.is_dir():
                dest.unlink()
                deleted_files += 1
        except Exception as exc:
            errors.append(f"Dest delete failed:\n{dest_path}\n{exc}")

    return (deleted_files, deleted_folders, errors)
