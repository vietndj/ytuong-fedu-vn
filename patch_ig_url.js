const fs = require('fs');
let content = fs.readFileSync('process_report.js', 'utf8');
content = content.replace(
    "if (!igUrl) {",
    `
    // Try to extract from filename shortcode
    const shortcodeMatch = fileName.match(/_([a-zA-Z0-9_-]{11})_/);
    if (shortcodeMatch) {
        igUrl = "https://www.instagram.com/p/" + shortcodeMatch[1] + "/";
    }
    
if (!igUrl || !igUrl.includes('/p/') && !igUrl.includes('/reel')) {`
);
fs.writeFileSync('process_report.js', content);
