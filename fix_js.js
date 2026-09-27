const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const { execSync } = require('child_process');

const reportsDir = 'reports';
const distDir = 'dist/reports';
const files = fs.readdirSync(reportsDir).filter(f => f.endsWith('.html'));

let fixedCount = 0;

for (const file of files) {
    const filePath = path.join(reportsDir, file);
    let html = fs.readFileSync(filePath, 'utf8');
    
    // 3. Fix JS Syntax Error
    let $ = cheerio.load(html);
    let modified = false;
    $('script').each((i, el) => {
        let scriptContent = $(el).html();
        if (scriptContent) {
            // Fix 1: if(player) player.currentTime = startTime; }
            if (scriptContent.match(/if\s*\(player\)\s*player\.currentTime\s*=\s*startTime;\s*\}/)) {
                scriptContent = scriptContent.replace(/if\s*\(player\)\s*player\.currentTime\s*=\s*startTime;\s*\}/g, 'if(player) player.currentTime = startTime;');
                modified = true;
            }
            // Fix 2: var p = player.play(); }); } }
            if (scriptContent.includes('var p = player.play();\n            });\n        }')) {
                scriptContent = scriptContent.replace('var p = player.play();\n            });\n        }', 'var p = player.play();\n        if (p !== undefined) { p.catch(function(e) {}); }\n        ');
                modified = true;
            }
            if (modified) {
                $(el).text(scriptContent);
            }
        }
    });

    if (modified) {
        const newHtml = $.html();
        fs.writeFileSync(filePath, newHtml);
        fs.copyFileSync(filePath, path.join(distDir, file));
        fixedCount++;
        
        // Verify JS syntax
        let jsContent = '';
        const $new = cheerio.load(newHtml);
        $new('script').each((i, el) => { jsContent += $new(el).html() + '\n'; });
        if (jsContent.trim()) {
            fs.writeFileSync('temp_script_verify.js', jsContent);
            try {
                execSync('node -c temp_script_verify.js', { stdio: 'pipe' });
                console.log(`JS fixed and verified: ${file}`);
            } catch (e) {
                console.error(`JS_ERROR in ${file}:`, e.stderr.toString());
            }
        }
    }
}

if (fs.existsSync('temp_script_verify.js')) fs.unlinkSync('temp_script_verify.js');
console.log(`Total JS fixed: ${fixedCount}`);
