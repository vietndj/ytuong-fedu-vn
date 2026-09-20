import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.webkit.launch()
        page = await browser.new_page()
        page.on("console", lambda msg: print(f"Console {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"Page Error: {err}"))
        await page.goto("https://ytuong.fedu.vn", wait_until="networkidle")
        await page.screenshot(path="scratch/webkit_live_screenshot.png")
        await browser.close()

asyncio.run(main())
