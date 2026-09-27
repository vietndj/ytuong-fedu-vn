const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.on('console', msg => console.log('BROWSER_LOG:', msg.text()));
  page.on('pageerror', err => console.error('BROWSER_ERROR:', err.message));
  
  await page.goto('https://ytuong.fedu.vn/reports/IG_@Andrei_Kostromskikh_DcI-darjckz_Carousel_Analysis.html', { waitUntil: 'networkidle' });
  
  // Try to click the scroll down button to see if it works
  await page.waitForTimeout(1000);
  await page.screenshot({ path: 'screenshot_before_scroll.png', fullPage: true });
  
  const nextBtn = await page.$('.carousel-nav-overlay button:nth-child(2)');
  if (nextBtn) {
    await nextBtn.click();
    await page.waitForTimeout(500); // wait for scroll animation
    await page.screenshot({ path: 'screenshot_after_scroll.png', fullPage: true });
    console.log("Navigated carousel");
  }
  
  await browser.close();
})();
