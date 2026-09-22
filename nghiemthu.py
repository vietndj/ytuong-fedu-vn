from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        page = browser.new_page()
        
        url = "https://ytuong.fedu.vn/reports/IG_@UME_%F0%9F%93%8D%D0%BC%D0%B8%D0%BD%D1%81%D0%BA-%D0%BC%D0%B8%D1%80_DcVnyJyNWGY_Video_by_ume.izakaya.html"
        page.on("console", lambda msg: print(f"Console: {msg.text}"))
        page.on("pageerror", lambda err: print(f"PageError: {err}"))
        page.goto(url, wait_until="networkidle")
        time.sleep(5)
        
        # Take screenshot
        page.screenshot(path="nghiemthu_report.png", full_page=True)
        
        # Check video state
        video_info = page.evaluate("""() => {
            const vid = document.getElementById('mainPlayer');
            if (!vid) return 'No video element';
            return {
                src: vid.src,
                readyState: vid.readyState,
                error: vid.error ? vid.error.code : null,
                networkState: vid.networkState,
                duration: vid.duration
            };
        }""")
        print(f"Video Info: {video_info}")
        
        browser.close()

run()
