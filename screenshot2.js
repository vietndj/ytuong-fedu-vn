const { chromium } = require('playwright');
(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    try {
        await page.goto('https://ytuong.fedu.vn/reports/IG_@gakuyen_Dc0MQfeEwp4_Carousel_Analysis.html', { waitUntil: 'load', timeout: 30000 });
        // wait a bit for iframes to render
        await page.waitForTimeout(5000);
        await page.screenshot({ path: 'screenshots/IG_@gakuyen_Dc0MQfeEwp4_Carousel_Analysis.png', fullPage: true });
    } catch(e) {
        console.error(e);
    }
    await browser.close();
})();
