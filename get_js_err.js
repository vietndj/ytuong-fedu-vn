const { chromium } = require('playwright');
(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    page.on('pageerror', err => {
        console.log("=== PAGE ERROR ===");
        console.log(err.message);
        console.log(err.stack);
    });
    await page.goto("https://ytuong.fedu.vn/reports/IG_@Chibuzor_Ossai_DdRGI36Aj0X_Carousel_Analysis");
    await page.waitForTimeout(3000);
    await browser.close();
})();
