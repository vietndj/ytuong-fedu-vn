import asyncio
from playwright.async_api import async_playwright
import json
import urllib.parse

async def run():
    url = "https://ytuong.fedu.vn/reports/IG_@jigummmmm_DdnqexOTN8A_%EC%84%A4%EA%B1%B0%EC%A7%80%ED%95%98%EB%8A%94_%EB%AA%A8%EC%8A%B5%EB%8F%84_%EC%98%88%EC%81%98%EA%B2%8C_%EC%B0%8D%EC%9D%84_%EC%88%98_%EC%9E%88%EB%83%90%EA%B3%A0%EC%9A%94.html"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # Desktop
        context_desktop = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page_desktop = await context_desktop.new_page()
        
        console_errors_desktop = []
        page_desktop.on('console', lambda msg: console_errors_desktop.append(msg.text) if msg.type == 'error' else None)
        page_desktop.on('pageerror', lambda err: console_errors_desktop.append(str(err)))
        
        await page_desktop.goto(url, wait_until='networkidle')
        await page_desktop.evaluate('() => document.fonts.ready')
        await page_desktop.screenshot(path='vision_report_desktop.png', full_page=True)
        
        dom_report_desktop = await get_dom_probe(page_desktop, console_errors_desktop)
        with open('dom_probe_desktop.json', 'w', encoding='utf-8') as f:
            json.dump(dom_report_desktop, f, ensure_ascii=False, indent=2)
            
        await context_desktop.close()
        
        # Mobile
        iphone_13 = p.devices['iPhone 13']
        context_mobile = await browser.new_context(**iphone_13)
        page_mobile = await context_mobile.new_page()
        
        console_errors_mobile = []
        page_mobile.on('console', lambda msg: console_errors_mobile.append(msg.text) if msg.type == 'error' else None)
        page_mobile.on('pageerror', lambda err: console_errors_mobile.append(str(err)))
        
        await page_mobile.goto(url, wait_until='networkidle')
        await page_mobile.evaluate('() => document.fonts.ready')
        await page_mobile.screenshot(path='vision_report_mobile.png', full_page=True)
        
        dom_report_mobile = await get_dom_probe(page_mobile, console_errors_mobile)
        with open('dom_probe_mobile.json', 'w', encoding='utf-8') as f:
            json.dump(dom_report_mobile, f, ensure_ascii=False, indent=2)
            
        await context_mobile.close()
        await browser.close()

async def get_dom_probe(page, console_errors):
    return await page.evaluate('''() => {
        const checks = {};
        checks.consoleErrors = window.__capturedErrors || [];
        
        const targets = document.querySelectorAll('.meta-item, .shot-meta-grid, .shot-details, .meta-label, .meta-val, h1, h2, h3, h4, p');
        checks.elements = [...targets].map(el => {
            const rect = el.getBoundingClientRect();
            const style = getComputedStyle(el);
            return {
                tag: el.tagName,
                classes: el.className,
                text: el.textContent?.slice(0, 150) || '',
                visible: rect.width > 0 && rect.height > 0 
                         && style.display !== 'none' 
                         && style.visibility !== 'hidden'
                         && parseFloat(style.opacity) > 0,
                rect: {x: Math.round(rect.x), y: Math.round(rect.y), w: Math.round(rect.width), h: Math.round(rect.height)},
                font: style.fontFamily,
                color: style.color
            };
        });
        
        checks.fontsLoaded = document.fonts.status;
        checks.loadedFontFamilies = [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family);
        return checks;
    }''')

asyncio.run(run())
