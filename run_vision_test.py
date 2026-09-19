import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # Navigate to the local server or index.html
        # We can serve it on a local python server or just open file://
        import os
        file_path = f"file://{os.path.abspath('index.html')}"
        print(f"Navigating to {file_path}")
        await page.goto(file_path)
        # Wait for network idle or a few seconds for images to load
        await page.wait_for_timeout(3000)
        # Capture screenshot
        await page.screenshot(path="vision_report.png", full_page=True)
        await browser.close()
        print("Screenshot saved to vision_report.png")

asyncio.run(main())
