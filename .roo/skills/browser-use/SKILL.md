---
name: browser-use
description: Skill for web browser automation using Playwright for both local and external URLs. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
---

# Browser automation (Playwright)
Use native Python Playwright scripts to automate browsing and UI verification for any URL, including local development servers and external sites.

## Prerequisites
Ensure Playwright is installed (already listed in `requirements.txt`):
```powershell
py -m pip install playwright
playwright install chromium
```

**Helper scripts available** (all paths relative to project root):
- `{base folder}/.roo/skills/browser-use/scripts/with_server.py` - Optional. Manages local dev server lifecycle (supports multiple servers).

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is absolutely necessary. These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

**Output files**: Examples and scripts write screenshots/logs to an `outputs/` folder relative to the current working directory. The folder is created automatically if it does not exist.

## Decision tree: choosing your approach
```
User task → What is the target?
    ├─ Local HTML file (file://) → Read HTML file directly to identify selectors.
    │     ├─ Success → Write Playwright script using selectors.
    │     └─ Fails/Incomplete → Treat as dynamic (below).
    └─ URL (http/https) → Do you control the server process?
          ├─ Yes (local dev server) → Is it already running?
          │     ├─ No → Run: python .roo/skills/browser-use/scripts/with_server.py --help
          │     │        Then use the helper + write a simplified Playwright script.
          │     └─ Yes → Reconnaissance-then-action (below).
          └─ No (external site) → Reconnaissance-then-action (below).
```

## Example: using with_server.py (optional)
Use this only when you need to start and manage one or more local dev servers as part of automation.
`with_server.py` starts the server(s), waits until they are ready, runs your automation script, then cleans up. Run `--help` first before using it.

**Single server** (run from project root):
```powershell
python .roo/skills/browser-use/scripts/with_server.py --server "py app.py" --port 5000 -- python .roo/skills/browser-use/examples/basic_automation.py
```

**Multiple servers (e.g., backend + frontend)**:
```powershell
python .roo/skills/browser-use/scripts/with_server.py `
  --server "cd backend; python server.py" --port 3000 `
  --server "cd frontend; npm run dev" --port 5173 `
  -- python .roo/skills/browser-use/examples/basic_automation.py --url http://localhost:3000
```

Your automation script only needs Playwright logic — servers are managed automatically by `with_server.py`.
See `{base folder}/.roo/skills/browser-use/examples/basic_automation.py` for a robust, ready-to-use boilerplate.

## Reconnaissance-Then-Action Pattern
💡 **Tip for Users:** You can rapidly generate selectors and scripts by running `playwright codegen <url>` in your terminal.

1) **Inspect rendered DOM**.
    ```python
    page.screenshot(path='outputs/inspect.png', full_page=True)
    content = page.content()
    page.locator('button').all()
    ```
2) **Identify selectors** from inspection results.
3) **Execute actions** using discovered selectors.

## Common Pitfall
❌ **Don't** rely on `networkidle` as it is flaky on modern apps with background polling.
✅ **Do** wait for a specific element to be visible: `page.wait_for_selector('.main-content')` before inspection.
❌ **Don't** use Linux-only paths (`/tmp/`, `/mnt/`) in scripts — this project runs on Windows.
✅ **Do** use a relative `outputs/` directory (auto-created by examples).

## Best Practices
- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `{base folder}/.roo/skills/browser-use/scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly.
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done (use `try/finally`)
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` — not `networkidle`
- Output files go in a relative `outputs/` directory; create it with `Path('outputs').mkdir(parents=True, exist_ok=True)`

## Reference Files

All paths below are relative to the project root.

- **scripts/** - Helper scripts (call with `--help` first; do NOT read source):
  - `{base folder}/.roo/skills/browser-use/scripts/with_server.py` - Starts one or more local dev servers, runs your automation script, then cleans up

- **examples/** - Automation scripts (pass these to `with_server.py` or run standalone):
  - `{base folder}/.roo/skills/browser-use/examples/basic_automation.py` - Robust boilerplate with error handling and `wait_for_selector`
  - `{base folder}/.roo/skills/browser-use/examples/element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `{base folder}/.roo/skills/browser-use/examples/static_html_automation.py` - Using file:// URLs for local HTML
  - `{base folder}/.roo/skills/browser-use/examples/console_logging.py` - Capturing console logs during automation
