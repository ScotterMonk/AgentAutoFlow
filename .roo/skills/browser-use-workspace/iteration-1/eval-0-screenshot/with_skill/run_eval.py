"""
Eval 0 - WITH SKILL: Screenshot of example.com
Following browser-use SKILL.md decision tree and best practices.

Decision tree:
  Target is URL (https://example.com) → external site → Reconnaissance-then-Action
  
Approach:
  1. Wait for specific element to be visible (not networkidle)
  2. Take full-page screenshot
  3. Confirm heading is found
  4. Use sync_playwright() + try/finally
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

# Output files go in outputs/ relative to cwd
OUTPUTS = Path("outputs")
OUTPUTS.mkdir(parents=True, exist_ok=True)

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            context = browser.new_context()
            page = context.new_page()

            # Navigate to target
            page.goto("https://example.com")

            # Wait for specific element — not networkidle (per SKILL.md best practice)
            page.wait_for_selector("h1", timeout=10000)

            # Reconnaissance: check what's on the page
            heading_el = page.locator("h1").first
            heading_text = heading_el.inner_text()

            # Take full-page screenshot
            screenshot_path = OUTPUTS / "example_screenshot.png"
            page.screenshot(path=str(screenshot_path), full_page=True)

            # Confirm heading found
            if "Example Domain" in heading_text:
                print(f"[PASS] Heading found: '{heading_text}'")
            else:
                print(f"[WARN] Unexpected heading: '{heading_text}'")

            print(f"Screenshot saved to: {screenshot_path}")

        finally:
            browser.close()

if __name__ == "__main__":
    run()
