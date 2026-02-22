from pathlib import Path
from playwright.sync_api import sync_playwright

# Example: Capturing console logs during browser automation
# Output goes to outputs/ relative to current working directory (created automatically).

url = 'http://localhost:5173'  # Replace with your URL

# Ensure output directory exists (works on Windows and Linux)
Path('outputs').mkdir(parents=True, exist_ok=True)

console_logs = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})

    # Set up console log capture
    def handle_console_message(msg):
        console_logs.append(f"[{msg.type}] {msg.text}")
        print(f"Console: [{msg.type}] {msg.text}")

    page.on("console", handle_console_message)

    try:
        # Navigate to page; wait for a real element rather than networkidle (which is flaky)
        page.goto(url)
        page.wait_for_selector('body', timeout=10000)

        # Interact with the page (triggers console logs)
        page.click('text=Dashboard')
        page.wait_for_timeout(1000)

    finally:
        browser.close()

# Save console logs to file (relative path — works on Windows and Linux)
log_path = Path('outputs') / 'console.log'
log_path.write_text('\n'.join(console_logs), encoding='utf-8')

print(f"\nCaptured {len(console_logs)} console messages")
print(f"Logs saved to: {log_path}")