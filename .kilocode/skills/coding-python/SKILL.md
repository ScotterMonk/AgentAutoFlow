---
name: coding-python
description: When python, flask, or jinja are being written or edited. Use this skill any time you are writing, editing, refactoring, or reviewing Python (.py), Flask routes/blueprints, or Jinja2 templates (.html with Jinja). Trigger even if the user only mentions a .py file, a Flask endpoint, a template, or asks about Python patterns, imports, error handling, or structure.
---

# Python Coding Standards

## Mandatory Metadata
Every function or class you **create or modify** must include this header comment:
```python
# Created by [Model_Name] | YYYY-MM-DD
# Example: # Created by Claude-Sonnet-4.5 | 2025-03-04
```
For modifications to existing functions/classes:
```python
# Modified by [Model_Name] | YYYY-MM-DD
# Example: # Modified by Claude-Sonnet-4.5 | 2025-03-04
```
Use the current model name from context and today's date.

## Syntax & Style

### Quotes
- Use **double quotes** (`"`) in all cases.
  - Good: `x += "."`
  - Bad: `x += '.'`

### String Formatting
- Use **f-strings** for interpolation (not `%` or `.format()`).
  - Good: `f"Hello, {name}!"`
  - Bad: `"Hello, {}!".format(name)` or `"Hello, %s" % name`

### SQL
- Always use **multi-line triple-quoted strings** for SQL queries.

### Readability
- Prioritize readable code over clever/compact one-liners.
- Keep vertical spacing compact — no excessive blank lines.

### Type Hints
- Add type hints to new functions you write (not required when modifying existing code without type hints).
  ```python
  def user_get(user_id: int) -> dict:
  ```

## Imports
Organize imports in this order (one blank line between groups):
1. Standard library (`os`, `sys`, `datetime`, etc.)
2. Third-party libraries (`flask`, `pytest`, etc.)
3. Local/project modules

```python
import os
import sys

from flask import Flask, request, jsonify

from utils_sync.config_sync import config_load
```

## Error Handling
- Use specific exception types — avoid bare `except:`.
- Log errors with context before re-raising or returning.
  ```python
  try:
      result = file_read(path)
  except FileNotFoundError as e:
      logger.error(f"File not found: {path} — {e}")
      raise
  ```

## Docstrings
- Add a one-line docstring to every new public function or class.
- Use triple double-quotes.
  ```python
  def user_sync(folders: list) -> bool:
      """Sync .roo directories across all provided folder paths."""
  ```

---

## Flask-Specific Patterns

### Route Organization
- Keep route handlers thin — delegate logic to utility functions.
- Group related routes into blueprints (`blueprints/` folder).
- Route naming: use domain-first (e.g., `/user/edit`, not `/edit_user`).

### Error Handlers
- Register global error handlers in the app factory, not inline.
  ```python
  @app.errorhandler(404)
  def error_not_found(e):
      return jsonify({"error": "Not found"}), 404
  ```

### Response Pattern
- Use `jsonify()` for all API responses; set explicit status codes.

---

## Jinja2-Specific Patterns

### Template Language Mode
- Set file language mode to `jinja-html` for `.html` template files.

### Template Inheritance
- All page templates should extend a base layout:
  ```jinja
  {% extends "base.html" %}
  {% block content %}
    {# page content here #}
  {% endblock %}
  ```

### Variable Safety
- Use the `| default()` filter when a variable might be undefined:
  ```jinja
  {{ user.name | default("Guest") }}
  ```

### Logic in Templates
- Keep logic minimal in templates — complex logic belongs in Python, not Jinja.
- Use `{% set %}` for local variables rather than inline expressions when readability suffers.

---

## Testing (pytest)
- Test files live in `tests/` and follow `test_[module_name].py` naming.
- Each test function name describes what it verifies: `test_user_sync_creates_backup`.
- Use `tmp_path` fixture for file system tests — never write to real project paths.
- Confirm a test doesn't already exist before writing a new one.
