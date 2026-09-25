const fs = require('fs');
const queue = JSON.parse(fs.readFileSync('audit_queue.json'));
let uniqueIds = new Set();
queue.forEach(item => {
    if (uniqueIds.has(item.id)) return;
    uniqueIds.add(item.id);
    
    let id = item.id;
    let creator = item.creator;
    let url = null;
    
    if (id.startsWith('IG_')) {
        const prefix = 'IG_' + creator + '_';
        if (id.startsWith(prefix)) {
            const remainder = id.substring(prefix.length);
            const match = remainder.match(/^([A-Za-z0-9_-]{11})(?:_|$)/);
            if (match) url = 'https://www.instagram.com/reel/' + match[1] + '/';
            else url = 'https://www.instagram.com/reel/' + remainder.split('_')[0] + '/';
        }
    } else if (id.startsWith('TT_')) {
        const prefix = 'TT_' + creator + '_';
        if (id.startsWith(prefix)) {
            const remainder = id.substring(prefix.length);
            const match = remainder.match(/^([0-9]{19})(?:_|$)/);
            if (match) url = 'https://www.tiktok.com/@' + creator.replace('@','') + '/video/' + match[1];
            else url = 'https://www.tiktok.com/@' + creator.replace('@','') + '/video/' + remainder.split('_')[0];
        }
    }
    
    if (url) console.log(url);
});
