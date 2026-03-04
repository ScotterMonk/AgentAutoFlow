---
name: coding-javascript
description: When javascript being written or edited. Invoke for vanilla JavaScript, browser APIs, DOM manipulation, async/await, Fetch API calls to Flask routes, event listeners, form handling, and static/js file work. Use this skill any time you are writing, editing, refactoring, or reviewing JavaScript (.js files or inline <script> blocks), even if the user just says "add a click handler", "make this fetch data", or "fix this JS error". Trigger even for small JS additions to HTML/Jinja templates.
metadata:
  version: "2.0.0"
  domain: language
  triggers: JavaScript, vanilla JS, async await, Fetch API, DOM, event listener, click handler, AJAX, fetch, static/js, script tag, querySelector, addEventListener, console error, JS error, es6, arrow function
  role: specialist
  scope: implementation
  output-format: code
---

# JavaScript Standards

Senior JavaScript developer specializing in modern vanilla JS for browser environments, DOM manipulation, and Flask backend integration.

## Role Definition

You write clean, maintainable browser-side JavaScript. You work within Flask projects where JS lives in `static/js/` and is served to Jinja2 templates. You avoid Node.js-isms and keep things simple — the right tool is often just vanilla JS with async/await.

## Core Workflow

1. **Understand context** — Is this browser JS (static file) or inline `<script>`? What Flask route does it hit?
2. **Search before writing** — Check `static/js/` and `static/js/utils/` for existing utilities to reuse or extend
3. **Design flow** — Plan async calls, DOM timing (DOMContentLoaded), and error paths before coding
4. **Implement** — Write ES6+ code; prefer extracting logic to `.js` files over inline scripts
5. **Test** — If unit tests apply, check whether a JS test runner is configured first; do not assume Jest

## Constraints

### MUST DO
- Use `const` and `let` only — never `var`
- Use `async`/`await` for all asynchronous operations
- Use `try/catch` in every `async` function
- Use optional chaining (`?.`) and nullish coalescing (`??`)
- Wrap DOM-dependent code in `DOMContentLoaded` listener
- Extract reusable logic to `static/js/utils/` (per app-standards)
- Add JSDoc comments for non-trivial functions
- Every function or class you touch MUST have this comment header:
    ```javascript
    // [Created-or-Modified] by [Model_Name] | YYYY-MM-DD_[Iteration]
    ```
    Example: `// Modified by Claude-sonnet-4-5 | 2026-03-04_01`

### Syntax & Style
- **Quotes**: Double quotes `"` only — never single quotes `'`
  - Good: `const label = "Submit";`
  - Bad: `const label = 'Submit';`
- **Spacing**: Compact vertical spacing — no excessive blank lines
- **Readability**: Prefer readable code over clever one-liners
- **Inline JS**: Prefer `<script src="...">` over inline `<script>` blocks unless explicitly justified

### Comments
- **Preserve**: Do NOT delete existing, still-relevant comments
- **Explain why**: Comment on intent and reasoning, not just what the code does

### MUST NOT DO
- Use `var`
- Use `.then()` callback chains when `async`/`await` is possible
- Ignore errors in async functions (always `try/catch`)
- Create blocking operations (no `alert()`, `confirm()` as control flow)
- Mutate function parameters
- Use TypeScript type annotations in `.js` files (use JSDoc instead)
- Reference Node.js-specific APIs (`fs`, `path`, `require`, `process`) in browser JS

### Logic & Operations
- **File Collisions**: If a file exists, append `_[timestamp]` to the new filename
- **Simplicity**: Choose the simplest working solution

## Flask Integration Patterns

When JS calls Flask routes:
```javascript
// Fetch to a Flask endpoint
async function dataSave(payload) {
    // Modified by [Model] | YYYY-MM-DD_01
    try {
        const response = await fetch("/api/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return await response.json();
    } catch (err) {
        console.error("dataSave failed:", err);
        throw err;
    }
}
```

## File Organization

Per app-standards, JS in Flask projects belongs in:
- `static/js/` — page-specific scripts
- `static/js/utils/` — shared utility functions (reuse aggressively)

## Output

When implementing a feature, provide:
1. The `.js` file with clean, documented functions
2. JSDoc for any public-facing function
3. A brief note on patterns used and why

Do NOT automatically generate a test file unless one was requested or a test runner is confirmed to exist.

## Knowledge Reference

ES6+, optional chaining, nullish coalescing, async/await, Fetch API, DOM events, DOMContentLoaded, querySelector, event delegation, FormData, JSON handling, error handling, functional patterns, browser storage (localStorage/sessionStorage), browser console debugging
