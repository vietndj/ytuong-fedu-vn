const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const logs = [];
  page.on('console', msg => logs.push(`[${msg.type()}] ${msg.text()}`));
  
  await page.goto('https://ytuong.fedu.vn/reports/IG_@Rika_ビオトープめだか植物のある暮らし_Da5KgjAxfOG_Video_by_r_6cafe.html');
  await page.waitForTimeout(5000); // wait for player logic
  
  console.log("Console Logs:");
  logs.forEach(l => console.log(l));
  
  await browser.close();
})();
