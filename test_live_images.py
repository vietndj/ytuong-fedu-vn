import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        await page.goto("https://ytuong.fedu.vn")
        
        # Inject state to load all images
        await page.evaluate("""
            let st = JSON.parse(localStorage.getItem('fedu_video_ideas_state') || '{}');
            st.curationMode = true;
            localStorage.setItem('fedu_video_ideas_state', JSON.stringify(st));
        """)
        
        await page.reload()
        await page.wait_for_timeout(5000)
        
        # Scroll down to lazy load images
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(3000)
        
        # Find broken images
        broken = await page.evaluate("""
            Array.from(document.querySelectorAll('img')).filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src)
        """)
        
        print(f"Total broken images found on frontend: {len(broken)}")
        if broken:
            for b in broken[:20]:
                print(b)
            
        await browser.close()

asyncio.run(main())
