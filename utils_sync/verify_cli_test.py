# Created by claude-sonnet-4-5 | 2025-11-13_1
# [Modified] by claude-sonnet-4.6 | 2026-03-18_01
"""
Verification script for CLI integration test results.
Checks file content, timestamps, and backup creation.

The scaffold folder name is read from config.txt (scaffold_folder key),
defaulting to ".kilocode" if not found.
"""
import os
import sys
from pathlib import Path

# Allow running this script from any working directory by adjusting the import path.
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils_sync.config_sync import load_config


def verify_cli_test(scaffold_folder: str = None):
    """Verify the results of the CLI integration test.

    Args:
        scaffold_folder: Name of the scaffold subdirectory (e.g. ".kilocode").
                         If None, reads from config.txt via load_config().
    """
    # Resolve scaffold folder from config if not explicitly provided
    if scaffold_folder is None:
        config = load_config()
        scaffold_folder = config.get("scaffold_folder", ".kilocode")

    print("=== CLI Integration Test Verification ===\n")
    print(f"Using scaffold_folder: {scaffold_folder!r}\n")

    # File paths (resolved via config scaffold_folder)
    file_a = Path(f"test_integration/project_a/{scaffold_folder}/file.txt")
    file_b = Path(f"test_integration/project_b/{scaffold_folder}/file.txt")
    backup_dir = Path(f"test_integration/project_b/{scaffold_folder}")
    
    # Check files exist
    if not file_a.exists():
        print("❌ FAIL: Source file does not exist")
        return False
    if not file_b.exists():
        print("❌ FAIL: Destination file does not exist")
        return False
    
    print("✓ Both files exist")
    
    # Check content matches
    content_a = file_a.read_text()
    content_b = file_b.read_text()
    
    print(f"\nSource content: {content_a[:50]}...")
    print(f"Dest content: {content_b[:50]}...")
    
    if content_a == content_b:
        print("✓ File contents match")
    else:
        print("❌ FAIL: File contents do not match")
        return False
    
    # Check backup file was created (.bak extension)
    backup_files = list(backup_dir.glob("*.bak"))
    if backup_files:
        print(f"✓ Backup file created: {backup_files[0].name}")
        backup_content = backup_files[0].read_text()
        print(f"  Backup content: {backup_content[:50]}...")
    else:
        print("❌ FAIL: No backup file found")
        return False
    
    # Check timestamps
    mtime_a = os.path.getmtime(file_a)
    mtime_b = os.path.getmtime(file_b)
    
    print(f"\nTimestamps:")
    print(f"  Source: {mtime_a}")
    print(f"  Dest: {mtime_b}")
    
    if mtime_b >= mtime_a - 1:  # Allow 1 second tolerance
        print("✓ Destination timestamp updated correctly")
    else:
        print("⚠ Warning: Destination timestamp may not be updated")
    
    print("\n=== CLI Integration Test: PASSED ===")
    return True

if __name__ == "__main__":
    verify_cli_test()