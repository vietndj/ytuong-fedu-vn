import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.webkit.launch()
        page = await browser.new_page()
        
        url = "file://" + os.path.abspath("test_onerror.html")
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        text = await page.evaluate("document.body.innerText")
        print("Result:", text)
        
        await browser.close()

asyncio.run(main())
