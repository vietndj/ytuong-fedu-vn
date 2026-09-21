import re

FILES = [
    '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/dist/index.html',
    '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html',
    '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/dist/ytuong.html',
    '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ytuong.html'
]

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Thay avatar button
    content = re.sub(
        r'<button[^>]*?onclick="event\.stopPropagation\(\);\s*filterByCreator\([^\)]*\)"[^>]*?class="shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-slate-800 border border-slate-700 text-sm hover:border-sky-400 hover:bg-sky-500/10 hover:scale-105 transition cursor-pointer group"[^>]*?>\s*<span class="group-hover:hidden">👤</span>\s*<span class="hidden group-hover:block text-sky-400">🔍</span>\s*</button>',
        r'<a href="${igReelsUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" class="shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-slate-800 border border-slate-700 text-sm hover:border-pink-500 hover:bg-pink-500/10 hover:scale-105 transition" title="Xem Instagram Reels của ${escapeHtml(authorDisplayName)}">\n                                    <span>👤</span>\n                                </a>',
        content,
        flags=re.DOTALL
    )

    # 2. Thay Tên tác giả button
    content = re.sub(
        r'<button[^>]*?type="button"[^>]*?onclick="event\.stopPropagation\(\);\s*filterByCreator\([^\)]*\)"[^>]*?class="font-bold text-sm text-white truncate hover:text-sky-400 transition"[^>]*?>\s*\$\{escapeHtml\(authorDisplayName\)\}\s*</button>',
        r'<a href="${igReelsUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" class="font-bold text-sm text-white truncate hover:text-pink-400 hover:underline transition">\n                                            ${escapeHtml(authorDisplayName)}\n                                        </a>',
        content,
        flags=re.DOTALL
    )

    # 3. Thêm overlay vào Duo-Poster
    # The poster now has class: class="relative rounded-xl overflow-hidden aspect-poster bg-slate-900 group cursor-pointer border border-slate-800 hover:border-sky-500/50 transition duration-300" onclick="openReportModal(\'${item.id}\')" title="Bấm để xem báo cáo phân tích chi tiết">
    # Let's replace the <img right after this div to inject the overlay before the img.
    content = re.sub(
        r'(<div class="relative rounded-xl overflow-hidden aspect-poster bg-slate-900 group cursor-pointer border border-slate-800 hover:border-sky-500/50 transition duration-300" onclick="openReportModal\(\\\'\$\{item\.id\}\\\'\)" title="Bấm để xem báo cáo phân tích chi tiết">)\s*<img',
        r'\1\n                                    <!-- Hover Overlay: Báo Cáo -->\n                                    <div class="absolute inset-0 bg-slate-900/60 opacity-0 group-hover:opacity-100 transition duration-300 flex items-center justify-center z-20">\n                                        <span class="px-3 py-1.5 bg-slate-800/80 backdrop-blur-sm border border-slate-700 rounded-full text-xs font-bold text-white shadow-xl flex items-center gap-1.5 transform translate-y-2 group-hover:translate-y-0 transition-all duration-300">\n                                            📄 Xem Báo Cáo\n                                        </span>\n                                    </div>\n                                <img',
        content
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for f in FILES:
    try:
        process_file(f)
        print(f"Processed {f}")
    except Exception as e:
        print(f"Error processing {f}: {e}")

