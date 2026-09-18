def fix(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_tag = '<!-- Ngành Badge -->'
    end_tag = '<!-- Kiểu quay Badge -->'
    
    import re
    
    new_badge_block = r'''<!-- Ngành Badge -->
                                ${(item.industries || []).map(ind => {
                                    const c = getBadgeColorClasses(ind.badge_color || 'sky');
                                    const isIndActive = appState.currentIndustry === ind.id;
                                    return `<button onclick="event.stopPropagation(); selectIndustry('${ind.id}')"
                                        class="px-1.5 py-0.5 rounded text-[9px] uppercase tracking-wide font-bold border transition cursor-pointer hover:scale-105 active:scale-95 flex items-center gap-1 ${isIndActive ? 'bg-sky-500 text-white border-sky-400 shadow-md shadow-sky-500/30 ring-1 ring-sky-300/60' : `${c} opacity-80 hover:opacity-100`}"
                                        title="Lọc theo ngành: ${escapeHtml(ind.name)}">
                                        <span>${ind.icon}</span>
                                        <span>${escapeHtml(ind.name)}</span>
                                    </button>`;
                                }).join('')}

                                <!-- Kiểu quay Badge -->'''
                                
    content = re.sub(r'<!-- Ngành Badge -->.*?<!-- Kiểu quay Badge -->', new_badge_block, content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

fix('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ytuong.html')
fix('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html')
