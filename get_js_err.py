import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        def handle_error(err):
            print("=== PAGE ERROR ===")
            print(err.name, err.message)
            print(err.stack)
            
        page.on("pageerror", handle_error)
        
        await page.goto("https://ytuong.fedu.vn/reports/IG_@Chibuzor_Ossai_DdRGI36Aj0X_Carousel_Analysis")
        await page.wait_for_timeout(3000)
        await browser.close()

asyncio.run(main())
