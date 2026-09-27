const fs = require('fs');

const results = JSON.parse(fs.readFileSync('batch_results.json', 'utf8'));

let md = "| # | Tên | Số slide | YouTube IDs | JS Error | Vision | Link Live |\n";
md += "|---|---|---|---|---|---|---|\n";

results.forEach((r, i) => {
    let slide = r.slides || '-';
    let ytIds = r.ytIds ? r.ytIds.split(',').map(id => id.substring(0,6)+'...').join(', ') : '-';
    let jsErr = r.jsError || '-';
    let vision = r.status.includes('timeout') ? '❌ Bỏ qua (Do Deploy timeout)' : (r.status === 'Processed' ? '✅ Đạt' : '-');
    let statusText = r.status === 'Processed' ? `[Live URL](https://ytuong.fedu.vn/reports/${encodeURI(r.name)})` : r.status;
    
    // Fallback link if skipped
    if(statusText.includes('không cần sửa') || statusText.includes('Không có link') || statusText.includes('timeout')) {
       statusText = `${r.status} <br> [Live URL](https://ytuong.fedu.vn/reports/${encodeURI(r.name)})`;
    }

    md += `| ${i+1} | ${r.name} | ${slide} | ${ytIds} | ${jsErr} | ${vision} | ${statusText} |\n`;
});

fs.writeFileSync('final_table.md', md);
