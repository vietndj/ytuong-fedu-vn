import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("https://ytuong.fedu.vn/reports/IG_@Chibuzor_Ossai_DdRGI36Aj0X_Carousel_Analysis")
        await page.wait_for_timeout(3000)
        await page.screenshot(path="live_proof.png", full_page=False)
        await browser.close()

asyncio.run(main())
