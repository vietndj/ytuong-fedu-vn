import re

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Ẩn Logo
content = content.replace('<div class="relative group">', '<div class="relative group hidden">', 1)

# 2. Đổi tên Accordion Summary
content = content.replace('Tìm kiếm & Bộ lọc (Nhấn để mở)', 'Menu & Bộ lọc')

# 3. Thu gọn Ô tìm kiếm + Bộ lọc thứ cấp vào details
# Cắt phần Ô tìm kiếm và Bộ lọc từ main
start_main = content.find('<!-- PROMINENT UNIVERSAL SEARCH BAR')
end_main = content.find('<!-- VIEW 1: IDEAS GRID')
if start_main != -1 and end_main != -1:
    moved_block = content[start_main:end_main]
    content = content[:start_main] + content[end_main:]
    
    # Chèn vào trong details, cụ thể là sau thẻ </header>
    end_header = content.find('</header>')
    if end_header != -1:
        insert_pos = end_header + len('</header>')
        # wrap moved_block inside a div with max-w-7xl for alignment if needed?
        # Since it was in main which has max-w-7xl mx-auto, I should wrap it or just paste it since it's already well formatted.
        # But wait, main has px-4 sm:px-6 lg:px-8. Let's just wrap it.
        wrap_block = f"""
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4">
            {moved_block.strip()}
        </div>
"""
        content = content[:insert_pos] + wrap_block + content[insert_pos:]

# 4. Tải video inside videoPlayerModal
content = content.replace('Tải Về', 'Tải Video')

# 5. Đổi tên nút Follow
content = content.replace('<span>Xem Bản Gốc</span>', '<span>Theo dõi</span>')
content = content.replace('title="Xem Bản Gốc trên Instagram"', 'title="Theo dõi trên Instagram"')

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

