---
name: coding-html
description: When html or jinja are being written or edited.
---

# HTML coding standards

## Syntax & Style
Spacing: Keep vertical spacing compact (no excessive blank lines).
Readability: Prioritize readable code over "clever" one-liners.

## CSS
**In-line css**: Prefer use of classes from .css files to in-line css, unless explicitely justified.

## JS
**In-line js**: Prefer including and referencing from functions in .js files to in-line js, unless explicitly justified.

## Mandatory metadata

**Preserve comments**: Do NOT delete existing, still relevant comments.

**Every** function or class you touch MUST have this comment header:
For JavaScript:
```javascript
// [Created-or-Modified] by [Model_Name] | YYYY-MM-DD_[Iteration]
```
Example: `// Modified by Claude-4.5-Sonnet | 2025-11-27_01`

For Jinja/HTML comments:
```html
<!-- [Created-or-Modified] by [Model_Name] | YYYY-MM-DD_[Iteration] -->
```

## Syntax & Style
Quotes: Enforce Double Quotes (") over Single Quotes (').
Good: `const msg = "Hello";`
Bad: `const msg = 'Hello';`
Templates: Set language mode to jinja-html.
Spacing: Keep vertical spacing compact (no excessive blank lines).
Readability: Prioritize Readable Code over "clever" one-liners.

## Tooling Preference (Web)
Primary: browser_action (ALWAYS try this first).
Fallback: Other browser tools (Only if browser_action fails).
