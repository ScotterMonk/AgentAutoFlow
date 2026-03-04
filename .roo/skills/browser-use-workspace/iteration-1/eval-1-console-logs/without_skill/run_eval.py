"""
Eval 1 - WITHOUT SKILL: Capture console logs from localhost:5000
Naive/ad-hoc approach — no skill guidance.

Common mistakes without skill:
  - Console listener attached AFTER goto (misses early messages)
  - Uses networkidle (flaky)
  - No file output — just prints to stdout
  - No try/finally cleanup
  - Might attempt to manage the server unnecessarily
"""
import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate first — THEN attach listener (misses early console messages)
        try:
            await page.goto("http://localhost:5000", wait_until="networkidle", timeout=8000)
        except Exception as e:
            print(f"Error navigating: {e}")

        # Listener attached too late — already missed page load messages
        messages = []
        page.on("console", lambda msg: messages.append(f"{msg.type}: {msg.text}"))

        # Just print to stdout — not saved to file
        print("Console messages:", messages)
        print("Done")

        # No try/finally — browser left open if exception occurs above
        await browser.close()

asyncio.run(run())
