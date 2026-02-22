from pathlib import Path
from playwright.sync_api import sync_playwright

# Example: Automating interaction with static HTML files using file:// URLs
# Output goes to outputs/ relative to current working directory (created automatically).

html_file_path = Path('path/to/your/file.html').resolve()
file_url = html_file_path.as_uri()  # Produces file:///... (cross-platform)

# Ensure output directory exists (works on Windows and Linux)
Path('outputs').mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})

    try:
        # Navigate to local HTML file
        page.goto(file_url)
        page.wait_for_selector('body', timeout=10000)

        # Take screenshot
        page.screenshot(path='outputs/static_page.png', full_page=True)

        # Interact with elements
        page.click('text=Click Me')
        page.fill('#name', 'John Doe')
        page.fill('#email', 'john@example.com')

        # Submit form
        page.click('button[type="submit"]')
        page.wait_for_timeout(500)

        # Take final screenshot
        page.screenshot(path='outputs/after_submit.png', full_page=True)

    finally:
        browser.close()

print("Static HTML automation completed!")
print("Screenshots saved to outputs/static_page.png and outputs/after_submit.png")