const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://ytuong.fedu.vn');
  
  await page.evaluate(() => {
    let st = JSON.parse(localStorage.getItem('fedu_video_ideas_state') || '{}');
    st.curationMode = true;
    localStorage.setItem('fedu_video_ideas_state', JSON.stringify(st));
  });
  await page.reload();
  await page.waitForTimeout(3000);
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(3000);
  
  const srcs = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('img')).map(img => img.src);
  });
  
  console.log("All image srcs (first 10):");
  console.log(srcs.slice(0, 10));
  
  await browser.close();
})();
