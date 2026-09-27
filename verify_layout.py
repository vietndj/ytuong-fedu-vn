import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://localhost:8000/reports/IG_@Chibuzor_Ossai_DdRGI36Aj0X_Carousel_Analysis.html")
        await page.wait_for_timeout(3000)

        # Trích xuất thông tin Bounding Box để đo kích thước thực tế
        data = await page.evaluate("""
            () => {
                const wrap = document.querySelector('.video-wrap');
                const stack = document.querySelector('.carousel-stack');
                if (!stack || !wrap) return { error: 'Elements not found' };
                
                const wrapRect = wrap.getBoundingClientRect();
                const stackRect = stack.getBoundingClientRect();
                
                const children = Array.from(stack.children).map((el, i) => {
                    const rect = el.getBoundingClientRect();
                    return {
                        tag: el.tagName,
                        index: i,
                        height: rect.height,
                        width: rect.width,
                        top: rect.top,
                        isVisible: rect.height > 0 && rect.width > 0,
                        display: window.getComputedStyle(el).display
                    };
                });
                
                return {
                    wrap_height: wrapRect.height,
                    stack_height: stackRect.height,
                    stack_overflow_y: window.getComputedStyle(stack).overflowY,
                    children: children
                };
            }
        """)
        print(data)
        await page.screenshot(path="verify_chibuzor.png", full_page=False)
        await browser.close()

asyncio.run(main())
