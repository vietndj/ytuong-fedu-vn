import re

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html', 'r') as f:
    content = f.read()

toast_html = """
    <!-- Global Toast Notification -->
    <div id="toastNotification" class="fixed bottom-6 right-6 z-50 px-4 py-3 rounded-2xl bg-slate-900/95 text-slate-100 text-sm font-semibold border border-slate-700 shadow-2xl backdrop-blur-md flex items-center gap-2 transform translate-y-12 opacity-0 pointer-events-none transition-all duration-300">
        <span id="toastIcon">✅</span>
        <span id="toastMsg">Thành công!</span>
    </div>
"""

if 'id="toastNotification"' not in content:
    content = content.replace('</body>', toast_html + '\n</body>')

# Also, there are two `showToast` functions. Let's delete the first one to avoid confusion.
content = re.sub(r'function showToast\(msg\) \{[\s\S]*?clearTimeout\(toast\._timeout\);[\s\S]*?\}', '', content, count=1)

with open('/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html', 'w') as f:
    f.write(content)
print("Toast restored!")
