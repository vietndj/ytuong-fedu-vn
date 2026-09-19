import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        url = "file://" + os.path.abspath("index.html")
        print("Navigating to:", url)
        await page.goto(url)
        
        # Inject state
        await page.evaluate("""
            let st = JSON.parse(localStorage.getItem('fedu_video_ideas_state') || '{}');
            st.curationMode = true;
            localStorage.setItem('fedu_video_ideas_state', JSON.stringify(st));
        """)
        
        # Reload to apply Admin mode
        await page.reload()
        
        # Wait for data to load and render
        await page.wait_for_timeout(2000)
        
        # Click the India filter pill (we can just click by text)
        print("Clicking India tab...")
        await page.evaluate("""
            const indiaBtn = Array.from(document.querySelectorAll('.filter-pill')).find(el => el.textContent.includes('Ấn Độ'));
            if (indiaBtn) indiaBtn.click();
        """)
        
        await page.wait_for_timeout(1000)
        
        # Take screenshot
        screenshot_path = os.path.abspath("screenshot_admin_india.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        print("Saved screenshot to:", screenshot_path)
        
        # Also let's extract the text of the video titles to double check
        titles = await page.evaluate("""
            Array.from(document.querySelectorAll('.video-card')).map(card => {
                const titleEl = card.querySelector('h3');
                return titleEl ? titleEl.innerText : 'Unknown';
            })
        """)
        print("Rendered video titles:", titles)
        
        await browser.close()

asyncio.run(main())
