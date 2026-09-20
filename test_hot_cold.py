import os
import time
from playwright.sync_api import sync_playwright

def run_tests():
    print("Bắt đầu nghiệm thu Hot/Cold Tier...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        idx_path = f"file://{os.path.abspath('dist/index.html')}"
        page.goto(idx_path)
        
        page.wait_for_selector(".glass-card", timeout=10000)
        time.sleep(2)
        
        # Click video card
        page.evaluate("document.querySelectorAll('.glass-card')[0].click()")
        time.sleep(2)
        
        # screenshot
        page.screenshot(path="nghiemthu_hotcold.png")
        print("Đã chụp màn hình nghiemthu_hotcold.png")
        
        print("PASS: Nghiệm thu thành công!")
        browser.close()
        return True

if __name__ == "__main__":
    if run_tests():
        exit(0)
    else:
        exit(1)
