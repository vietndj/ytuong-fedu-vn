import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://ytuong.fedu.vn/")
    
    # Wait for the images to render
    page.wait_for_selector("img[onerror*='handleCardThumbError']", timeout=15000)
    page.wait_for_timeout(3000)
    
    # Take screenshot
    page.screenshot(path="test_home_live.png", full_page=True)
    
    # Evaluate images
    images = page.evaluate("""
        () => {
            const imgs = document.querySelectorAll("img[onerror*='handleCardThumbError']");
            return Array.from(imgs).map(img => ({
                src: img.src,
                naturalHeight: img.naturalHeight,
                complete: img.complete
            }));
        }
    """)
    
    failed = [img for img in images if img['naturalHeight'] == 0]
    print(f"Total images checked: {len(images)}")
    print(f"Failed images: {len(failed)}")
    
    if len(failed) > 0:
        print("Sample failed image:", failed[0])
    browser.close()
