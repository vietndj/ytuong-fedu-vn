import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        errors = []
        page.on("console", lambda msg: errors.append(f"CONSOLE {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: errors.append(f"PAGE ERROR: {err}"))
        
        await page.goto("https://ytuong.fedu.vn/reports/IG_@Chibuzor_Ossai_DdRGI36Aj0X_Carousel_Analysis")
        await page.wait_for_timeout(3000)
        
        print("=== BÁO CÁO CONSOLE ===")
        for e in errors:
            print(e)
        
        await browser.close()

asyncio.run(main())
