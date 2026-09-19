import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        url = "file://" + os.path.abspath("index.html")
        await page.goto(url)
        
        # Inject state
        await page.evaluate("""
            let st = JSON.parse(localStorage.getItem('fedu_video_ideas_state') || '{}');
            st.curationMode = true;
            localStorage.setItem('fedu_video_ideas_state', JSON.stringify(st));
        """)
        
        await page.reload()
        await page.wait_for_timeout(2000)
        
        # Extract all x-factors
        xf = await page.evaluate("""
            Array.from(document.querySelectorAll('.xf-pill')).map(el => el.innerText.replace(/\\n/g, ' '))
        """)
        print("X-factors found:", xf)
        
        await browser.close()

asyncio.run(main())
