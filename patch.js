const fs = require('fs');
let content = fs.readFileSync('process_report.js', 'utf8');
content = content.replace(
    "jsContent += $(el).html() + '\\n';",
    "jsContent += $(el).html() + '\\n';\n});\njsContent = jsContent.replace(/if\\\\(player\\\\)\\\\s+player\\\\.currentTime\\\\s*=\\\\s*startTime;\\\\s*\\\\}/g, 'if(player) player.currentTime = startTime;');\nif (false) {"
);
fs.writeFileSync('process_report.js', content);
