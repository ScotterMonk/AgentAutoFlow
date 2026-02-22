from pathlib import Path
from playwright.sync_api import sync_playwright

# Example: Discovering buttons and other elements on a page
# Output goes to outputs/ relative to current working directory (created automatically).

# Ensure output directory exists (works on Windows and Linux)
Path('outputs').mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        # Navigate to page; wait for a real element rather than networkidle (which is flaky)
        page.goto('http://localhost:5173')
        page.wait_for_selector('body', timeout=10000)

        # Discover all buttons on the page
        buttons = page.locator('button').all()
        print(f"Found {len(buttons)} buttons:")
        for i, button in enumerate(buttons):
            text = button.inner_text() if button.is_visible() else "[hidden]"
            print(f"  [{i}] {text}")

        # Discover links
        links = page.locator('a[href]').all()
        print(f"\nFound {len(links)} links:")
        for link in links[:5]:  # Show first 5
            text = link.inner_text().strip()
            href = link.get_attribute('href')
            print(f"  - {text} -> {href}")

        # Discover input fields
        inputs = page.locator('input, textarea, select').all()
        print(f"\nFound {len(inputs)} input fields:")
        for input_elem in inputs:
            name = input_elem.get_attribute('name') or input_elem.get_attribute('id') or "[unnamed]"
            input_type = input_elem.get_attribute('type') or 'text'
            print(f"  - {name} ({input_type})")

        # Take screenshot for visual reference
        page.screenshot(path='outputs/page_discovery.png', full_page=True)
        print("\nScreenshot saved to outputs/page_discovery.png")

    finally:
        browser.close()