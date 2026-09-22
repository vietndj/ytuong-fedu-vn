from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        page = browser.new_page()
        page.on("console", lambda msg: print(f"Console: {msg.text}"))
        page.on("requestfailed", lambda req: print(f"Failed: {req.url} - {req.failure}"))
        
        url = f"file://{os.path.abspath('test_browser.html')}"
        page.goto(url, wait_until="networkidle")
        
        page.screenshot(path="test_browser.png")
        
        browser.close()

run()
