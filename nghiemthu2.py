from playwright.sync_api import sync_playwright
import time
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        page = browser.new_page()
        
        url = f"file://{os.path.abspath('./dist/reports/IG_@UME_📍минск-мир_DcVnyJyNWGY_Video_by_ume.izakaya.html')}"
        
        page.goto(url, wait_until="networkidle")
        time.sleep(3)
        
        # Take screenshot
        page.screenshot(path="nghiemthu_images.png", full_page=True)
        
        # Check image count and src
        img_info = page.evaluate("""() => {
            const imgs = Array.from(document.querySelectorAll('.shot-img'));
            return imgs.map(img => img.src);
        }""")
        print(f"Images count: {len(img_info)}, First src: {img_info[0] if img_info else 'None'}")
        
        browser.close()

run()
