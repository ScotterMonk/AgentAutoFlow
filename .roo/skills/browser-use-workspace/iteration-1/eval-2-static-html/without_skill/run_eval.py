"""
Eval 2 - WITHOUT SKILL: Element discovery on static HTML form
Naive/ad-hoc approach — no skill guidance.

Common mistakes without skill:
  - Skips the "read HTML file directly" step from decision tree
  - Uses http:// instead of file:// URL
  - No try/finally cleanup
  - No structured output saved to file
"""
import asyncio
from playwright.async_api import async_playwright

# Mistake: tries to serve via http instead of file://
# This would fail on a local file — should use file:// URL
TARGET_URL = "http://localhost/form.html"

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Uses http:// — wrong for local file (will fail or need a server)
        # Should use file:/// URL per SKILL.md decision tree
        try:
            await page.goto(TARGET_URL, wait_until="networkidle", timeout=5000)
        except Exception as e:
            print(f"Navigation failed (expected — wrong URL scheme): {e}")
            # No fallback to file:// URL
            await browser.close()
            return

        # No structured discovery — just prints raw element count
        inputs = await page.query_selector_all("input")
        buttons = await page.query_selector_all("button")
        print(f"Found {len(inputs)} inputs and {len(buttons)} buttons")

        # No output file saved
        # No try/finally
        await browser.close()

asyncio.run(run())
