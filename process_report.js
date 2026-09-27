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

// 1. Tìm IG link
const igRegex = /https?:\/\/(www\.)?instagram\.com\/(p|reels)\/[\w-]+/i;
const match = html.match(igRegex);

if (!match) {
    console.log("NO_IG_LINK");
    process.exit(0);
}

const igUrl = match[0];
console.log(`FOUND_IG: ${igUrl}`);

// Clean temp dir
const tempDir = path.join(__dirname, 'temp_vids');
if (fs.existsSync(tempDir)) {
    fs.rmSync(tempDir, { recursive: true, force: true });
}
fs.mkdirSync(tempDir);

// 2. Tải video bằng yt-dlp
try {
    console.log(`Downloading: ${igUrl}`);
    execSync(`yt-dlp "${igUrl}" -o "${tempDir}/%(autonumber)s.%(ext)s"`, { stdio: 'pipe' });
} catch (e) {
    console.error("yt-dlp failed:", e.message);
}

const files = fs.readdirSync(tempDir).filter(f => f.endsWith('.mp4'));
if (files.length <= 1) {
    console.log("SINGLE_VIDEO");
    process.exit(0);
}

console.log(`Found ${files.length} videos`);

// 3. Upload YouTube
const ytIds = [];
for (const file of files) {
    const fullPath = path.join(tempDir, file);
    try {
        console.log(`Uploading ${file}...`);
        const result = execSync(`python3 upload_yt.py "${fullPath}" "IG Carousel Video"`, { stdio: 'pipe' }).toString().trim();
        const id = result.split('\n').pop().trim();
        if (id && id.length === 11) {
            ytIds.push(id);
            console.log(`Uploaded: ${id}`);
        } else {
            console.error("Failed to get valid YT ID:", id);
            process.exit(1);
        }
    } catch (e) {
        console.error("Upload failed", e.stderr ? e.stderr.toString() : e.message);
        if (e.stderr && e.stderr.toString().includes("ERROR_QUOTA")) {
            console.log("ERROR_QUOTA");
            process.exit(2);
        }
        process.exit(1);
    }
}

// 4. Sửa HTML
const $ = cheerio.load(html);

// Sửa carousel stack
const stack = $('.carousel-stack');
if (stack.length) {
    stack.empty();
    ytIds.forEach(id => {
        stack.append(`<iframe src="https://www.youtube.com/embed/${id}?autoplay=0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n`);
    });
}

// Thêm CSS
$('head').append(`
<style>
.video-wrap { height: 75vh; overflow: hidden; position: relative; }
.carousel-stack { overflow-y: scroll; scroll-snap-type: y mandatory; }
iframe { flex: 0 0 100%; height: 100%; border: none; }
</style>
`);

// Thêm nút điều hướng nếu chưa có
if ($('.carousel-nav-overlay').length === 0) {
    stack.parent().append(`
<div class="carousel-nav-overlay" style="position:absolute; right:10px; bottom:20px; display:flex; flex-direction:column; gap:10px; z-index:100;">
    <button class="nav-btn" onclick="document.querySelector('.carousel-stack').scrollBy({top: -300, behavior: 'smooth'})" style="padding:10px; background:rgba(0,0,0,0.5); color:white; border:none; border-radius:50%;">▲</button>
    <button class="nav-btn" onclick="document.querySelector('.carousel-stack').scrollBy({top: 300, behavior: 'smooth'})" style="padding:10px; background:rgba(0,0,0,0.5); color:white; border:none; border-radius:50%;">▼</button>
</div>
    `);
}

// Extract scripts and test
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

// Write back
fs.writeFileSync(filePath, $.html());

console.log("SUCCESS:", ytIds.join(','));
