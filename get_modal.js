const fs = require('fs');
const html = fs.readFileSync('dist/index.html', 'utf8');
const match = html.match(/function openReportModal[\s\S]+?<\/script>/);
console.log(match ? match[0].substring(0, 1500) : "Not found");
