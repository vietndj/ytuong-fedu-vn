import asyncio
from playwright.async_api import async_playwright
import json

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()
        
        print("Navigating to production URL...")
        await page.goto('https://ytuong.fedu.vn', wait_until='networkidle')
        await page.evaluate("localStorage.setItem('fedu_admin_auth', '1')")
        await page.reload(wait_until='networkidle')
        await page.wait_for_timeout(2000)
        
        print("Clicking edit button...")
        await page.wait_for_selector('button[onclick^="openEditIdeaModal"]', timeout=10000)
        await page.click('button[onclick^="openEditIdeaModal"]')
        await page.wait_for_selector('#editIdeaModal.open', timeout=5000)
        await page.wait_for_timeout(1000)
        
        print("Selecting 'other' industry to show input...")
        # scroll to the bottom of the modal so the dropdown is visible
        await page.evaluate("document.querySelector('#editIdeaAiIndustry').scrollIntoView()")
        await page.select_option('#editIdeaAiIndustry', 'other')
        await page.wait_for_timeout(500)
        
        print("Taking Desktop screenshot...")
        await page.screenshot(path='vision_report_desktop.png')
        await context.close()
        
        # Test Mobile (iPhone 13)
        context_mobile = await browser.new_context(
            viewport={'width': 390, 'height': 844},
            is_mobile=True,
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
        )
        page_mobile = await context_mobile.new_page()
        
        print("Mobile: Navigating...")
        await page_mobile.goto('https://ytuong.fedu.vn', wait_until='networkidle')
        await page_mobile.evaluate("localStorage.setItem('fedu_admin_auth', '1')")
        await page_mobile.reload(wait_until='networkidle')
        await page_mobile.wait_for_timeout(2000)
        
        print("Mobile: Clicking edit...")
        await page_mobile.wait_for_selector('button[onclick^="openEditIdeaModal"]', timeout=10000)
        await page_mobile.click('button[onclick^="openEditIdeaModal"]')
        await page_mobile.wait_for_selector('#editIdeaModal.open', timeout=5000)
        await page_mobile.wait_for_timeout(1000)
        
        print("Mobile: Selecting 'other'...")
        await page_mobile.evaluate("document.querySelector('#editIdeaAiIndustry').scrollIntoView()")
        await page_mobile.select_option('#editIdeaAiIndustry', 'other')
        await page_mobile.wait_for_timeout(500)
        
        print("Mobile: Taking screenshot...")
        await page_mobile.screenshot(path='vision_report_mobile.png')
        
        await context_mobile.close()
        
        await browser.close()
        print("Done.")

asyncio.run(run())
