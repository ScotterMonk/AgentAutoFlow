"""
Eval 2 - WITH SKILL: Element discovery on static HTML file
Following browser-use SKILL.md decision tree and best practices.

Decision tree:
  Target is local HTML file (file://) → Read HTML file directly to identify selectors first
  If that succeeds → Write Playwright script using discovered selectors.
  (No server needed, no with_server.py)

Step 1: Read the HTML file directly (reconnaissance)
Step 2: Identify selectors from the file content
Step 3: Run Playwright using file:// URL to confirm/list elements
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUTS = Path("outputs")
OUTPUTS.mkdir(parents=True, exist_ok=True)

HTML_PATH = Path("C:/temp/form.html")
FILE_URL = HTML_PATH.as_uri()  # Produces file:///C:/temp/form.html

def run():
    # Step 1: Reconnaissance — read HTML file directly (per SKILL.md decision tree)
    if HTML_PATH.exists():
        html_content = HTML_PATH.read_text(encoding="utf-8")
        print(f"[Step 1] HTML file read directly: {len(html_content)} chars")
        print("HTML preview:\n", html_content[:300])
    else:
        print(f"[WARN] HTML file not found at {HTML_PATH}, will attempt file:// anyway")

    # Step 2: Use Playwright with file:// URL to dynamically discover all elements
    discovered = {"inputs": [], "buttons": [], "textareas": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(FILE_URL)

            # Wait for body — specific element wait, not networkidle
            page.wait_for_selector("body", timeout=5000)

            # Discover inputs
            inputs = page.locator("input").all()
            for el in inputs:
                inp_type = el.get_attribute("type") or "text"
                inp_id = el.get_attribute("id") or "(no id)"
                inp_name = el.get_attribute("name") or "(no name)"
                discovered["inputs"].append(f"<input type='{inp_type}' id='{inp_id}' name='{inp_name}'>")

            # Discover textareas
            textareas = page.locator("textarea").all()
            for el in textareas:
                ta_id = el.get_attribute("id") or "(no id)"
                ta_name = el.get_attribute("name") or "(no name)"
                discovered["textareas"].append(f"<textarea id='{ta_id}' name='{ta_name}'>")

            # Discover buttons
            buttons = page.locator("button").all()
            for el in buttons:
                btn_type = el.get_attribute("type") or "button"
                btn_id = el.get_attribute("id") or "(no id)"
                btn_text = el.inner_text()
                discovered["buttons"].append(f"<button type='{btn_type}' id='{btn_id}'>{btn_text}</button>")

        finally:
            browser.close()

    # Step 3: Report findings
    report_lines = [
        "=== Element Discovery Report ===",
        f"Source: {FILE_URL}",
        "",
        f"INPUTS ({len(discovered['inputs'])}):",
        *[f"  {x}" for x in discovered["inputs"]],
        "",
        f"TEXTAREAS ({len(discovered['textareas'])}):",
        *[f"  {x}" for x in discovered["textareas"]],
        "",
        f"BUTTONS ({len(discovered['buttons'])}):",
        *[f"  {x}" for x in discovered["buttons"]],
    ]
    report = "\n".join(report_lines)
    print("\n" + report)

    report_path = OUTPUTS / "element_discovery.txt"
    report_path.write_text(report, encoding="utf-8")
    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    run()
