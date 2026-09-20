import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        url = "file://" + os.path.abspath("dist/index.html")
        await page.goto(url)
        
        # Inject state to load all images
        await page.evaluate("""
            let st = JSON.parse(localStorage.getItem('fedu_video_ideas_state') || '{}');
            st.curationMode = true;
            localStorage.setItem('fedu_video_ideas_state', JSON.stringify(st));
        """)
        
        await page.reload()
        await page.wait_for_timeout(3000)
        
        # Scroll down to lazy load images
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(2000)
        
        # Find broken images
        broken = await page.evaluate("""
            Array.from(document.querySelectorAll('img')).filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src)
        """)
        
        print(f"Total broken images found on frontend: {len(broken)}")
        if broken:
            print("First 5:", broken[:5])
            
        await browser.close()

asyncio.run(main())
