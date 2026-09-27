const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const { execSync } = require('child_process');

const fileName = process.argv[2];
const filePath = path.join('reports', `${fileName}.html`);

if (!fs.existsSync(filePath)) {
    console.error("File not found:", filePath);
    process.exit(1);
}

const html = fs.readFileSync(filePath, 'utf8');
let igUrl = null;

try {
    const jsData = fs.readFileSync('ideas_data.js', 'utf8');
    const reportUrlStr = `"report_url": "reports/${fileName}.html"`;
    const idx = jsData.indexOf(reportUrlStr);
    if (idx !== -1) {
        const beforeBlock = jsData.substring(Math.max(0, idx - 1000), idx);
        const igUrlMatch = beforeBlock.match(/"ig_url"\s*:\s*"([^"]+)"/);
        if (igUrlMatch) {
            igUrl = igUrlMatch[1];
        }
    }
} catch (e) {}


    // Try to extract from filename shortcode
    const shortcodeMatch = fileName.match(/_([a-zA-Z0-9_-]{11})_/);
    if (shortcodeMatch) {
        igUrl = "https://www.instagram.com/p/" + shortcodeMatch[1] + "/";
    }
    
if (!igUrl || !igUrl.includes('/p/') && !igUrl.includes('/reel')) {
    const igRegex = /https?:\/\/(www\.)?instagram\.com\/(p|reels|reel)\/[\w-]+/i;
    const match = html.match(igRegex);
    if (match) igUrl = match[0];
}

if (!igUrl || !igUrl.includes('instagram.com')) {
    console.log("NO_IG_LINK");
    process.exit(0);
}

console.log(`FOUND_IG: ${igUrl}`);

const tempDir = path.join(__dirname, 'temp_vids');
if (fs.existsSync(tempDir)) fs.rmSync(tempDir, { recursive: true, force: true });
fs.mkdirSync(tempDir);

try {
    console.log(`Downloading: ${igUrl}`);
    execSync(`yt-dlp "${igUrl}" -o "${tempDir}/%(autonumber)s.%(ext)s"`, { stdio: 'pipe' });
} catch (e) {}

const files = fs.readdirSync(tempDir).filter(f => f.endsWith('.mp4'));
if (files.length <= 1) {
    console.log("SINGLE_VIDEO");
    process.exit(0);
}

const ytIds = [];
for (const file of files) {
    const fullPath = path.join(tempDir, file);
    try {
        console.log(`Uploading ${file}...`);
        const result = execSync(`python3 upload_yt.py "${fullPath}" "IG Carousel Video"`, { stdio: 'pipe' }).toString().trim();
        const id = result.split('\n').pop().trim();
        if (id && id.length === 11) ytIds.push(id);
        else {
            console.error("Failed YT ID:", id);
            process.exit(1);
        }
    } catch (e) {
        if (e.stderr && e.stderr.toString().includes("ERROR_QUOTA")) process.exit(2);
        process.exit(1);
    }
}

const $ = cheerio.load(html);
const stack = $('.carousel-stack');
if (stack.length) {
    stack.empty();
    ytIds.forEach(id => {
        stack.append(`<iframe src="https://www.youtube.com/embed/${id}?autoplay=0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n`);
    });
} else {
    process.exit(1);
}

$('head').append(`
<style>
.video-wrap { height: 75vh; overflow: hidden; position: relative; }
.carousel-stack { overflow-y: scroll; scroll-snap-type: y mandatory; }
iframe { flex: 0 0 100%; height: 100%; border: none; }
</style>
`);

if ($('.carousel-nav-overlay').length === 0) {
    stack.parent().append(`
<div class="carousel-nav-overlay" style="position:absolute; right:10px; bottom:20px; display:flex; flex-direction:column; gap:10px; z-index:100;">
    <button class="nav-btn" onclick="document.querySelector('.carousel-stack').scrollBy({top: -300, behavior: 'smooth'})" style="padding:10px; background:rgba(0,0,0,0.5); color:white; border:none; border-radius:50%;">▲</button>
    <button class="nav-btn" onclick="document.querySelector('.carousel-stack').scrollBy({top: 300, behavior: 'smooth'})" style="padding:10px; background:rgba(0,0,0,0.5); color:white; border:none; border-radius:50%;">▼</button>
</div>
    `);
}

// Fix known JS error
$('script').each((i, el) => {
    let scriptContent = $(el).html();
    if (scriptContent) {
        scriptContent = scriptContent.replace(/if\s*\(player\)\s*player\.currentTime\s*=\s*startTime;\s*\}/g, 'if(player) player.currentTime = startTime;');
        $(el).text(scriptContent);
    }
});

let jsContent = '';
$('script').each((i, el) => {
    jsContent += $(el).html() + '\n';
});

if (jsContent.trim()) {
    fs.writeFileSync('temp_script.js', jsContent);
    try {
        execSync('node -c temp_script.js', { stdio: 'pipe' });
    } catch (e) {
        console.error("JS_ERROR:", e.stderr.toString());
        process.exit(3);
    }
}

fs.writeFileSync(filePath, $.html());
try {
    fs.mkdirSync('dist/reports', { recursive: true });
    fs.copyFileSync(filePath, path.join('dist/reports', `${fileName}.html`));
} catch(e) {}

console.log("SUCCESS:", ytIds.join(','));
