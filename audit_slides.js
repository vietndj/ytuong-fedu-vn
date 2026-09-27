const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const files = fs.readdirSync('reports').filter(f => f.endsWith('.html'));
const results = [];

for(const f of files) {
  const html = fs.readFileSync(path.join('reports', f), 'utf8');
  const $ = cheerio.load(html);
  // Find the actual carousel-stack div
  const stack = $('div.carousel-stack').first();
  const iframes = stack.find('iframe').length;
  const videos = stack.find('video').length;
  const imgs = stack.find('img').length;
  const total = iframes + videos + imgs;
  if(total > 1) results.push({ f: f.replace('.html',''), iframes, videos, imgs, total });
}

results.sort((a,b) => a.iframes - b.iframes);
results.forEach(r => {
  const status = r.iframes > 1 ? '✅ HAS_YT' : '⚠️  NEEDS_YT';
  console.log(status + ' | slides:' + r.total + ' (vid:'+r.videos+' img:'+r.imgs+' yt:'+r.iframes+') | ' + r.f);
});
