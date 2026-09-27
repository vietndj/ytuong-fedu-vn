import asyncio
from playwright.async_api import async_playwright
import sys

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://localhost:8000/reports/IG_@Chibuzor_Ossai_DdRGI36Aj0X_Carousel_Analysis.html")
        await page.wait_for_timeout(2000)
        await page.screenshot(path="screenshot_chibuzor.png", full_page=False)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
