const fs = require('fs');
let code = fs.readFileSync('functions/api/video.js', 'utf8');
code = code.replace(/newHeaders\.set\('access-control-allow-origin', '\*'\);/, "newHeaders.set('access-control-allow-origin', '*');\n  newHeaders.set('X-Fedu-Proxy', 'v3');");
fs.writeFileSync('functions/api/video.js', code);
