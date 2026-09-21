const fs = require('fs');

let content = fs.readFileSync('ideas_data.js', 'utf8');

// The file defines var FEDU_IDEAS_DATABASE = { ... }
// We can just replace "https://placehold.co/... " with ""
content = content.replace(/"https:\/\/placehold\.co\/[^"]*"/g, '""');

fs.writeFileSync('ideas_data.js', content, 'utf8');
console.log('Fixed placeholders in ideas_data.js');
