---
name: browser-use
description: Skill for web browser automation using Playwright for both local and external URLs. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
---

# Browser automation (Playwright)
Use native Python Playwright scripts to automate browsing and UI verification for any URL, including local development servers and external sites.

**Helper scripts available**:
- `scripts/with_server.py` - Optional. Manages local dev server lifecycle (supports multiple servers).

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is abslutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

## Decision tree: choosing your approach
```
User task → What is the target?
    ├─ Local HTML file (file://) → Read HTML file directly to identify selectors.
    │     ├─ Success → Write Playwright script using selectors.
    │     └─ Fails/Incomplete → Treat as dynamic (below).
    └─ URL (http/https) → Do you control the server process?
          ├─ Yes (local dev server) → Is it already running?
          │     ├─ No → Run: python scripts/with_server.py --help.
          │     │        Then use the helper + write a simplified Playwright script.
          │     └─ Yes → Reconnaissance-then-action (below).
          └─ No (external site) → Reconnaissance-then-action (below).
```

## Example: using with_server.py (optional)
Use this only when you need to start and manage one or more local dev servers as part of automation.
To start a server, run `--help` first, then use the helper.

**Single server**:
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend)**:
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically).
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Example local URL
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Example: external URL
Use the same Playwright code for remote browsing; only the URL changes.
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://example.com')
    page.wait_for_load_state('networkidle')
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern
1) **Inspect rendered DOM**.
    ```python
    page.screenshot(path='/tmp/inspect.png', full_page=True)
    content = page.content()
    page.locator('button').all()
    ```
2) **Identify selectors** from inspection results.
3) **Execute actions** using discovered selectors.

## Common Pitfall
❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices
- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference Files

- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation
