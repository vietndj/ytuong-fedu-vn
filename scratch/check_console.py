import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Capture console messages
        page.on("console", lambda msg: print(f"Console {msg.type}: {msg.text}"))
        # Capture unhandled exceptions
        page.on("pageerror", lambda err: print(f"Page Error: {err}"))
        
        await page.goto("https://ytuong.fedu.vn", wait_until="networkidle")
        await browser.close()

asyncio.run(main())
