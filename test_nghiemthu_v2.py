import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        iphone_13 = p.devices['iPhone 13']
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(**iphone_13)
        page = await context.new_page()
        
        file_path = f"file://{os.path.abspath('index.html')}"
        await page.goto(file_path)
        await page.wait_for_timeout(2000)
        
        # 1. Chụp màn hình trang chủ xem Logo ẩn chưa và Accordion thu gọn
        await page.screenshot(path="nghiemthu_v2_home_closed.png")
        
        # 2. Click mở Accordion "Menu & Bộ lọc"
        summary = page.locator("summary").first
        if await summary.count() > 0:
            await summary.click()
            await page.wait_for_timeout(1000)
            await page.screenshot(path="nghiemthu_v2_menu_opened.png")
            
        # 3. Mở Video Modal
        idea_card = page.locator(".idea-card").first
        if await idea_card.count() > 0:
            await idea_card.click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path="nghiemthu_v2_modal_opened.png")
            
        await browser.close()
        print("Đã chụp xong các ảnh Playwright Mắt Thần.")

asyncio.run(run())
