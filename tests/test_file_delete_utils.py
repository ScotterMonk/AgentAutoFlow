"""Tests for utils_sync.file_delete_utils — no Tkinter required."""

import pytest
from pathlib import Path

from utils_sync.file_delete_utils import (
    delete_file_across_folders,
    delete_file_and_folder_across_folders,
)


# ---------------------------------------------------------------------------
# delete_file_across_folders
# ---------------------------------------------------------------------------

def test_delete_file_across_folders_success(tmp_path):
    """File in .roo/ subdir is deleted; returns count=1 and no errors."""
    # Arrange: create .roo/rules/example.md inside tmp_path
    roo_dir = tmp_path / ".roo" / "rules"
    roo_dir.mkdir(parents=True)
    target_file = roo_dir / "example.md"
    target_file.write_text("# test content")

    relative_path = "rules/example.md"

    # Act
    deleted_count, errors = delete_file_across_folders(
        relative_path=relative_path,
        action={},
        favorite_folders=[str(tmp_path)],
    )

    # Assert
    assert errors == []
    assert deleted_count == 1
    assert not target_file.exists()


def test_delete_file_across_folders_skips_directory(tmp_path):
    """When target path is a directory, refuses to delete and records an error."""
    # Arrange: create a directory where a file would normally be
    roo_dir = tmp_path / ".roo" / "rules"
    roo_dir.mkdir(parents=True)
    # The "file" path is actually a directory
    dir_as_file = roo_dir / "subdir"
    dir_as_file.mkdir()

    relative_path = "rules/subdir"

    # Act
    deleted_count, errors = delete_file_across_folders(
        relative_path=relative_path,
        action={},
        favorite_folders=[str(tmp_path)],
    )

    # Assert
    assert deleted_count == 0
    assert len(errors) == 1
    assert "Refusing to delete folder" in errors[0]
    assert dir_as_file.exists()  # directory untouched


def test_delete_file_across_folders_missing_file_no_error(tmp_path):
    """Non-existent target is silently skipped — count stays 0, no errors."""
    (tmp_path / ".roo").mkdir()

    deleted_count, errors = delete_file_across_folders(
        relative_path="rules/missing.md",
        action={},
        favorite_folders=[str(tmp_path)],
    )

    assert deleted_count == 0
    assert errors == []


def test_delete_file_across_folders_also_deletes_source(tmp_path):
    """source_path in action dict is deleted in addition to favorite-folder copies."""
    # Arrange favorite copy
    roo_dir = tmp_path / ".roo" / "rules"
    roo_dir.mkdir(parents=True)
    fav_file = roo_dir / "note.md"
    fav_file.write_text("fav")

    # Arrange source (separate location, not under tmp_path/.roo)
    source_dir = tmp_path / "source_project" / ".roo" / "rules"
    source_dir.mkdir(parents=True)
    source_file = source_dir / "note.md"
    source_file.write_text("src")

    deleted_count, errors = delete_file_across_folders(
        relative_path="rules/note.md",
        action={"source_path": str(source_file)},
        favorite_folders=[str(tmp_path)],
    )

    assert errors == []
    assert deleted_count == 2
    assert not fav_file.exists()
    assert not source_file.exists()


# ---------------------------------------------------------------------------
# delete_file_and_folder_across_folders
# ---------------------------------------------------------------------------

def test_delete_file_and_folder_across_folders_success(tmp_path):
    """File and its parent folder are deleted; parent is not the .roo root."""
    roo_dir = tmp_path / ".roo" / "skills" / "my-skill"
    roo_dir.mkdir(parents=True)
    skill_file = roo_dir / "SKILL.md"
    skill_file.write_text("# skill")

    deleted_files, deleted_folders, errors = delete_file_and_folder_across_folders(
        relative_path="skills/my-skill/SKILL.md",
        action={},
        favorite_folders=[str(tmp_path)],
    )

    assert errors == []
    assert deleted_files == 1
    assert deleted_folders == 1
    assert not skill_file.exists()
    assert not roo_dir.exists()


def test_delete_file_and_folder_skips_when_parent_is_roo_root(tmp_path):
    """When the file sits directly in .roo/, the .roo folder itself is NOT deleted."""
    roo_dir = tmp_path / ".roo"
    roo_dir.mkdir(parents=True)
    top_file = roo_dir / "top.md"
    top_file.write_text("top-level file")

    deleted_files, deleted_folders, errors = delete_file_and_folder_across_folders(
        relative_path="top.md",
        action={},
        favorite_folders=[str(tmp_path)],
    )

    assert errors == []
    assert deleted_files == 1
    assert deleted_folders == 0   # .roo root must NOT be removed
    assert not top_file.exists()
    assert roo_dir.exists()       # .roo directory still present


def test_delete_file_and_folder_target_is_directory(tmp_path):
    """Target that is itself a directory is refused and counted as error."""
    roo_dir = tmp_path / ".roo" / "skills"
    roo_dir.mkdir(parents=True)
    dir_target = roo_dir / "some-skill"
    dir_target.mkdir()

    deleted_files, deleted_folders, errors = delete_file_and_folder_across_folders(
        relative_path="skills/some-skill",
        action={},
        favorite_folders=[str(tmp_path)],
    )

    assert deleted_files == 0
    assert len(errors) == 1
    assert "Refusing to delete folder as file" in errors[0]
    assert dir_target.exists()
