import re
with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html', 'r') as f:
    content = f.read()

# The admin bar HTML
admin_bar_html = """
    <!-- Admin Curation Bar -->
    <div id="curationAdminBar" class="hidden bg-slate-900/95 border-t border-b border-amber-500/40 px-4 py-1.5 text-xs text-amber-200 flex items-center justify-between flex-wrap gap-2 shadow-md">
        <div class="flex items-center gap-2">
            <span class="px-2 py-0.5 rounded bg-amber-500 text-slate-950 font-black text-[11px]">⚙️ QUẢN TRỊ</span>
            <span class="text-[11px] text-amber-300 font-semibold hidden sm:inline">🟡 Thẻ viền vàng = Đã ẩn khỏi học viên</span>
        </div>
        <div class="flex items-center gap-1.5 flex-wrap">
            <button onclick="exportCurationConfig()" class="px-2.5 py-1 rounded-lg bg-emerald-500 text-slate-950 font-bold text-xs shadow-sm cursor-pointer">Export Cấu Hình (JSON)</button>
            <button onclick="lockAdminMode()" class="px-2.5 py-1 rounded-lg bg-rose-500/20 text-rose-300 border border-rose-500/40 hover:bg-rose-500/30 text-xs font-semibold ml-1 cursor-pointer">🔒 Thoát</button>
        </div>
    </div>
"""

# Insert right after </header>
content = content.replace("</header>", "</header>\n" + admin_bar_html)

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html', 'w') as f:
    f.write(content)
