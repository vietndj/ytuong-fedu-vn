import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # intercept and see if it fails
        async def on_response(response):
            if "shot_01_mid.jpg" in response.url:
                print(f"Response: {response.url} - {response.status}")
                
        page.on("response", on_response)
        
        await page.goto("https://ytuong.fedu.vn")
        await page.evaluate("""
            let st = JSON.parse(localStorage.getItem('fedu_video_ideas_state') || '{}');
            st.curationMode = true;
            localStorage.setItem('fedu_video_ideas_state', JSON.stringify(st));
        """)
        await page.reload()
        await page.wait_for_timeout(3000)
        
        await browser.close()

asyncio.run(main())
