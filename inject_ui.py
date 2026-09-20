import os

idx_path = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/dist/index.html"
with open(idx_path, "r") as f:
    html = f.read()

# Tim header modal de them nut
target = 'class="flex items-center gap-1.5 sm:gap-2 shrink-0">'
if 'id="videoModalDownloadOriginalBtn"' not in html:
    replacement = target + '''
                        <!-- Nút Tải Bản Gốc -->
                        <a id="videoModalDownloadOriginalBtn" href="#" target="_blank" class="hidden px-2 py-1 bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 rounded-lg text-xs font-bold hover:bg-indigo-500 hover:text-white transition items-center gap-1">
                            📥 Tải bản gốc (G-Drive)
                        </a>'''
    html = html.replace(target, replacement)
    
# Cap nhat logic JS
target_js = 'const title = document.getElementById(\'videoModalTitle\');'
if 'const downloadBtn = document.getElementById(\'videoModalDownloadOriginalBtn\');' not in html:
    replacement_js = target_js + '''
            const downloadBtn = document.getElementById('videoModalDownloadOriginalBtn');
            if (downloadBtn) {
                if (item.video_url_original) {
                    downloadBtn.href = item.video_url_original;
                    downloadBtn.classList.remove('hidden');
                    downloadBtn.classList.add('flex');
                } else {
                    downloadBtn.href = "#";
                    downloadBtn.classList.add('hidden');
                    downloadBtn.classList.remove('flex');
                }
            }'''
    html = html.replace(target_js, replacement_js)

with open(idx_path, "w") as f:
    f.write(html)

print("Injected UI button.")
