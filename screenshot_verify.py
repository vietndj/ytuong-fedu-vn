from playwright.sync_api import sync_playwright
import time

def verify_site():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        print("Navigating to https://ytuong.fedu.vn...")
        page.goto("https://ytuong.fedu.vn", wait_until="networkidle")
        
        # Wait a bit for JS to render ideas
        page.wait_for_selector('.idea-card', timeout=10000)
        time.sleep(3) # Extra wait for masonry/images
        
        # Search for one of the new texts to see if it's there
        content = page.content()
        if "Dùng hook treo máy thẳng đứng" in content or "Bán phong cách sống" in content:
            print("[SUCCESS] New text found on the page!")
        else:
            print("[WARNING] New text NOT found. Cloudflare might still be building or caching.")
            
        page.screenshot(path="ytuong_live_screenshot.png", full_page=True)
        print("Screenshot saved to ytuong_live_screenshot.png")
        browser.close()

verify_site()
