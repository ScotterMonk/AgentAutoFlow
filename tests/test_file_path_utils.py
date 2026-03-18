import os
import sys
from pathlib import Path
from utils_sync import file_path_utils

# [Created-or-Modified] by [LLM model] | 2025-11-13_01

def test_normalize_path_expands_and_resolves(tmp_path):
    # Create a nested folder and a file
    folder = tmp_path / "someFolder"
    folder.mkdir()
    f = folder / "file.txt"
    f.write_text("hello")
    # Use an env var and ~ expansion simulation by passing absolute path string
    normalized = file_path_utils.normalize_path(str(folder))
    assert isinstance(normalized, Path)
    assert normalized.is_absolute()
    assert normalized.exists()
    # Trailing slashes should be handled
    normalized2 = file_path_utils.normalize_path(str(folder) + os.sep)
    assert normalized == normalized2

def test_deduplicate_paths_preserves_order_and_normalizes(tmp_path):
    a = tmp_path / "A"
    b = tmp_path / "B"
    a.mkdir()
    b.mkdir()
    # create same path twice with different representations
    paths = [str(a), a.as_posix(), str(b)]
    result = file_path_utils.deduplicate_paths(paths)
    assert len(result) == 2
    assert result[0] == file_path_utils.normalize_path(a)
    assert result[1] == file_path_utils.normalize_path(b)

def test_has_scaffold_dir_positive_and_negative(tmp_path):
    base = tmp_path / "project"
    base.mkdir()
    # Negative: no scaffold dir
    assert file_path_utils.has_scaffold_dir(base, ".kilocode") is False
    # Positive: create scaffold directory (real dir)
    roo = base / ".kilocode"
    roo.mkdir()
    assert file_path_utils.has_scaffold_dir(base, ".kilocode") is True
    # If scaffold dir is a symlink (if filesystem supports), create a symlink and expect False
    # Some filesystems or platforms (Windows) may require admin rights; skip symlink test if not permitted
    try:
        target = tmp_path / "target_scaffold"
        target.mkdir()
        link = base / ".kilocode_link"
        # create symlink pointing at target
        link.symlink_to(target, target_is_directory=True)
        # has_scaffold_dir checks for the exact scaffold_folder name; symlinks are ignored
        # Ensure the function does not crash when encountering symlinked entries
        # This is just to confirm behavior doesn't raise; result may be False since name isn't ".kilocode"
        _ = file_path_utils.has_scaffold_dir(base, ".kilocode")
    except (OSError, NotImplementedError):
        # symlink creation not allowed on this platform; that's acceptable for test portability
        pass

def test_get_scaffold_relative_path_returns_relative_when_inside_scaffold(tmp_path):
    base = tmp_path / "proj"
    base.mkdir()
    scaffold = base / ".kilocode"
    scaffold.mkdir()
    nested = scaffold / "rules"
    nested.mkdir(parents=True)
    file = nested / "01.md"
    file.write_text("content")
    # full path inside scaffold dir should return relative path 'rules/01.md'
    rel = file_path_utils.get_scaffold_relative_path(file, base, ".kilocode")
    assert rel == "rules/01.md"
    # calling with the scaffold directory itself returns None
    assert file_path_utils.get_scaffold_relative_path(scaffold, base, ".kilocode") is None
    # outside path returns None
    outside = tmp_path / "other.txt"
    outside.write_text("x")
    assert file_path_utils.get_scaffold_relative_path(outside, base, ".kilocode") is None


def test_get_project_folder_name_prefers_parent_of_app(tmp_path):
    # Path with /app/ should return the folder name above app
    root = tmp_path / "SomeProject"
    app_dir = root / "app"
    app_dir.mkdir(parents=True)

    assert file_path_utils.get_project_folder_name(app_dir) == "SomeProject"


def test_get_project_folder_name_falls_back_to_selected_folder_name(tmp_path):
    # No /app/ segment -> return the selected folder name (houses scaffold dir)
    project = tmp_path / "project_x"
    project.mkdir(parents=True)
    (project / ".kilocode").mkdir()

    assert file_path_utils.get_project_folder_name(project) == "project_x"
