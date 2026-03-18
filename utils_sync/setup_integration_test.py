# Created by claude-sonnet-4-5 | 2025-11-13_1
# [Modified] by claude-sonnet-4.6 | 2026-03-18_01
"""
Setup script for integration testing of the file sync utility.
Creates test directories and files with controlled timestamps.

The scaffold folder name is read from config.txt (scaffold_folder key),
defaulting to ".kilocode" if not found.
"""
import os
import sys
import time
from pathlib import Path

# Allow running this script from any working directory by adjusting the import path.
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils_sync.config_sync import load_config


def setup_integration_test(scaffold_folder: str = None):
    """Create test environment for integration testing.

    Args:
        scaffold_folder: Name of the scaffold subdirectory (e.g. ".kilocode").
                         If None, reads from config.txt via load_config().
    """
    # Resolve scaffold folder from config if not explicitly provided
    if scaffold_folder is None:
        config = load_config()
        scaffold_folder = config.get("scaffold_folder", ".kilocode")

    # Create root test directory
    test_root = Path("test_integration")
    test_root.mkdir(exist_ok=True)

    # Create project directories
    project_a = test_root / "project_a"
    project_b = test_root / "project_b"

    project_a.mkdir(exist_ok=True)
    project_b.mkdir(exist_ok=True)

    # Create scaffold subdirectories (name driven by config)
    scaffold_a = project_a / scaffold_folder
    scaffold_b = project_b / scaffold_folder

    scaffold_a.mkdir(exist_ok=True)
    scaffold_b.mkdir(exist_ok=True)

    # Create test file in project_a (source - newer)
    file_a = scaffold_a / "file.txt"
    file_a.write_text("Content from project_a - This is the newer version")

    # Wait a moment to ensure timestamp difference
    time.sleep(0.1)

    # Create test file in project_b (destination - older)
    file_b = scaffold_b / "file.txt"
    file_b.write_text("Content from project_b - This is the older version")

    # Explicitly set older mtime for project_b file
    old_time = time.time() - 3600  # 1 hour ago
    os.utime(file_b, (old_time, old_time))

    # Verify setup
    print(f"Integration test environment created (scaffold_folder={scaffold_folder!r}):")
    print(f"  {project_a} - Created")
    print(f"  {project_b} - Created")
    print(f"  {file_a} - Created (newer)")
    print(f"  {file_b} - Created (older)")
    print(f"\nFile timestamps:")
    print(f"  project_a file mtime: {os.path.getmtime(file_a)}")
    print(f"  project_b file mtime: {os.path.getmtime(file_b)}")
    print(f"\nReady for integration testing!")


if __name__ == "__main__":
    setup_integration_test()