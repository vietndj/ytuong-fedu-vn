import re

def fix(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_block = r'''<button\s*type="button"\s*onclick="event\.stopPropagation\(\); selectIndustry\('\$\{item\.industry\.id\}'\)"\s*class="[^"]*"\s*title="Lọc theo ngành: \$\{escapeHtml\(item\.industry\.name\)\}"\s*>\s*<span>\$\{item\.industry\.icon\}</span>\s*<span>\$\{escapeHtml\(item\.industry\.name\)\}</span>\s*</button>'''
    
    new_block = r'''${(item.industries || []).map(ind => {
                                    const c = getBadgeColorClasses(ind.badge_color || 'sky');
                                    const isIndActive = appState.currentIndustry === ind.id;
                                    return `<button type="button" onclick="event.stopPropagation(); selectIndustry('${ind.id}')"
                                        class="px-1.5 py-0.5 rounded text-[9px] uppercase tracking-wide font-bold border transition cursor-pointer hover:scale-105 active:scale-95 flex items-center gap-1 ${isIndActive ? 'bg-sky-500 text-white border-sky-400 shadow-md shadow-sky-500/30 ring-1 ring-sky-300/60' : `${c} opacity-80 hover:opacity-100`}"
                                        title="Lọc theo ngành: ${escapeHtml(ind.name)}">
                                        <span>${ind.icon}</span>
                                        <span>${escapeHtml(ind.name)}</span>
                                    </button>`;
                                }).join('')}'''
                                
    content = re.sub(old_block, new_block, content)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

fix('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ytuong.html')
fix('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html')
