"""
Eval 0 - WITHOUT SKILL: Screenshot of example.com
Naive/ad-hoc approach — no skill guidance.

Common mistakes without skill:
  - Uses networkidle (flaky on modern apps)
  - No try/finally cleanup
  - Screenshot saved to cwd, not outputs/
  - No confirmation that heading was found
"""
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://example.com", wait_until="networkidle")

        # Take screenshot (saved to cwd, not outputs/)
        await page.screenshot(path="screenshot.png", full_page=True)
        print("Screenshot saved to screenshot.png")

        # No confirmation whether heading was found
        # No try/finally — cleanup only if no exception
        await browser.close()

asyncio.run(run())
