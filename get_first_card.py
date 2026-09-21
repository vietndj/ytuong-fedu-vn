import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        await page.goto("https://ytuong.fedu.vn")
        await page.evaluate("""
            let st = JSON.parse(localStorage.getItem('fedu_video_ideas_state') || '{}');
            st.curationMode = true;
            localStorage.setItem('fedu_video_ideas_state', JSON.stringify(st));
        """)
        await page.reload()
        await page.wait_for_timeout(3000)
        
        srcs = await page.evaluate("""
            Array.from(document.querySelectorAll('#ideasCardsGrid img')).map(img => img.src)
        """)
        for src in srcs[:5]:
            print(src)
        
        await browser.close()

asyncio.run(main())
