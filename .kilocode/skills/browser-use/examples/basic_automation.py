#!/usr/bin/env python3
"""
Basic Playwright automation boilerplate.
Intended to be called via scripts/with_server.py after the local dev server is ready.

Usage (via with_server.py):
    python scripts/with_server.py --server "py app.py" --port 5000 -- python examples/basic_automation.py
    python scripts/with_server.py --server "py app.py" --port 5000 -- python examples/basic_automation.py --url http://localhost:5000/some-page

Usage (standalone external URL):
    python examples/basic_automation.py --url https://example.com
"""

import argparse
from playwright.sync_api import sync_playwright


def run_automation(url: str):
    """Run Playwright automation against the given URL."""
    with sync_playwright() as p:
        # Always launch chromium in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url)

            # Wait for a known element - prefer this over networkidle (which is flaky)
            page.wait_for_selector('body', timeout=10000)

            # --- Insert your automation logic below ---
            print(f"Successfully loaded: {url}")
            print(f"Page title: {page.title()}")
            # --- End automation logic ---

        except Exception as e:
            # Capture visual state on failure for debugging
            page.screenshot(path='error_state.png', full_page=True)
            print(f"Automation failed (screenshot saved to error_state.png): {e}")
            raise e

        finally:
            # Ensure browser process is always closed
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic Playwright automation script")
    parser.add_argument(
        "--url",
        default="http://localhost:5000",
        help="Target URL (default: http://localhost:5000)"
    )
    args = parser.parse_args()
    run_automation(args.url)
