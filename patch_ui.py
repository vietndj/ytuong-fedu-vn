import re

def patch_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. UGC logic
    # (item.industry && item.industry.id === 'ugc')
    content = re.sub(
        r'\(item\.industry\s*&&\s*item\.industry\.id\s*===\s*\'ugc\'\)',
        r'(item.industries && item.industries.some(i => i.id === "ugc"))',
        content
    )
    # x.industry?.id === 'ugc' -> x.industries?.some(i => i.id === 'ugc')
    content = re.sub(
        r'x\.industry\?\.id\s*===\s*\'ugc\'',
        r'x.industries?.some(i => i.id === "ugc")',
        content
    )

    # 2. Filtering logic
    # if (!item.industry || item.industry.id !== appState.currentIndustry) return false;
    content = re.sub(
        r'if\s*\(!item\.industry\s*\|\|\s*item\.industry\.id\s*!==\s*appState\.currentIndustry\)\s*return\s*false;',
        r'if (!item.industries || !item.industries.some(i => i.id === appState.currentIndustry)) return false;',
        content
    )

    # 3. Search string building
    # (item.industry?.name || '')
    content = re.sub(
        r'\(item\.industry\?\.name\s*\|\|\s*\'\'\)',
        r'(item.industries?.map(i => i.name).join(" ") || "")',
        content
    )
    # (item.industry?.en_name || '')
    content = re.sub(
        r'\(item\.industry\?\.en_name\s*\|\|\s*\'\'\)',
        r'(item.industries?.map(i => i.en_name || "").join(" ") || "")',
        content
    )

    # 4. Rendering badges
    # We need to replace the single industry badge block with a map over item.industries
    badge_block_old = r'''<button class="bg-\$\{badgeColorClass\}-500/10 hover:bg-\$\{badgeColorClass\}-500/20 text-\$\{badgeColorClass\}-400 border border-\$\{badgeColorClass\}-500/20 px-2 py-0.5 rounded flex items-center gap-1.5 text-xs transition-colors"
                                    onclick="event.stopPropagation\(\); selectIndustry\('\$\{item.industry.id\}'\)"
                                    title="Lọc theo ngành: \$\{escapeHtml\(item.industry.name\)\}">
                                    <span>\$\{item.industry.icon\}</span>
                                    <span>\$\{escapeHtml\(item.industry.name\)\}</span>
                                </button>'''
    
    badge_block_new = r'''${(item.industries || []).map(ind => {
                                    const c = getBadgeColorClasses(ind.badge_color || 'indigo');
                                    const isAct = appState.currentIndustry === ind.id;
                                    return `<button class="bg-${c}-500/10 hover:bg-${c}-500/20 text-${c}-400 border border-${c}-500/20 px-2 py-0.5 rounded flex items-center gap-1.5 text-xs transition-colors ${isAct ? 'ring-1 ring-'+c+'-400' : ''}"
                                        onclick="event.stopPropagation(); selectIndustry('${ind.id}')"
                                        title="Lọc theo ngành: ${escapeHtml(ind.name)}">
                                        <span>${ind.icon}</span>
                                        <span>${escapeHtml(ind.name)}</span>
                                    </button>`;
                                }).join('')}'''
    
    content = re.sub(badge_block_old, badge_block_new, content)

    # X-Factor Rendering: append after purpose badge
    purpose_badge = r'''<span class="bg-white/5 border border-white/10 px-2 py-0.5 rounded text-xs text-slate-300">
                                    🎯 \$\{escapeHtml\(item.purpose_group || 'Chưa phân loại'\)\}
                                </span>'''
    
    x_factor_block = r'''<span class="bg-white/5 border border-white/10 px-2 py-0.5 rounded text-xs text-slate-300">
                                    🎯 ${escapeHtml(item.purpose_group || 'Chưa phân loại')}
                                </span>
                                ${(item.x_factors || []).map(x => `<span class="bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 px-2 py-0.5 rounded text-xs flex items-center gap-1">✨ ${escapeHtml(x)}</span>`).join('')}'''
    
    content = content.replace(purpose_badge, x_factor_block)

    # 5. Fix handleCardThumbError fallback icon
    # '${item.industry?.icon || '🎬'}'
    content = re.sub(
        r'\'\$\{item\.industry\?\.icon\s*\|\|\s*\'🎬\'\}\'',
        r"'${item.industries?.[0]?.icon || \"🎬\"}'",
        content
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

patch_file('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ytuong.html')
patch_file('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html')

