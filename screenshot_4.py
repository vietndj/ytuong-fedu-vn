from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 1000})
    page.goto("https://ytuong.fedu.vn/")
    page.wait_for_timeout(5000)
    page.screenshot(path="screenshot_coachk.png")
    browser.close()
