const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
while ((match = scriptRegex.exec(html)) !== null) {
  count++;
  if (count === 5) {
    fs.writeFileSync('block5.js', match[1]);
    console.log('Wrote block5.js');
  }
}
