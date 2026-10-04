from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://ytuong.fedu.vn/")
    page.wait_for_timeout(5000)
    cards = page.query_selector_all(".shot-card")
    for i, card in enumerate(cards[:6]):
        title = card.query_selector(".creator-info strong")
        title_text = title.inner_text() if title else "N/A"
        desc = card.query_selector(".video-title-desc")
        desc_text = desc.inner_text() if desc else "N/A"
        print(f"Card {i+1}: {title_text} - {desc_text}")
    browser.close()
