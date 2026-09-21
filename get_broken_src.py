import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        await page.goto("https://ytuong.fedu.vn")
        await page.wait_for_timeout(3000)
        
        srcs = await page.evaluate("""
            Array.from(document.querySelectorAll('img')).map(img => img.src)
        """)
        
        print("All image srcs (first 20):")
        for src in srcs[:20]:
            print(src)
            
        await browser.close()

asyncio.run(main())
