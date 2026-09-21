const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + __dirname + '/test_onerror.html');
  await page.waitForTimeout(2000);
  const text = await page.evaluate(() => document.body.innerText);
  console.log("Result:", text);
  await browser.close();
})();
