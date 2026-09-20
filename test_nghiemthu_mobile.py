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
        
        # 1. Chụp màn hình trang chủ xem filter đã ẩn chưa
        await page.screenshot(path="nghiemthu_step1_home.png")
        
        # 2. Mở bộ lọc nếu có nút
        filter_btn = page.locator("text=Bộ Lọc")
        if await filter_btn.count() > 0:
            await filter_btn.first.click()
            await page.wait_for_timeout(1000)
            await page.screenshot(path="nghiemthu_step2_filter_opened.png")
            
        # 3. Mở một video/idea modal
        idea_card = page.locator(".idea-card").first
        if await idea_card.count() > 0:
            await idea_card.click()
            await page.wait_for_timeout(1500)
            await page.screenshot(path="nghiemthu_step3_modal_opened.png")
            
            # Click nút Tải Về
            download_btn = page.locator("text=Tải Về")
            if await download_btn.count() > 0:
                await download_btn.first.click()
                await page.wait_for_timeout(500)
                await page.screenshot(path="nghiemthu_step4_download_clicked.png")
                
            # Click ra ngoài / Click X để tắt
            close_btn = page.locator("button:has-text('✕')").first
            if await close_btn.count() > 0:
                await close_btn.click()
            else:
                # click ngoài
                await page.mouse.click(10, 10)
                
            await page.wait_for_timeout(1000)
            await page.screenshot(path="nghiemthu_step5_modal_closed.png")
            
        await browser.close()
        print("Đã hoàn tất kịch bản chụp ảnh Playwright.")

asyncio.run(run())
