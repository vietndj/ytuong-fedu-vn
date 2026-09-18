import re

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # badgeColorClass and isIndActive definitions
    content = re.sub(
        r'const badgeColorClass = getBadgeColorClasses\(item\.industry\.badge_color\);\s*const compId',
        r'const compId',
        content
    )
    content = re.sub(
        r'const isIndActive = appState\.currentIndustry === item\.industry\.id;\s*const isCountryActive',
        r'const isCountryActive',
        content
    )

    # Industry Badge Block in the UI
    old_badge_block = r'''<button onclick="event\.stopPropagation\(\); selectIndustry\('\$\{item\.industry\.id\}'\)"[^>]*>.*?<span>\$\{item\.industry\.icon\}</span>.*?<span>\$\{escapeHtml\(item\.industry\.name\)\}</span>.*?</button>'''
    
    new_badge_block = r'''${(item.industries || []).map(ind => {
                                    const c = getBadgeColorClasses(ind.badge_color || 'sky');
                                    const isIndActive = appState.currentIndustry === ind.id;
                                    return `<button onclick="event.stopPropagation(); selectIndustry('${ind.id}')"
                                        class="px-1.5 py-0.5 rounded text-[9px] uppercase tracking-wide font-bold border transition cursor-pointer hover:scale-105 active:scale-95 flex items-center gap-1 ${isIndActive ? 'bg-sky-500 text-white border-sky-400 shadow-md shadow-sky-500/30 ring-1 ring-sky-300/60' : `${c} opacity-80 hover:opacity-100`}"
                                        title="Lọc theo ngành: ${escapeHtml(ind.name)}">
                                        <span>${ind.icon}</span>
                                        <span>${escapeHtml(ind.name)}</span>
                                    </button>`;
                                }).join('')}'''

    content = re.sub(old_badge_block, new_badge_block, content, flags=re.DOTALL)

    # <option value="${ind.id}" ${item.industry?.id === ind.id ? 'selected' : ''}>${ind.icon} ${ind.name}</option>
    content = re.sub(
        r'\$\{item\.industry\?\.id === ind\.id \? \'selected\' : \'\'\}',
        r'${(item.industries || []).some(i => i.id === ind.id) ? "selected" : ""}',
        content
    )

    # const indObj = window.FEDU_IDEAS_DATABASE.industries.find(i => i.id === newIndustryId) || item.industry;
    content = re.sub(
        r'\|\| item\.industry;',
        r'|| (item.industries ? item.industries[0] : null);',
        content
    )
    
    # item.industry = indObj;
    content = re.sub(
        r'item\.industry = indObj;',
        r'item.industries = [indObj];',
        content
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ytuong.html')
fix_file('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html')
