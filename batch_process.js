const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const { execSync } = require('child_process');
const { chromium } = require('playwright');

const filesToProcess = [
    "Everyday_Filming_Logic_Carousel - @jazziesillona",
    "Hong_Kong_Visual_Rhythm_Carousel - @withyuee",
    "IG_@Andrei_Kostromskikh_DcI-darjckz_Carousel_Analysis",
    "IG_@Andrei_Kostromskikh_DctRlh0jZlj_Carousel_Analysis",
    "IG_@Banh_shimano_Dc0-FXlE4kV_Carousel_Analysis",
    "IG_@Beixin_Travel_&_Nature_Dc0zRNwDz11_Carousel_Analysis",
    "IG_@Gabe_Harris_Dc3ih_5jlqz_Carousel_Analysis",
    "IG_@davidmurphyfilm_Ddo3aQxjMeq_Carousel_Analysis",
    "IG_@dvdnguyen_DdXbbBiEq7P_Carousel_Analysis",
    "IG_@gakuyen_Dc0MQfeEwp4_Carousel_Analysis",
    "IG_@mcjacoub_Ddlh5pagYie_Carousel_Analysis",
    "IG_@minghan1004_DdESxNlE2Ay_Carousel_Analysis",
    "IG_@shotsbyzaid_DdkimD5DPNL_Carousel_Analysis",
    "IG_@yongandmike_DdolqWHEsws_Carousel_Analysis",
    "IG_@岳_🍜_GAKU_Dc0MHhTE9z0_Carousel_Analysis",
    "IG_@𝗧𝗵𝗼𝗺𝗮𝘀_𝗠𝗮𝘁𝗵𝗲𝘄_DcgSonjgnkV_Carousel_Analysis",
    "Mood_and_Tone_Carousel - @jazziesillona",
    "Quy_Tac_Quay_Phim_Carousel - @Jacoub_Anwar",
    "Street_Photography_Carousel - @jazziesillona",
    "Urban_Texture_Carousel - @jazziesillona",
    "Visual_Stopping_Power_Carousel - @jazziesillona",
    "Visual_Storytelling_Carousel - @withyuee"
];

let results = [];

async function processFile(fileName) {
    console.log(`\n--- Processing: ${fileName} ---`);
    const filePath = path.join('reports', `${fileName}.html`);
    let html;
    try {
        html = fs.readFileSync(filePath, 'utf8');
    } catch(e) {
        results.push({ name: fileName, status: '❌ File not found' });
        return;
    }

    // STEP 1: Find IG Link
    let igUrl = null;
    const shortcodeMatch = fileName.match(/_([a-zA-Z0-9_-]{11})_/);
    if (shortcodeMatch) {
        igUrl = "https://www.instagram.com/p/" + shortcodeMatch[1] + "/";
    }
    if (!igUrl || (!igUrl.includes('/p/') && !igUrl.includes('/reel'))) {
        const igRegex = /https?:\/\/(www\.)?instagram\.com\/(p|reels|reel)\/[\w-]+/i;
        const match = html.match(igRegex);
        if (match) igUrl = match[0];
    }
    if (!igUrl || !igUrl.includes('instagram.com')) {
        results.push({ name: fileName, status: 'Không có link IG gốc' });
        return;
    }

    // STEP 2: Download via yt-dlp
    const tempDir = path.join(__dirname, 'temp_vids');
    if (fs.existsSync(tempDir)) fs.rmSync(tempDir, { recursive: true, force: true });
    fs.mkdirSync(tempDir);
    
    try {
        console.log(`Downloading: ${igUrl}`);
        execSync(`yt-dlp "${igUrl}" -o "${tempDir}/%(autonumber)s.%(ext)s"`, { stdio: 'ignore' });
    } catch (e) {}

    const files = fs.readdirSync(tempDir).filter(f => f.endsWith('.mp4'));
    if (files.length <= 1) {
        results.push({ name: fileName, status: 'Single video, không cần sửa' });
        return;
    }

    // STEP 3: Upload YouTube Unlisted
    const ytIds = [];
    for (const file of files) {
        const fullPath = path.join(tempDir, file);
        try {
            console.log(`Uploading ${file}...`);
            const result = execSync(`python3 upload_yt.py "${fullPath}" "${fileName}"`, { stdio: 'pipe' }).toString().trim();
            const id = result.split('\n').pop().trim();
            if (id && id.length === 11) ytIds.push(id);
            else throw new Error("Invalid YT ID");
        } catch (e) {
            const errStr = e.stderr ? e.stderr.toString() : str(e);
            if (errStr.includes("ERROR_QUOTA") || errStr.includes("ERROR_AUTH")) {
                console.error("QUOTA ERROR! Halting.");
                process.exit(1);
            }
            results.push({ name: fileName, status: '❌ Lỗi upload YT' });
            return;
        }
    }

    // STEP 4: HTML edits
    const $ = cheerio.load(html);
    const stack = $('.carousel-stack');
    if (!stack.length) {
        results.push({ name: fileName, status: '❌ Không tìm thấy .carousel-stack' });
        return;
    }
    stack.empty();
    ytIds.forEach(id => {
        stack.append(`<iframe src="https://www.youtube.com/embed/${id}?autoplay=0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n`);
    });

    if (!$.html().includes('video-player-container-fix')) {
        $('head').append(`\n<style class="video-player-container-fix">\n.video-player-container { height: 75vh !important; max-height: none !important; aspect-ratio: auto !important; }\n.carousel-stack { overflow-y: scroll !important; scroll-snap-type: y mandatory !important; }\niframe { flex: 0 0 100% !important; height: 100% !important; object-fit: contain !important; scroll-snap-align: start !important; border: none !important; }\n</style>\n`);
    }

    if ($('.carousel-nav-overlay').length === 0) {
        $('.video-player-container').append(`\n<div class="carousel-nav-overlay" style="position:absolute; right:10px; bottom:20px; display:flex; flex-direction:column; gap:10px; z-index:100;">\n<button class="nav-btn" onclick="const stack = document.querySelector('.carousel-stack'); if(stack) stack.scrollBy({top: -stack.clientHeight, behavior: 'smooth'})" style="padding:10px; background:rgba(0,0,0,0.6); color:white; border:none; border-radius:50%; width: 44px; height: 44px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 16px;">▲</button>\n<button class="nav-btn" onclick="const stack = document.querySelector('.carousel-stack'); if(stack) stack.scrollBy({top: stack.clientHeight, behavior: 'smooth'})" style="padding:10px; background:rgba(0,0,0,0.6); color:white; border:none; border-radius:50%; width: 44px; height: 44px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 16px;">▼</button>\n</div>\n`);
    }

    let jsError = 'No';
    $('script').each((i, el) => {
        let scriptContent = $(el).html();
        if (scriptContent) {
            scriptContent = scriptContent.replace(/if\s*\(player\)\s*player\.currentTime\s*=\s*startTime;\s*\}/g, 'if(player) player.currentTime = startTime;');
            scriptContent = scriptContent.replace('var p = player.play();\n            });\n        }', 'var p = player.play();\n        if (p !== undefined) { p.catch(function(e) {}); }\n        ');
            $(el).text(scriptContent);
        }
    });

    let jsContent = '';
    const $new = cheerio.load($.html());
    $new('script').each((i, el) => { jsContent += $new(el).html() + '\n'; });
    if (jsContent.trim()) {
        fs.writeFileSync('temp_script_verify.js', jsContent);
        try { execSync('node -c temp_script_verify.js', { stdio: 'ignore' }); } 
        catch (e) { jsError = 'Yes'; }
    }

    fs.writeFileSync(filePath, $.html());
    fs.mkdirSync('dist/reports', { recursive: true });
    fs.copyFileSync(filePath, path.join('dist/reports', `${fileName}.html`));

    // STEP 5: Git Push & Deploy Wait
    try {
        execSync(`git add "${filePath}" "dist/reports/${fileName}.html"`);
        execSync(`git commit -m "fix(carousel): process ${fileName}"`);
        execSync(`git push`);
    } catch(e) {}
    
    // Check deploy (wait up to 60 * 5s)
    let deployed = false;
    for(let i=0; i<60; i++) {
        try {
            const liveHtml = execSync(`curl -s "https://ytuong.fedu.vn/reports/${encodeURI(fileName)}.html"`).toString();
            if(liveHtml.includes(ytIds[0])) { deployed = true; break; }
        } catch(e) {}
        execSync('sleep 5');
    }
    if (!deployed) {
        results.push({ name: fileName, status: '❌ Deploy timeout' });
        return;
    }

    // STEP 6: Screenshot (Playwright)
    let pageError = false;
    const browser = await chromium.launch();
    const page = await browser.newPage();
    page.on('pageerror', err => { pageError = true; });
    await page.goto(`https://ytuong.fedu.vn/reports/${encodeURI(fileName)}.html`, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    const screenshotPath = path.join(__dirname, `${fileName}_screenshot.png`);
    await page.screenshot({ path: screenshotPath, fullPage: true });
    await browser.close();

    if (pageError) jsError = 'Yes (Runtime)';

    results.push({ 
        name: fileName, 
        status: 'Processed', 
        slides: ytIds.length, 
        ytIds: ytIds.join(','),
        jsError: jsError,
        screenshot: screenshotPath
    });
}

(async () => {
    for (const file of filesToProcess) {
        await processFile(file);
    }
    fs.writeFileSync('batch_results.json', JSON.stringify(results, null, 2));
    console.log("ALL DONE!");
})();
