"""
Eval 1 - WITH SKILL: Capture console logs from localhost:5000
Following browser-use SKILL.md decision tree and best practices.

Decision tree:
  Target is URL (http://localhost:5000) → local dev server → already running?
  USER SAID YES (already running) → skip with_server.py → Reconnaissance-then-Action

Approach:
  1. Attach console listener BEFORE navigating (critical ordering)
  2. Do NOT manage server process (server is already running per prompt)
  3. Save messages to outputs/console_log.txt
  4. Use wait_for_selector (not networkidle)
  5. Use sync_playwright() + try/finally
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUTS = Path("outputs")
OUTPUTS.mkdir(parents=True, exist_ok=True)

def run():
    console_messages = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context()
            page = context.new_page()

            # Attach console listener BEFORE navigating — critical per SKILL.md
            def on_console(msg):
                entry = f"[{msg.type.upper()}] {msg.text}"
                console_messages.append(entry)
                print(entry)

            page.on("console", on_console)

            # Navigate to the already-running server (no with_server.py needed)
            try:
                page.goto("http://localhost:5000", timeout=8000)
                # Wait for a specific element — not networkidle
                page.wait_for_selector("body", timeout=5000)
            except Exception as nav_err:
                console_messages.append(f"[NAV-ERROR] Could not reach localhost:5000: {nav_err}")
                print(f"[NAV-ERROR] Server may not be running: {nav_err}")

            # Save console log to file
            log_path = OUTPUTS / "console_log.txt"
            with open(log_path, "w", encoding="utf-8") as f:
                if console_messages:
                    f.writelines(line + "\n" for line in console_messages)
                else:
                    f.write("[INFO] No console messages captured.\n")

            print(f"\nConsole log saved to: {log_path}")
            print(f"Total messages captured: {len(console_messages)}")

        finally:
            browser.close()

if __name__ == "__main__":
    run()
