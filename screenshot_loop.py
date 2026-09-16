from playwright.sync_api import sync_playwright
import time
import sys

def verify_site():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for i in range(10): # try 10 times (approx 2 minutes)
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            print(f"[{i+1}/10] Navigating to https://ytuong.fedu.vn...")
            
            # bypass cache to ensure we get latest
            page.set_extra_http_headers({"Cache-Control": "no-cache"})
            page.goto("https://ytuong.fedu.vn", wait_until="networkidle")
            
            try:
                page.wait_for_selector('.idea-card', timeout=10000)
                time.sleep(3)
                
                content = page.content()
                if "Dùng hook treo máy thẳng đứng" in content or "Bán phong cách sống" in content or "đẩy góc nhìn ra cảnh ngồi thuyền kayak" in content:
                    print("[SUCCESS] New text found on the page!")
                    page.screenshot(path="/Users/vietmac/.gemini/antigravity/brain/35f8baf8-7e5e-4d40-8360-340eadc1c9c2/ytuong_live_screenshot.png", full_page=True)
                    print("Screenshot saved.")
                    browser.close()
                    sys.exit(0)
                else:
                    print("[WARNING] New text NOT found. Retrying in 15 seconds...")
            except Exception as e:
                print(f"[ERROR] {e}. Retrying...")
            
            page.close()
            time.sleep(15)
            
        print("[FAIL] Could not verify new text after multiple attempts.")
        browser.close()
        sys.exit(1)

verify_site()
