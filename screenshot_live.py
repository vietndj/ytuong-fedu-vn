from playwright.sync_api import sync_playwright
import time

def take_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        # bypass cache
        page.set_extra_http_headers({'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
        page.goto('https://ytuong.fedu.vn', wait_until='networkidle')
        time.sleep(3)
        page.screenshot(path='/Users/vietmac/.gemini/antigravity/brain/35f8baf8-7e5e-4d40-8360-340eadc1c9c2/ytuong_live_screenshot_final.png', full_page=True)
        print("Screenshot saved to /Users/vietmac/.gemini/antigravity/brain/35f8baf8-7e5e-4d40-8360-340eadc1c9c2/ytuong_live_screenshot_final.png")
        browser.close()

take_screenshot()
