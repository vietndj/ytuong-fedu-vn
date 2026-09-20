import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Bọc toàn bộ Header / top bar vào thẻ <details>
# Tìm phần Header
start_header = html.find('<header class="')
if start_header != -1:
    end_header = html.find('</header>', start_header) + len('</header>')
    header_content = html[start_header:end_header]
    
    # Bọc nó lại
    new_header = f"""
    <details class="w-full bg-slate-950 border-b border-slate-800/60 sticky top-0 z-40 group [&_summary::-webkit-details-marker]:hidden">
        <summary class="flex items-center justify-between px-4 py-3 cursor-pointer text-slate-300 font-bold text-sm bg-slate-900">
            <div class="flex items-center gap-2">
                <span class="text-sky-400">🔍</span> Tìm kiếm & Bộ lọc (Nhấn để mở)
            </div>
            <span class="group-open:rotate-180 transition-transform">▼</span>
        </summary>
        <div class="p-2 border-t border-slate-800/50 bg-slate-950">
            {header_content}
        </div>
    </details>
    """
    
    # Thay thế header cũ bằng details. (Khéo bị hỏng sticky nếu header_content có class sticky)
    header_clean = header_content.replace('sticky top-0 z-40', 'relative')
    new_header = new_header.replace('{header_content}', header_clean)
    
    html = html.replace(header_content, new_header)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Đã gom Header thành Accordion")
else:
    print("Không tìm thấy thẻ <header>")
