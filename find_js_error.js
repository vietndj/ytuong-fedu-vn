const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  page.on('pageerror', err => {
      console.log('PAGE ERROR:', err.toString());
      console.log('STACK:', err.stack);
  });
  await page.goto('https://ytuong.fedu.vn/reports/IG_@Chibuzor_Ossai_DdRGI36Aj0X_Carousel_Analysis');
  await browser.close();
})();
