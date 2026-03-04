---
name: coding-html
description: When html or jinja are being written or edited. Use this skill any time you are writing, editing, refactoring, or reviewing HTML (.html files or inline HTML) or Jinja2 templates. Trigger even for small HTML additions, new template blocks, editing existing template structure, or when a user says "update the layout", "fix the template", "add a section", or "edit the page".
---

# HTML / Jinja2 Coding Standards

## Syntax & Style
- **Quotes**: Enforce Double Quotes (`"`) over single quotes (`'`) for HTML attributes and Jinja expressions.
  - Good: `<input type="text" name="email">`
  - Bad: `<input type='text' name='email'>`
- **Spacing**: Keep vertical spacing compact — no excessive blank lines between elements.
- **Indentation**: 2 spaces per level for HTML and Jinja blocks.
- **Readability**: Prioritize readable, explicit markup over terse or clever one-liners.
- **Language mode**: Set VS Code language mode to `jinja-html` for template files.

## CSS
**Inline CSS**: Prefer classes from `.css` files over inline `style=""` attributes, unless explicitly justified (e.g., dynamic values injected by Python).

## JavaScript
**Inline JS**: Prefer referencing functions from `.js` files over inline `<script>` blocks or `onclick=""` attributes, unless explicitly justified.

## Jinja2 Templates
- Use `{% block %}` / `{% endblock %}` for template inheritance — don't duplicate layout HTML.
- Wrap long Jinja expressions in `{# comment #}` comments to document intent.
- Use `{{ var | default('') }}` to guard against undefined variable errors.
- Prefer `{% include %}` for reusable partials (e.g., nav, footer, modals).
- Keep business logic out of templates — pass pre-computed values from Python routes.

## Mandatory Metadata

**Preserve comments**: Do NOT delete existing, still-relevant comments.

**Every HTML section or Jinja block you create or significantly modify** must have a comment header:

```html
<!-- [Created-or-Modified] by [Model_Name] | YYYY-MM-DD_[Iteration] -->
```

Example: `<!-- Modified by Claude-3-7-Sonnet | 2026-03-04_01 -->`

Place the comment immediately above the relevant `<section>`, `<div>`, or `{% block %}`.

## Tooling Preference (Web)
Primary: Use `web browser`.
Fallback: `browser_action` (only if web browser is unavailable or fails).
