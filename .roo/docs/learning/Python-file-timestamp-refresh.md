# Bulk “mtime refresh” safely (bytes-level edits + binary detection)

When you need to refresh modification times across many files (e.g., everything under `{base folder}/.roo/`), avoid text-mode rewrites that can accidentally change encodings, line endings, or otherwise churn content.

**Recommended pattern**:
- Read and write using **bytes** (e.g., `Path.read_bytes()` / `Path.write_bytes()`) so the file’s encoding is not re-interpreted.
- Use a small **binary detection heuristic** (e.g., presence of `\x00` or high ratio of non-text bytes in a sample) and **do not edit** binary files.
- For binary files, only update timestamps (e.g., `os.utime(path, None)`).

This preserves file integrity while still meeting the goal of updated mtimes.

