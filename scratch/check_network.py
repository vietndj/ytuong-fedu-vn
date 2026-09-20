import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        failed_requests = []
        page.on("response", lambda response: failed_requests.append(response) if response.status >= 400 else None)
        page.on("requestfailed", lambda request: print(f"Request failed: {request.url}"))
        
        await page.goto("https://ytuong.fedu.vn", wait_until="networkidle")
        for req in failed_requests:
            print(f"Failed HTTP {req.status}: {req.url}")
            
        await browser.close()

asyncio.run(main())
