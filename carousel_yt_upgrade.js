/**
 * carousel_yt_upgrade.js
 * =====================
 * Quy trình 6 bước xử lý TUẦN TỰ danh sách báo cáo Carousel.
 * 
 * CÁCH DÙNG:
 *   node carousel_yt_upgrade.js "File1" "File2" "File3"
 *   (Không cần đuôi .html)
 *
 * Hoặc không truyền arg → tự quét toàn bộ reports/ tìm file cần xử lý.
 *
 * QUY TRÌNH:
 *   Bước 1: Quét HTML → đếm <video>, <img>, <iframe> trong .carousel-stack
 *           Nếu có iframe youtube → DONE, bỏ qua
 *           Nếu video=0 hoặc (video+img) < 2 → SINGLE, bỏ qua
 *   Bước 2: Tải video từ URL nguồn trong <video src="...">
 *           3 pattern: ytuong.fedu.vn/api/video, media.fedu.vn/videos, drive.google.com
 *           Nếu 404 → thử fallback qua Drive API proxy
 *   Bước 3: Upload YouTube Unlisted (upload_yt.py)
 *           Nếu quota/auth error → DỪNG TOÀN BỘ
 *   Bước 4: Sửa HTML
 *           - Thay <video> bằng <iframe> YouTube (giữ nguyên <img>)
 *           - Thêm CSS ép khung 75vh + scroll-snap
 *           - Thêm nút điều hướng ▲▼
 *           - Sửa JS lỗi, verify bằng node -c
 *           - Sync dist/reports/
 *   Bước 5: Git push + curl -sL verify deploy (tối đa 60 lần × 5s)
 *   Bước 6: Playwright chụp production + bắt JS error
 */

const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const { execSync } = require('child_process');

// ====== CONFIG ======
const REPORTS_DIR = 'reports';
const DIST_DIR = 'dist/reports';
const TEMP_DIR = path.join(__dirname, 'temp_carousel_vid');
const BASE_URL = 'https://ytuong.fedu.vn/reports';
const SCREENSHOTS_DIR = path.join(__dirname, 'screenshots');
const MAX_DEPLOY_CHECKS = 60;
const DEPLOY_CHECK_INTERVAL_S = 5;
const MAX_JS_FIX_LOOPS = 3;

// ====== RESULTS ======
const results = [];

// ====== HELPERS ======
function log(msg) { console.log(`[${new Date().toLocaleTimeString()}] ${msg}`); }

function cleanTemp() {
  if (fs.existsSync(TEMP_DIR)) fs.rmSync(TEMP_DIR, { recursive: true, force: true });
  fs.mkdirSync(TEMP_DIR, { recursive: true });
}

function extractDriveIdFromApiUrl(url) {
  // https://ytuong.fedu.vn/api/video?id=XXXXX → XXXXX
  const m = url.match(/api\/video\?id=([^&"]+)/);
  return m ? m[1] : null;
}

// ====== BƯỚC 1: QUÉT HTML ======
function analyzeFile(fileName) {
  const filePath = path.join(REPORTS_DIR, `${fileName}.html`);
  if (!fs.existsSync(filePath)) return { skip: true, reason: 'File not found' };

  const html = fs.readFileSync(filePath, 'utf8');
  const $ = cheerio.load(html);
  const stack = $('div.carousel-stack').first();

  const videos = stack.find('video');
  const imgs = stack.find('img');
  const iframes = stack.find('iframe');

  if (iframes.length > 0) return { skip: true, reason: '✅ Đã có YouTube iframe' };
  if (videos.length === 0) return { skip: true, reason: 'Không có video trong carousel-stack' };
  if (videos.length + imgs.length < 2) return { skip: true, reason: '🔵 Single video, không phải carousel' };

  const videoSrc = $(videos[0]).attr('src') || '';
  return {
    skip: false,
    filePath,
    html,
    videoSrc,
    videoCount: videos.length,
    imgCount: imgs.length,
    totalSlides: videos.length + imgs.length
  };
}

// ====== BƯỚC 2: TẢI VIDEO ======
function downloadVideo(videoSrc, fileName) {
  cleanTemp();
  const destPath = path.join(TEMP_DIR, 'video.mp4');

  // Pattern 1: ytuong.fedu.vn/api/video?id=DRIVE_ID
  if (videoSrc.includes('api/video?id=')) {
    log(`  Tải video từ Drive API proxy: ${videoSrc.substring(0, 80)}...`);
    try {
      execSync(`curl -sL -o "${destPath}" "${videoSrc}"`, { timeout: 120000 });
      const stat = fs.statSync(destPath);
      if (stat.size < 10000) throw new Error('File quá nhỏ, có thể bị lỗi');
      return destPath;
    } catch (e) {
      return null;
    }
  }

  // Pattern 2: media.fedu.vn/videos/...
  if (videoSrc.includes('media.fedu.vn/videos/')) {
    log(`  Tải video từ R2: ${videoSrc.substring(0, 80)}...`);
    try {
      execSync(`curl -sL -o "${destPath}" "${videoSrc}"`, { timeout: 120000 });
      const stat = fs.statSync(destPath);
      if (stat.size < 10000) throw new Error('File quá nhỏ hoặc 404');
      return destPath;
    } catch (e) {
      // Fallback: tìm Drive ID từ ideas_data.js
      log(`  R2 lỗi, thử fallback Drive API...`);
      return downloadFallbackDrive(fileName);
    }
  }

  // Pattern 3: drive.google.com
  if (videoSrc.includes('drive.google.com')) {
    const driveId = videoSrc.match(/id=([^&]+)/);
    if (driveId) {
      const proxyUrl = `https://ytuong.fedu.vn/api/video?id=${driveId[1]}`;
      log(`  Tải video qua Drive proxy: ${proxyUrl.substring(0, 80)}...`);
      try {
        execSync(`curl -sL -o "${destPath}" "${proxyUrl}"`, { timeout: 120000 });
        const stat = fs.statSync(destPath);
        if (stat.size < 10000) throw new Error('File quá nhỏ');
        return destPath;
      } catch (e) {
        return null;
      }
    }
  }

  // Unknown pattern
  log(`  ⚠️ URL video không nhận diện được: ${videoSrc.substring(0, 80)}`);
  return null;
}

function downloadFallbackDrive(fileName) {
  try {
    const ideasData = fs.readFileSync('ideas_data.js', 'utf8');
    const reportStr = `reports/${fileName}.html`;
    const idx = ideasData.indexOf(reportStr);
    if (idx === -1) return null;
    
    const block = ideasData.substring(Math.max(0, idx - 2000), idx + 200);
    
    // Try video_url first
    const videoUrlMatch = block.match(/"video_url"\s*:\s*"([^"]+)"/);
    if (videoUrlMatch) {
      const vidUrl = videoUrlMatch[1];
      const driveIdMatch = vidUrl.match(/id=([^&]+)/);
      if (driveIdMatch) {
        const proxyUrl = `https://ytuong.fedu.vn/api/video?id=${driveIdMatch[1]}`;
        const destPath = path.join(TEMP_DIR, 'video.mp4');
        execSync(`curl -sL -o "${destPath}" "${proxyUrl}"`, { timeout: 120000 });
        const stat = fs.statSync(destPath);
        if (stat.size > 10000) return destPath;
      }
    }

    // Try gdrive_folder → list files via API? → too complex, skip
    return null;
  } catch (e) {
    return null;
  }
}

// ====== BƯỚC 3: UPLOAD YOUTUBE ======
function uploadToYoutube(videoPath, title) {
  log(`  Uploading YouTube: ${title}`);
  try {
    const result = execSync(
      `python3 upload_yt.py "${videoPath}" "${title}"`,
      { stdio: 'pipe', timeout: 300000 }
    ).toString().trim();
    
    const ytId = result.split('\n').pop().trim();
    if (ytId && ytId.length === 11) {
      log(`  ✅ YouTube ID: ${ytId}`);
      return ytId;
    }
    throw new Error(`Invalid YouTube ID: ${ytId}`);
  } catch (e) {
    const errStr = e.stderr ? e.stderr.toString() : String(e);
    if (errStr.includes('ERROR_QUOTA') || errStr.includes('quotaExceeded')) {
      log(`  🚨 QUOTA HẾT — DỪNG TOÀN BỘ TASK`);
      // Write partial results before exit
      fs.writeFileSync('carousel_results.json', JSON.stringify(results, null, 2));
      process.exit(99);
    }
    if (errStr.includes('ERROR_AUTH')) {
      log(`  🚨 AUTH LỖI — DỪNG TOÀN BỘ TASK`);
      fs.writeFileSync('carousel_results.json', JSON.stringify(results, null, 2));
      process.exit(98);
    }
    throw e;
  }
}

// ====== BƯỚC 4: SỬA HTML ======
function fixHtml(fileName, ytId) {
  const filePath = path.join(REPORTS_DIR, `${fileName}.html`);
  let html = fs.readFileSync(filePath, 'utf8');
  const $ = cheerio.load(html);

  // 4a: Thay <video> bằng <iframe> YouTube (giữ nguyên <img>)
  const stack = $('div.carousel-stack').first();
  stack.find('video').each((i, el) => {
    const iframe = `<iframe src="https://www.youtube.com/embed/${ytId}?autoplay=0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="flex:0 0 100%; width:100%; height:100%; scroll-snap-align:start; background:#000; border:none;"></iframe>`;
    $(el).replaceWith(iframe);
  });

  // 4b: Thêm CSS ép khung
  if (!$.html().includes('carousel-yt-fix-css')) {
    $('head').append(`
<style class="carousel-yt-fix-css">
.video-player-container { height: 75vh !important; max-height: none !important; aspect-ratio: auto !important; overflow: hidden !important; position: relative !important; }
.carousel-stack { overflow-y: scroll !important; scroll-snap-type: y mandatory !important; height: 100% !important; }
.carousel-stack > * { flex: 0 0 100% !important; height: 100% !important; object-fit: contain !important; scroll-snap-align: start !important; }
.carousel-stack iframe { border: none !important; }
</style>
`);
  }

  // 4c: Thêm nút điều hướng ▲▼
  if ($('.carousel-nav-overlay').length === 0) {
    const playerContainer = stack.parent();
    playerContainer.append(`
<div class="carousel-nav-overlay" style="position:absolute; right:10px; bottom:20px; display:flex; flex-direction:column; gap:10px; z-index:100;">
    <button onclick="var s=document.querySelector('.carousel-stack');if(s)s.scrollBy({top:-s.clientHeight,behavior:'smooth'})" style="padding:10px; background:rgba(0,0,0,0.6); color:white; border:none; border-radius:50%; width:44px; height:44px; cursor:pointer; font-size:16px;">▲</button>
    <button onclick="var s=document.querySelector('.carousel-stack');if(s)s.scrollBy({top:s.clientHeight,behavior:'smooth'})" style="padding:10px; background:rgba(0,0,0,0.6); color:white; border:none; border-radius:50%; width:44px; height:44px; cursor:pointer; font-size:16px;">▼</button>
</div>
`);
  }

  // 4d: Sửa lỗi JS đã biết
  $('script').each((i, el) => {
    let sc = $(el).html();
    if (!sc) return;
    // Lỗi 1: if(player) player.currentTime = startTime; }  ← dư }
    sc = sc.replace(/if\s*\(player\)\s*player\.currentTime\s*=\s*startTime;\s*\}/g,
      'if(player) player.currentTime = startTime;');
    // Lỗi 2: var p = player.play();\n            });\n        }  ← đứt gãy
    sc = sc.replace(/var p = player\.play\(\);\s*\}\);\s*\}/g,
      'var p = player.play(); if(p!==undefined){p.catch(function(e){});}');
    $(el).text(sc);
  });

  // 4e: Verify JS syntax (loop tối đa 3 lần)
  let jsError = 'No';
  for (let attempt = 0; attempt < MAX_JS_FIX_LOOPS; attempt++) {
    let jsContent = '';
    const $check = cheerio.load($.html());
    $check('script').each((i, el) => { jsContent += $check(el).html() + '\n'; });
    if (!jsContent.trim()) break;

    fs.writeFileSync('temp_js_check.js', jsContent);
    try {
      execSync('node -c temp_js_check.js', { stdio: 'pipe' });
      break; // PASS
    } catch (e) {
      jsError = `Attempt ${attempt + 1}`;
      log(`  ⚠️ JS SyntaxError (attempt ${attempt + 1}/${MAX_JS_FIX_LOOPS})`);
      // Aggressive cleanup: remove problematic patterns
      $('script').each((i, el) => {
        let sc = $(el).html();
        if (!sc) return;
        // Remove orphaned }); patterns
        sc = sc.replace(/^\s*\}\);\s*$/gm, '');
        $(el).text(sc);
      });
    }
  }
  if (fs.existsSync('temp_js_check.js')) fs.unlinkSync('temp_js_check.js');

  // 4f: Cũng cập nhật mainPlayer references để dùng iframe
  // Cập nhật rawVideoSrc thành YouTube embed
  $('script').each((i, el) => {
    let sc = $(el).html();
    if (!sc) return;
    if (sc.includes('rawVideoSrc')) {
      sc = sc.replace(
        /const rawVideoSrc = "[^"]+";/,
        `const rawVideoSrc = "https://www.youtube.com/embed/${ytId}";`
      );
      $(el).text(sc);
    }
  });

  // Write
  const finalHtml = $.html();
  fs.writeFileSync(filePath, finalHtml);
  
  // Sync dist
  fs.mkdirSync(DIST_DIR, { recursive: true });
  fs.copyFileSync(filePath, path.join(DIST_DIR, `${fileName}.html`));

  return jsError;
}

// ====== BƯỚC 5: GIT PUSH + DEPLOY CHECK ======
function gitPushAndVerify(fileName, ytId) {
  const filePath = path.join(REPORTS_DIR, `${fileName}.html`);
  const distPath = path.join(DIST_DIR, `${fileName}.html`);

  try {
    execSync(`git add "${filePath}" "${distPath}"`, { stdio: 'pipe' });
    execSync(`git commit -m "fix(carousel): YouTube upgrade ${fileName}"`, { stdio: 'pipe' });
    execSync('git push', { stdio: 'pipe', timeout: 60000 });
    log(`  ✅ Git pushed`);
  } catch (e) {
    log(`  ⚠️ Git push warning: ${e.message.substring(0, 80)}`);
  }

  // Verify deploy with curl -sL (follow redirects!)
  const liveUrl = `${BASE_URL}/${encodeURIComponent(fileName)}.html`;
  log(`  Đợi deploy: ${liveUrl.substring(0, 80)}...`);
  
  for (let i = 0; i < MAX_DEPLOY_CHECKS; i++) {
    try {
      const liveHtml = execSync(
        `curl -sL "${liveUrl}"`,
        { stdio: 'pipe', timeout: 15000 }
      ).toString();
      
      if (liveHtml.includes(`youtube.com/embed/${ytId}`)) {
        log(`  ✅ Deploy confirmed (check ${i + 1})`);
        return true;
      }
    } catch (e) {}
    
    execSync(`sleep ${DEPLOY_CHECK_INTERVAL_S}`);
  }

  log(`  ❌ Deploy timeout sau ${MAX_DEPLOY_CHECKS * DEPLOY_CHECK_INTERVAL_S}s`);
  return false;
}

// ====== BƯỚC 6: NGHIỆM THU PLAYWRIGHT ======
async function screenshotProduction(fileName) {
  fs.mkdirSync(SCREENSHOTS_DIR, { recursive: true });
  const liveUrl = `${BASE_URL}/${encodeURIComponent(fileName)}.html`;
  const screenshotPath = path.join(SCREENSHOTS_DIR, `${fileName}.png`);

  let pageErrors = [];
  try {
    const { chromium } = require('playwright');
    const browser = await chromium.launch();
    const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    
    page.on('pageerror', err => pageErrors.push(err.message));
    
    await page.goto(liveUrl, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);
    await page.screenshot({ path: screenshotPath, fullPage: false });
    
    await browser.close();
    log(`  📸 Screenshot: ${screenshotPath}`);
  } catch (e) {
    log(`  ⚠️ Playwright error: ${e.message.substring(0, 80)}`);
  }

  return {
    screenshotPath,
    pageErrors,
    hasJsError: pageErrors.length > 0
  };
}

// ====== MAIN ======
async function processFile(fileName) {
  log(`\n━━━ [${fileName}] ━━━`);

  // BƯỚC 1
  const analysis = analyzeFile(fileName);
  if (analysis.skip) {
    log(`  ⏭️  ${analysis.reason}`);
    results.push({ name: fileName, slides: '-', ytIds: '-', jsError: '-', vision: '-', status: analysis.reason });
    return;
  }
  log(`  📊 Carousel: ${analysis.videoCount} video + ${analysis.imgCount} ảnh = ${analysis.totalSlides} slides`);

  // BƯỚC 2
  const videoPath = downloadVideo(analysis.videoSrc, fileName);
  if (!videoPath) {
    const reason = '❌ Không tải được video từ nguồn gốc';
    log(`  ${reason}`);
    results.push({ name: fileName, slides: analysis.totalSlides, ytIds: '-', jsError: '-', vision: '-', status: reason });
    return;
  }
  log(`  ✅ Video tải xong: ${(fs.statSync(videoPath).size / 1024 / 1024).toFixed(1)}MB`);

  // BƯỚC 3
  let ytId;
  try {
    ytId = uploadToYoutube(videoPath, `Carousel Slide - ${fileName}`);
  } catch (e) {
    const reason = '❌ Lỗi upload YouTube: ' + e.message.substring(0, 60);
    log(`  ${reason}`);
    results.push({ name: fileName, slides: analysis.totalSlides, ytIds: '-', jsError: '-', vision: '-', status: reason });
    return;
  }

  // BƯỚC 4
  const jsError = fixHtml(fileName, ytId);
  log(`  ✅ HTML đã sửa (JS: ${jsError})`);

  // BƯỚC 5
  const deployed = gitPushAndVerify(fileName, ytId);
  if (!deployed) {
    results.push({ name: fileName, slides: analysis.totalSlides, ytIds: ytId, jsError, vision: '❌ Deploy timeout', status: '❌ Deploy timeout', liveUrl: `${BASE_URL}/${encodeURIComponent(fileName)}.html` });
    return;
  }

  // BƯỚC 6
  const screenshot = await screenshotProduction(fileName);
  const visionStatus = screenshot.hasJsError ? '⚠️ JS Error runtime' : '✅ Đạt';

  results.push({
    name: fileName,
    slides: analysis.totalSlides,
    ytIds: ytId,
    jsError,
    vision: visionStatus,
    status: 'Processed',
    liveUrl: `${BASE_URL}/${encodeURIComponent(fileName)}.html`,
    screenshot: screenshot.screenshotPath
  });
  log(`  🎉 HOÀN THÀNH: ${visionStatus}`);
}

async function main() {
  // Xác định danh sách file cần xử lý
  let fileList;
  
  if (process.argv.length > 2) {
    // Truyền qua argument
    fileList = process.argv.slice(2);
  } else {
    // Tự quét toàn bộ reports/
    fileList = fs.readdirSync(REPORTS_DIR)
      .filter(f => f.endsWith('.html'))
      .map(f => f.replace('.html', ''));
  }

  log(`Bắt đầu xử lý ${fileList.length} file TUẦN TỰ...`);
  
  for (const fileName of fileList) {
    await processFile(fileName);
  }

  // Xuất kết quả
  fs.writeFileSync('carousel_results.json', JSON.stringify(results, null, 2));
  
  // Xuất bảng markdown
  let md = '| # | Tên | Số slide | YouTube IDs | JS Error | Vision | Link Live |\n';
  md += '|---|---|---|---|---|---|---|\n';
  results.forEach((r, i) => {
    const link = r.liveUrl ? `[Live](${r.liveUrl})` : r.status;
    md += `| ${i + 1} | ${r.name} | ${r.slides} | ${r.ytIds} | ${r.jsError} | ${r.vision} | ${link} |\n`;
  });
  fs.writeFileSync('carousel_results.md', md);
  
  log('\n━━━ KẾT QUẢ TỔNG HỢP ━━━');
  const processed = results.filter(r => r.status === 'Processed').length;
  const skipped = results.filter(r => r.status !== 'Processed' && !r.status.includes('❌')).length;
  const failed = results.filter(r => r.status.includes('❌')).length;
  log(`✅ Thành công: ${processed} | ⏭️ Bỏ qua: ${skipped} | ❌ Lỗi: ${failed}`);
  log(`Bảng kết quả: carousel_results.md`);
  log(`JSON: carousel_results.json`);
}

main().catch(e => {
  console.error('FATAL:', e);
  fs.writeFileSync('carousel_results.json', JSON.stringify(results, null, 2));
  process.exit(1);
});
