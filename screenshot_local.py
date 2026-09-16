from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto('http://localhost:8000', wait_until='networkidle')
    time.sleep(3)
    page.screenshot(path='/Users/vietmac/.gemini/antigravity/brain/35f8baf8-7e5e-4d40-8360-340eadc1c9c2/ytuong_local_screenshot.png', full_page=True)
    browser.close()
