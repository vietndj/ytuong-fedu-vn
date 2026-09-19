import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile viewport (iPhone 12/13 size)
        page = await browser.new_page(viewport={"width": 390, "height": 844})
        
        url = "file://" + os.path.abspath("index.html")
        print("Navigating to:", url)
        await page.goto(url)
        
        # Wait for data to load and render
        await page.wait_for_timeout(2000)
        
        # Open the first video
        print("Opening video modal...")
        await page.evaluate("""
            if (typeof FEDU_IDEAS_DATABASE !== 'undefined' && FEDU_IDEAS_DATABASE.ideas.length > 0) {
                openVideoModal(FEDU_IDEAS_DATABASE.ideas[0].id);
            }
        """)
        
        await page.wait_for_timeout(1000)
        
        # Take screenshot of the modal
        screenshot_path = os.path.abspath("screenshot_mobile_modal.png")
        await page.screenshot(path=screenshot_path)
        print("Saved screenshot to:", screenshot_path)
        
        await browser.close()

asyncio.run(main())
