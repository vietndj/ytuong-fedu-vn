import os

idx_path = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/dist/index.html"
with open(idx_path, "r") as f:
    html = f.read()

target = 'id="videoModalShareBtn"'
replacement = '''id="videoModalDownloadOriginalBtn" href="#" target="_blank" class="hidden px-2.5 py-1.5 bg-indigo-500/20 text-indigo-300 hover:bg-indigo-500 hover:text-white rounded-lg text-xs font-bold transition items-center gap-1.5 cursor-pointer">
                            📥 Tải bản gốc (G-Drive)
                        </a>
                    <button 
                        id="videoModalShareBtn"'''
html = html.replace(target, replacement)
with open(idx_path, "w") as f:
    f.write(html)
print("Injected!")
