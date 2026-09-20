import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 390, 'height': 844}, user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1')
        await page.goto("https://ytuong.fedu.vn", wait_until="networkidle")
        # Scroll down by 800px
        await page.evaluate('window.scrollBy(0, 800)')
        await page.wait_for_timeout(500)
        await page.screenshot(path="scratch/live_mobile_screenshot_scroll.png")
        await browser.close()

asyncio.run(main())
