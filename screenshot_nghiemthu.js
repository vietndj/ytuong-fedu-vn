const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  
  await page.goto('http://localhost:8000/index.html', { waitUntil: 'networkidle' });
  
  // wait for data to load
  await page.waitForTimeout(2000);
  
  // wait for the filter tags to render (Kho Ý Tưởng section)
  await page.screenshot({ path: 'nghiemthu_tags.png', fullPage: true });
  console.log("Screenshot saved as nghiemthu_tags.png");
  
  await browser.close();
})();
