from playwright.sync_api import sync_playwright
import time
import os

with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page()
    page.goto(f"file://{os.path.abspath('test_video_tag.html')}")
    time.sleep(5)
    duration = page.evaluate("document.getElementById('vid').duration")
    error = page.evaluate("document.getElementById('vid').error")
    print(f"duration: {duration}, error: {error}")
    browser.close()
