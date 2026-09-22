from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    logs = []
    page.on("console", lambda msg: logs.append(f"[{msg.type}] {msg.text}"))
    page.on("pageerror", lambda err: logs.append(f"[pageerror] {err}"))
    
    # Go to the broken URL
    page.goto('https://ytuong.fedu.vn/reports/IG_@Rika_ビオトープめだか植物のある暮らし_Da5KgjAxfOG_Video_by_r_6cafe.html')
    page.wait_for_timeout(5000)
    
    print("--- CONSOLE LOGS ---")
    for log in logs:
        print(log)
    print("--------------------")
    browser.close()
