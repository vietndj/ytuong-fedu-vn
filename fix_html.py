import os
import re

def fix_file(path):
    with open(path, 'r') as f:
        html = f.read()

    btn_html = '''
                    <a id="videoModalDownloadOriginalBtn" href="#" target="_blank" class="hidden px-2.5 py-1.5 rounded-lg bg-indigo-500/20 text-indigo-300 hover:bg-indigo-500 hover:text-white transition items-center gap-1.5 font-bold text-xs cursor-pointer" title="Tải bản gốc từ Google Drive">
                        <span>📥</span>
                        <span class="hidden sm:inline">Bản Gốc</span>
                    </a>
'''
    if 'videoModalDownloadOriginalBtn' not in html:
        # insert before the share btn
        html = html.replace('<!-- Copy Share Link Button -->', '<!-- Copy Share Link Button -->' + btn_html)
        
    js_code = '''
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
            }
'''
    if "const downloadBtn = document.getElementById('videoModalDownloadOriginalBtn');" not in html:
        html = html.replace("const title = document.getElementById('videoModalTitle');", "const title = document.getElementById('videoModalTitle');" + js_code)
        
    with open(path, 'w') as f:
        f.write(html)
        
fix_file("index.html")
fix_file("ytuong.html")
