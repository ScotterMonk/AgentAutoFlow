# Created by gpt-5.2 | 2026-02-09_01
"""auto_fix_dates

Walks the local `.roo/` directory recursively and forces all files to have a
fresh modification time by making a minimal, semantics-preserving whitespace
change.

Rules implemented (per request):
- For `.md` files: append a single space to the very end of the file.
- For scripting-style files: add a single space to an existing comment line; if
  no comment is found, append a new comment line.
- For all other text-like files: append a single space to end of file.

If a file appears binary, the script will only `os.utime()` it (to avoid
corrupting binary content) while still meeting the goal of updating modified
times.
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class FixResult:
    """Per-file outcome."""

    path: Path
    action: str
    error: Optional[str] = None


# Created by gpt-5.2 | 2026-02-09_01
def _is_probably_binary(data: bytes) -> bool:
    """Heuristic to avoid editing binary files."""

    if not data:
        return False
    if b"\x00" in data:
        return True
    # If the first chunk has a high ratio of non-text bytes, treat as binary.
    sample = data[:4096]
    textish = b"\t\n\r" + bytes(range(32, 127))
    non_text = sum(1 for b in sample if b not in textish)
    return (non_text / max(1, len(sample))) > 0.25


# Created by gpt-5.2 | 2026-02-09_01
def _comment_prefix_for_suffix(suffix: str) -> Optional[bytes]:
    """Return a line-comment prefix for common scripting/text formats."""

    suffix = suffix.lower()
    if suffix in {".py", ".sh", ".bash", ".ps1", ".rb"}:
        return b"#"
    if suffix in {".js", ".ts", ".jsx", ".tsx", ".java", ".c", ".cc", ".cpp", ".h", ".hpp", ".cs", ".go"}:
        return b"//"
    if suffix in {".sql"}:
        return b"--"
    return None


# Created by gpt-5.2 | 2026-02-09_01
def _touch_now(path: Path) -> None:
    """Set mtime/atime to now."""

    os.utime(path, None)


# Created by gpt-5.2 | 2026-02-09_01
def _append_space_eof(path: Path, data: bytes) -> bytes:
    """Append a single space byte to end-of-file."""

    return data + b" "


# Created by gpt-5.2 | 2026-02-09_01
def _add_space_to_comment_line(path: Path, data: bytes, comment_prefix: bytes) -> bytes:
    """Add a single space to an existing comment line; otherwise append one."""

    # Work in bytes to avoid encoding changes.
    lines = data.splitlines(keepends=True)
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(comment_prefix):
            if line.endswith(b"\r\n"):
                lines[i] = line[:-2] + b" " + b"\r\n"
            elif line.endswith(b"\n"):
                lines[i] = line[:-1] + b" " + b"\n"
            else:
                lines[i] = line + b" "
            return b"".join(lines)

    # No existing comment found: add a new harmless comment line.
    newline = b"\r\n" if b"\r\n" in data else b"\n"
    if not data.endswith((b"\n", b"\r\n")) and data:
        data = data + newline
    return data + comment_prefix + b" " + newline


# Created by gpt-5.2 | 2026-02-09_01
def _fix_one_file(path: Path, *, dry_run: bool) -> FixResult:
    """Apply the requested minimal edit to a single file."""

    try:
        data = path.read_bytes()
    except Exception as e:
        return FixResult(path=path, action="read_failed", error=str(e))

    if _is_probably_binary(data):
        if not dry_run:
            try:
                _touch_now(path)
            except Exception as e:
                return FixResult(path=path, action="utime_failed", error=str(e))
        return FixResult(path=path, action="binary_utime")

    suffix = path.suffix.lower()
    if suffix == ".md":
        new_data = _append_space_eof(path, data)
        action = "md_append_space"
    else:
        comment_prefix = _comment_prefix_for_suffix(suffix)
        if comment_prefix is not None:
            new_data = _add_space_to_comment_line(path, data, comment_prefix)
            action = "script_comment_space"
        else:
            new_data = _append_space_eof(path, data)
            action = "append_space"

    if dry_run:
        return FixResult(path=path, action=f"dry_run:{action}")

    try:
        path.write_bytes(new_data)
        _touch_now(path)
        return FixResult(path=path, action=action)
    except Exception as e:
        return FixResult(path=path, action="write_failed", error=str(e))


# Created by gpt-5.2 | 2026-02-09_01
def _iter_roo_files(root: Path) -> Iterable[Path]:
    """Yield all files under `.roo/` recursively."""

    # Use rglob("*") to include all extensions and nested folders.
    for p in root.rglob("*"):
        if p.is_file():
            yield p


# Created by gpt-5.2 | 2026-02-09_01
def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Force .roo file mtimes to now via harmless whitespace edits")
    parser.add_argument("--root", default=".roo", help="Root folder to process (default: .roo)")
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without writing")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.exists() or not root.is_dir():
        print(f"ERROR: root folder not found or not a directory: {root}")
        return 2

    files = sorted(_iter_roo_files(root))
    if not files:
        print(f"No files found under: {root}")
        return 0

    results: list[FixResult] = []
    for f in files:
        results.append(_fix_one_file(f, dry_run=args.dry_run))

    failures = [r for r in results if r.error]
    print(f"Processed: {len(results)} files")
    print(f"Failures:  {len(failures)}")
    if failures:
        for r in failures:
            print(f"- {r.path}: {r.action}: {r.error}")
        return 1

    # Print a small sample of actions for confidence.
    sample = results[:10]
    for r in sample:
        print(f"- {r.path}: {r.action}")
    if len(results) > len(sample):
        print(f"... ({len(results) - len(sample)} more)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

