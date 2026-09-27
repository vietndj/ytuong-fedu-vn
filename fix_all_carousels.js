const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const { execSync } = require('child_process');

const reportsDir = 'reports';
const distDir = 'dist/reports';
if (!fs.existsSync(distDir)) fs.mkdirSync(distDir, { recursive: true });

const files = fs.readdirSync(reportsDir).filter(f => f.endsWith('.html'));

let fixedCount = 0;

for (const file of files) {
    const filePath = path.join(reportsDir, file);
    let html = fs.readFileSync(filePath, 'utf8');
    
    // Only process files with .carousel-stack
    if (!html.includes('carousel-stack')) continue;
    
    const $ = cheerio.load(html);
    let modified = false;
    
    // 1. Fix CSS
    if (!html.includes('video-player-container-fix')) {
        $('head').append(`
<style class="video-player-container-fix">
.video-player-container { height: 75vh !important; max-height: none !important; aspect-ratio: auto !important; }
.carousel-stack { overflow-y: scroll !important; scroll-snap-type: y mandatory !important; }
.carousel-stack > * { flex: 0 0 100% !important; height: 100% !important; object-fit: contain !important; scroll-snap-align: start !important; border: none !important; }
</style>
        `);
        modified = true;
    }
    
    // 2. Add Navigation Overlay
    if ($('.carousel-nav-overlay').length === 0) {
        $('.video-player-container').append(`
<div class="carousel-nav-overlay" style="position:absolute; right:10px; bottom:20px; display:flex; flex-direction:column; gap:10px; z-index:100;">
    <button class="nav-btn" onclick="const stack = document.querySelector('.carousel-stack'); if(stack) stack.scrollBy({top: -stack.clientHeight, behavior: 'smooth'})" style="padding:10px; background:rgba(0,0,0,0.6); color:white; border:none; border-radius:50%; width: 44px; height: 44px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 16px;">▲</button>
    <button class="nav-btn" onclick="const stack = document.querySelector('.carousel-stack'); if(stack) stack.scrollBy({top: stack.clientHeight, behavior: 'smooth'})" style="padding:10px; background:rgba(0,0,0,0.6); color:white; border:none; border-radius:50%; width: 44px; height: 44px; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 16px;">▼</button>
</div>
        `);
        modified = true;
    }
    
    // 3. Fix JS Syntax Error
    $('script').each((i, el) => {
        let scriptContent = $(el).html();
        if (scriptContent && scriptContent.match(/if\s*\(player\)\s*player\.currentTime\s*=\s*startTime;\s*\}/)) {
            scriptContent = scriptContent.replace(/if\s*\(player\)\s*player\.currentTime\s*=\s*startTime;\s*\}/g, 'if(player) player.currentTime = startTime;');
            $(el).text(scriptContent);
            modified = true;
        }
    });

    if (modified) {
        const newHtml = $.html();
        fs.writeFileSync(filePath, newHtml);
        fs.copyFileSync(filePath, path.join(distDir, file));
        fixedCount++;
        console.log(`Fixed: ${file}`);
        
        // Verify JS syntax
        let jsContent = '';
        const $new = cheerio.load(newHtml);
        $new('script').each((i, el) => { jsContent += $new(el).html() + '\n'; });
        if (jsContent.trim()) {
            fs.writeFileSync('temp_script_verify.js', jsContent);
            try {
                execSync('node -c temp_script_verify.js', { stdio: 'pipe' });
            } catch (e) {
                console.error(`JS_ERROR in ${file}:`, e.stderr.toString());
            }
        }
    }
}

if (fs.existsSync('temp_script_verify.js')) fs.unlinkSync('temp_script_verify.js');
console.log(`Total fixed: ${fixedCount}`);
