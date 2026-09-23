const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const scriptRegex = /<script\b[^>]*>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
while ((match = scriptRegex.exec(html)) !== null) {
  count++;
  const code = match[1];
  if (!code.trim()) continue;
  try {
    new Function(code);
  } catch (e) {
    console.error(`Syntax error in script block ${count}:`, e.message);
  }
}
console.log(`Checked ${count} script blocks.`);
