import os
import time
import queue
import shutil
from pathlib import Path
import datetime
from utils_sync.sync_core import SyncEngine
from utils_sync.progress_events import EventType

# [Created-or-Modified] by [LLM model] | 2025-11-13_01

def drain_queue(q):
    items = []
    while True:
        try:
            items.append(q.get_nowait())
        except queue.Empty:
            break
    return items

def test_scan_folders_indexes_only_scaffold_files_respects_ignore_patterns(tmp_path):
    q = queue.Queue()
    config = {"ignore_patterns": [".git", "__pycache__"], "scaffold_folder": ".kilocode"}
    engine = SyncEngine(config, q)

    # create folder1 and folder2 with .kilocode scaffold dirs
    base1 = tmp_path / "f1"; base1.mkdir()
    roo1 = base1 / ".kilocode"; roo1.mkdir()
    (roo1 / "a.txt").write_text("v1")
    (roo1 / ".git").mkdir()
    (roo1 / ".git" / "ignore.txt").write_text("secret")

    base2 = tmp_path / "f2"; base2.mkdir()
    roo2 = base2 / ".kilocode"; roo2.mkdir()
    (roo2 / "a.txt").write_text("v2")

    index = engine.scan_folders([base1, base2])

    # ensure 'a.txt' present and .git file ignored
    assert any(k.endswith("a.txt") for k in index.keys())

    # flatten check: there should be two entries for a.txt (one per folder)
    found = 0
    for rel, group in index.items():
        if rel and rel.endswith("a.txt"):
            found += len(group)
    assert found == 2

    events = drain_queue(q)
    assert any(e.event_type == EventType.SCAN_START for e in events)
    assert any(e.event_type == EventType.SCAN_FILE for e in events)


# [Created-or-Modified] by gpt-5.2 | 2026-01-11_01
def test_scan_folders_ignores_bak_files(tmp_path):
    """Backup files should be informational-only and never indexed for planning."""
    q = queue.Queue()
    config = {"ignore_patterns": [], "scaffold_folder": ".kilocode"}
    engine = SyncEngine(config, q)

    base = tmp_path / "proj"; base.mkdir()
    roo = base / ".kilocode"; roo.mkdir()
    (roo / "rules").mkdir()
    (roo / "rules" / "01.md").write_text("content")
    (roo / "rules" / "01.md_20260101T000000Z.bak").write_text("backup")

    index = engine.scan_folders([base])

    # The real file should be present
    assert any(str(k).endswith("rules/01.md") for k in index.keys())
    # The .bak file should never be indexed
    assert not any(str(k).endswith(".bak") for k in index.keys())


# [Created-or-Modified] by claude-sonnet-4.6 | 2026-03-18_01
def test_scan_folders_ignores_scaffold_docs_when_config_uses_legacy_roo_prefix(tmp_path):
    """
    When ignore_patterns contains ".roo/docs" or ".roo\\docs" (legacy prefix), the docs folder
    inside the scaffold directory should be skipped during scanning.
    This verifies backward compatibility: legacy .roo/-prefixed ignore patterns still work.
    """
    q = queue.Queue()
    config = {"ignore_patterns": [".roo/docs", r".roo\docs"], "scaffold_folder": ".kilocode"}
    engine = SyncEngine(config, q)

    base = tmp_path / "proj"; base.mkdir()
    roo = base / ".kilocode"; roo.mkdir()

    # File under .kilocode/docs should be ignored (matched by legacy .roo/docs pattern)
    docs_dir = roo / "docs"; docs_dir.mkdir()
    ignored_file = docs_dir / "ignored.md"
    ignored_file.write_text("to be ignored")

    # File under a different subfolder should still be indexed
    keep_dir = roo / "keep"; keep_dir.mkdir()
    kept_file = keep_dir / "keep.md"
    kept_file.write_text("to be kept")

    index = engine.scan_folders([base])

    # Ensure the kept file is present
    assert any(str(k).endswith("keep/keep.md") for k in index.keys())

    # Ensure nothing from docs/ is present in the index
    assert not any("docs/" in str(k) or str(k).endswith("docs") for k in index.keys())

def test_plan_actions_picks_newest_source(tmp_path):
    q = queue.Queue()
    config = {"ignore_patterns": [], "scaffold_folder": ".kilocode"}
    engine = SyncEngine(config, q)

    base1 = tmp_path / "p1"; base1.mkdir()
    (base1 / ".kilocode").mkdir()
    file1 = base1 / ".kilocode" / "rules" / "01.md"; file1.parent.mkdir(parents=True)
    file1.write_text("old")

    base2 = tmp_path / "p2"; base2.mkdir()
    (base2 / ".kilocode").mkdir()
    file2 = base2 / ".kilocode" / "rules" / "01.md"; file2.parent.mkdir(parents=True)
    file2.write_text("new")

    # set mtimes: file2 newer
    now = time.time()
    os.utime(file1, (now - 100, now - 100))
    os.utime(file2, (now, now))

    index = engine.scan_folders([base1, base2])

    # find the key for rules/01.md
    key = None
    for k in index:
        if k and k.endswith("rules/01.md"):
            key = k
            break
    assert key is not None

    actions = engine.plan_actions(index)
    assert len(actions) == 1
    act = actions[0]

    # source_path should be file2 (newer), destination file1
    assert str(act["source_path"]) == str(file2)
    assert str(act["destination_path"]) == str(file1)


# [Created-or-Modified] by gpt-5.2 | 2026-01-11_01
def test_plan_actions_respects_file_compare_threshold_seconds(tmp_path):
    """plan_actions should treat mtimes within threshold seconds as equal.

    The new behavior compares mtimes at whole-second granularity and only plans a
    copy when src is newer than dst by > file_compare_threshold_sec.
    """
    q = queue.Queue()
    config = {"ignore_patterns": [], "file_compare_threshold_sec": 2, "scaffold_folder": ".kilocode"}
    engine = SyncEngine(config, q)

    base1 = tmp_path / "p1"; base1.mkdir()
    (base1 / ".kilocode").mkdir()
    file1 = base1 / ".kilocode" / "rules" / "01.md"; file1.parent.mkdir(parents=True)
    file1.write_text("older")

    base2 = tmp_path / "p2"; base2.mkdir()
    (base2 / ".kilocode").mkdir()
    file2 = base2 / ".kilocode" / "rules" / "01.md"; file2.parent.mkdir(parents=True)
    file2.write_text("newer")

    # Make file2 only 2 seconds newer (== threshold) => no action
    now = time.time()
    os.utime(file1, (now, now))
    os.utime(file2, (now + 2, now + 2))

    index = engine.scan_folders([base1, base2])
    actions = engine.plan_actions(index)
    assert actions == []

    # Make file2 3 seconds newer (> threshold) => action expected
    os.utime(file2, (now + 3, now + 3))
    index2 = engine.scan_folders([base1, base2])
    actions2 = engine.plan_actions(index2)
    assert len(actions2) == 1

def test_execute_actions_performs_copy_backup_and_respects_dry_run(tmp_path):
    q = queue.Queue()
    # prepare two bases
    base1 = tmp_path / "s1"; base1.mkdir()
    (base1 / ".kilocode").mkdir()
    src = (base1 / ".kilocode" / "x.txt")
    src.write_text("SRC")

    base2 = tmp_path / "s2"; base2.mkdir()
    (base2 / ".kilocode").mkdir()
    dst = (base2 / ".kilocode" / "x.txt")
    dst.write_text("OLD")

    # set mtimes so src is newer than dst
    now = time.time()
    os.utime(src, (now, now))
    os.utime(dst, (now - 200, now - 200))

    # build index and actions with dry_run=True
    config = {"ignore_patterns": [], "dry_run": True, "backup_mode": "timestamped", "scaffold_folder": ".kilocode"}
    engine = SyncEngine(config, q)
    index = engine.scan_folders([base1, base2])
    actions = engine.plan_actions(index)

    # dry run: execute_actions should emit SKIP and not modify dst
    engine.execute_actions(actions)
    events = drain_queue(q)
    assert any(e.event_type == EventType.SKIP for e in events)
    assert dst.read_text() == "OLD"

    # now perform real copy with backup_mode timestamped
    q2 = queue.Queue()
    config2 = {"ignore_patterns": [], "dry_run": False, "backup_mode": "timestamped", "scaffold_folder": ".kilocode"}
    engine2 = SyncEngine(config2, q2)
    engine2.execute_actions(actions)
    evs = drain_queue(q2)
    assert any(e.event_type == EventType.COPY for e in evs)

    # dst should now equal src
    assert dst.read_text() == "SRC"

    # backup file should exist with a .bak suffix in the same parent directory
    backups = [p for p in dst.parent.iterdir() if p.name.startswith(dst.name) and ".bak" in p.name]
    assert len(backups) >= 1

# [Created-or-Modified] by tester | 2025-11-13_1
def test_append_allowlisted_root_file_to_index(tmp_path):
    """
    Test that allowlisted root files are appended to the index after scaffold dir is scanned.
    Validates that root_allowlist config includes specified files in the index with
    synthetic keys (just the filename) and that scaffold files continue to be indexed normally.
    """
    q = queue.Queue()
    # Configure with root_allowlist including .kilocodemodes
    config = {"ignore_patterns": [], "root_allowlist": [".kilocodemodes"], "scaffold_folder": ".kilocode"}
    engine = SyncEngine(config, q)

    # Create temporary project folder with .kilocode directory
    project = tmp_path / "project1"
    project.mkdir()
    scaffold_dir = project / ".kilocode"
    scaffold_dir.mkdir()

    # Add a file in .kilocode/docs for normal scanning
    docs_dir = scaffold_dir / "docs"
    docs_dir.mkdir()
    readme = docs_dir / "README.md"
    readme.write_text("# Documentation")

    # Add allowlisted root file
    modes_file = project / ".kilocodemodes"
    modes_file.write_text("mode1\nmode2\n")

    # Scan the folder
    index = engine.scan_folders([project])

    # Assert .kilocodemodes is in the index with synthetic key
    assert ".kilocodemodes" in index, "Allowlisted root file .kilocodemodes should be in index"
    assert len(index[".kilocodemodes"]) == 1, "Should have exactly one entry for .kilocodemodes"

    # Verify the path points to the actual root file
    modes_entry = index[".kilocodemodes"][0]
    assert modes_entry["path"] == modes_file, "Path should point to root .kilocodemodes file"
    assert modes_entry["base_folder"] == project

    # Assert scaffold files continue to be indexed normally
    assert any("docs/README.md" in k for k in index.keys()), "scaffold files should still be indexed"

    # Verify events were emitted
    events = drain_queue(q)
    assert any(e.event_type == EventType.SCAN_START for e in events)
    assert any(".kilocodemodes" in e.file_path for e in events if e.event_type == EventType.SCAN_FILE)

# [Created-or-Modified] by tester | 2025-11-13_1
def test_root_allowlist_safety_checks(tmp_path):
    """
    Test safety checks for root allowlist files:
    - Symlinks are not included
    - Directories are not included (only regular files)
    - Allowlist files are ignored if project lacks a real scaffold directory
    """
    import pytest
    q = queue.Queue()
    config = {"ignore_patterns": [], "root_allowlist": [".kilocodemodes", "config.txt"], "scaffold_folder": ".kilocode"}
    engine = SyncEngine(config, q)

    # Test case 1: Symlink should NOT be included
    project1 = tmp_path / "proj_symlink"
    project1.mkdir()
    (project1 / ".kilocode").mkdir()
    real_file = tmp_path / "real_modes.txt"
    real_file.write_text("real content")
    symlink_path = project1 / ".kilocodemodes"

    # Try to create symlink; skip if not supported on Windows
    try:
        symlink_path.symlink_to(real_file)
        index1 = engine.scan_folders([project1])
        assert ".kilocodemodes" not in index1, "Symlinks should NOT be included in index"
    except (OSError, NotImplementedError) as e:
        pytest.skip(f"Symlink creation not supported: {e}")

    # Test case 2: Directory should NOT be included (only regular files)
    project2 = tmp_path / "proj_directory"
    project2.mkdir()
    (project2 / ".kilocode").mkdir()
    dir_path = project2 / ".kilocodemodes"
    dir_path.mkdir()  # Create as directory, not file

    index2 = engine.scan_folders([project2])
    assert ".kilocodemodes" not in index2, "Directories should NOT be included in index"

    # Test case 3: No scaffold directory means allowlist files are NOT considered
    project3 = tmp_path / "proj_no_scaffold"
    project3.mkdir()
    # Do NOT create scaffold directory
    modes3 = project3 / ".kilocodemodes"
    modes3.write_text("should be ignored")

    index3 = engine.scan_folders([project3])
    assert ".kilocodemodes" not in index3, "Allowlist files should be ignored without scaffold directory"

    # Verify error event was emitted for missing scaffold dir
    events = drain_queue(q)
    assert any(e.event_type == EventType.ERROR and ".kilocode" in e.message
               for e in events), "Should emit error for missing scaffold directory"

    # Test case 4: Valid regular file IS included
    project4 = tmp_path / "proj_valid"
    project4.mkdir()
    (project4 / ".kilocode").mkdir()
    valid_file = project4 / "config.txt"
    valid_file.write_text("valid config")

    q4 = queue.Queue()
    engine4 = SyncEngine(config, q4)
    index4 = engine4.scan_folders([project4])
    assert "config.txt" in index4, "Valid regular files should be included"
    assert index4["config.txt"][0]["path"] == valid_file
