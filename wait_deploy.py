import time
import sys
from playwright.sync_api import sync_playwright

def wait_and_screenshot():
    for _ in range(15):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={'width': 1280, 'height': 800})
                page.set_extra_http_headers({'Cache-Control': 'no-cache'})
                page.goto('https://ytuong.fedu.vn', wait_until='networkidle')
                time.sleep(3)
                js_content = page.evaluate('JSON.stringify(window.ALL_IDEAS || [])')
                if 'hook treo máy thẳng đứng' in js_content or 'Bán phong cách sống' in js_content:
                    print("[SUCCESS] Cloudflare updated!")
                    page.screenshot(path='/Users/vietmac/.gemini/antigravity/brain/35f8baf8-7e5e-4d40-8360-340eadc1c9c2/ytuong_live_screenshot_success.png', full_page=True)
                    browser.close()
                    sys.exit(0)
                browser.close()
        except Exception as e:
            pass
        print("Waiting 10s for Cloudflare build...")
        time.sleep(10)
    print("Failed")
    sys.exit(1)

wait_and_screenshot()
