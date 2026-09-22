import re

# Read original JS
with open('js_block.txt', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Replace heroSearchInput with globalSearchInput
js_content = js_content.replace("'heroSearchInput'", "'globalSearchInput'")

# Add Intersection Observer at the end
observer_js = """
// Infinite Scroll using IntersectionObserver
document.addEventListener('DOMContentLoaded', () => {
    const sentinel = document.getElementById('paginationBar');
    if (sentinel) {
        const observer = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !sentinel.classList.contains('hidden')) {
                loadMoreIdeas();
            }
        }, { rootMargin: '200px' });
        observer.observe(sentinel);
    }
});
"""
js_content += observer_js

html_template = f"""<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Kho Ý Tưởng Video | ytuong.fedu.vn</title>
    
    <!-- Google Fonts Preconnect -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://media.fedu.vn">
    
    <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    fontFamily: {{
                        sans: ['"Be Vietnam Pro"', 'sans-serif']
                    }}
                }}
            }}
        }}
    </script>
    
    <style>
        :root {{
            --bg-main: #070a0f;
        }}
        body {{
            background-color: var(--bg-main);
            color: #f1f5f9;
            font-family: 'Be Vietnam Pro', sans-serif;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
        }}
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: #070a0f; }}
        ::-webkit-scrollbar-thumb {{ background: #1e293b; border-radius: 4px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #38bdf8; }}

        /* Glass Header */
        .glass-header {{
            background: rgba(11, 15, 23, 0.9);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.07);
        }}
        
        /* Shooting Style Tab Active */
        .style-tab.active {{
            background: rgba(255,255,255,0.1);
            color: #ffffff;
            font-weight: 700;
        }}
        
        /* Search Input Toggle */
        #globalSearchContainer.hidden-search {{ display: none; }}
        
        /* Modals */
        .app-modal-backdrop {{
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(3, 7, 18, 0.88);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            z-index: 9999;
        }}
        body.modal-open {{ overflow: hidden; }}
        
        /* Poster 9:16 Aspect Ratio */
        .aspect-poster {{
            aspect-ratio: 9 / 16;
        }}
        
        /* Hide scrollbar for horizontal scrolling tabs */
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
        .no-scrollbar {{ -ms-overflow-style: none; scrollbar-width: none; }}
    </style>
</head>
<body class="text-slate-200">
    <!-- HEADER 48px -->
    <header class="glass-header fixed top-0 w-full z-50 h-[44px] md:h-[48px] flex items-center px-2 md:px-4 gap-2">
        <div class="text-sm font-bold shrink-0 flex items-center gap-2">
            🎬 <span class="hidden md:inline">Kho Ý Tưởng</span>
        </div>
        
        <!-- Shooting Styles Tabs (Horizontal Scroll) -->
        <div id="shootingStyleTabsContainer" class="flex-1 flex items-center overflow-x-auto no-scrollbar gap-1 px-2 h-full py-1">
            <!-- Tabs will be rendered here by JS -->
        </div>
        
        <!-- Search Toggle -->
        <button onclick="document.getElementById('globalSearchContainer').classList.toggle('hidden-search')" class="p-2 hover:bg-white/10 rounded-lg shrink-0">
            🔍
        </button>
        <div id="globalSearchContainer" class="hidden-search absolute top-full right-0 mt-1 mr-2 bg-slate-900 border border-slate-700 p-2 rounded-lg shadow-xl">
            <input type="text" id="globalSearchInput" placeholder="Tìm kiếm..." class="bg-slate-800 text-sm px-3 py-1.5 rounded outline-none border border-slate-700 focus:border-sky-500 w-48">
        </div>
        
        <!-- Settings/Filters Dropdown (⚙️) -->
        <div class="relative group shrink-0">
            <button class="p-2 hover:bg-white/10 rounded-lg">⚙️</button>
            <div class="absolute right-0 top-full mt-1 w-64 bg-slate-900 border border-slate-700 rounded-xl shadow-2xl hidden group-hover:block p-4 z-50 max-h-[80vh] overflow-y-auto">
                <div class="text-xs font-semibold text-slate-400 mb-2">NGÀNH HÀNG</div>
                <div id="industryPillsContainer" class="flex flex-wrap gap-1 mb-4"></div>
                
                <div class="text-xs font-semibold text-slate-400 mb-2">QUỐC GIA</div>
                <div id="countryTabsContainer" class="flex flex-wrap gap-1 mb-4"></div>
                
                <div class="text-xs font-semibold text-slate-400 mb-2">ĐỘ KHÓ (CHUYỂN CẢNH)</div>
                <div id="transitionFilterContainer" class="flex flex-col gap-1 mb-4 text-sm">
                    <button id="btnTransitionAll" onclick="appState.currentTransitionLevel='all'; applyFilters(true)" class="text-left px-2 py-1 rounded hover:bg-white/5">Tất cả</button>
                    <button id="btnTransitionL1" onclick="appState.currentTransitionLevel='Chuyển cảnh Level 1'; applyFilters(true)" class="text-left px-2 py-1 rounded hover:bg-white/5">Cơ bản (C1)</button>
                    <button id="btnTransitionL2" onclick="appState.currentTransitionLevel='Chuyển cảnh Level 2'; applyFilters(true)" class="text-left px-2 py-1 rounded hover:bg-white/5">Nâng cao (C2)</button>
                </div>
                
                <hr class="border-slate-700 my-2">
                <button id="quickResetFiltersBtn" onclick="resetAllFilters()" class="w-full text-center text-sm py-1.5 bg-rose-500/20 text-rose-400 rounded hover:bg-rose-500/30 mb-2">Làm mới (Reset)</button>
                <button onclick="requestAdminAccess()" class="w-full text-center text-sm py-1.5 bg-amber-500/20 text-amber-400 rounded hover:bg-amber-500/30">Chế độ Admin</button>
            </div>
        </div>
    </header>

    <!-- GRID AREA (Starts right under header) -->
    <main class="pt-[44px] md:pt-[48px] min-h-screen">
        <div class="p-2 md:p-4 max-w-[1920px] mx-auto">
            <!-- Empty State -->
            <div id="emptyState" class="hidden text-center py-20 text-slate-500">
                Không tìm thấy ý tưởng nào phù hợp.
            </div>
            
            <!-- Grid -->
            <div id="ideasCardsGrid" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3 md:gap-4">
                <!-- Cards rendered by JS -->
            </div>
            
            <!-- Sentinel for Infinite Scroll -->
            <div id="paginationBar" class="h-10 w-full flex items-center justify-center mt-4">
                <div class="w-6 h-6 border-2 border-sky-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
        </div>
    </main>

    <!-- 6 MODALS -->
    <!-- 1. Video Player Modal -->
    <div id="videoPlayerModal" class="app-modal-backdrop flex items-center justify-center p-2 md:p-4">
        <div class="bg-slate-900 rounded-xl max-w-lg w-full overflow-hidden border border-slate-700 relative flex flex-col max-h-[95vh]">
            <button onclick="closeVideoModal()" class="absolute top-2 right-2 w-10 h-10 bg-black/50 rounded-full text-white z-10 flex items-center justify-center hover:bg-red-500 transition">✕</button>
            <div class="p-3 border-b border-slate-800 bg-slate-900 z-10">
                <h3 id="videoModalTitle" class="font-semibold truncate">Video</h3>
            </div>
            <div class="relative w-full bg-black flex-1 flex items-center justify-center min-h-0" style="aspect-ratio: 9/16;">
                <video id="modalActiveVideo" controls playsinline class="w-full h-full object-contain hidden"></video>
                <iframe id="modalActiveYoutube" class="w-full h-full hidden" frameborder="0" allowfullscreen></iframe>
            </div>
            <div class="p-3 bg-slate-900 border-t border-slate-800 flex justify-between z-10">
                <button id="videoModalCreatorBtn" class="text-sm text-sky-400 hover:underline truncate">Creator</button>
                <a id="videoModalDirectLink" href="#" target="_blank" class="text-sm bg-sky-600 hover:bg-sky-500 text-white px-3 py-1 rounded">Mở Link Gốc</a>
            </div>
        </div>
    </div>

    <!-- 2. Report Embed Modal -->
    <div id="reportEmbedModal" class="app-modal-backdrop flex items-center justify-center p-2 md:p-4">
        <div class="bg-slate-900 rounded-xl w-full max-w-4xl h-[90vh] overflow-hidden border border-slate-700 relative flex flex-col">
            <button onclick="closeReportModal()" class="absolute top-2 right-2 w-10 h-10 bg-black/50 rounded-full text-white z-10 flex items-center justify-center hover:bg-red-500 transition">✕</button>
            <div class="p-3 border-b border-slate-800 flex items-center gap-3">
                <span class="bg-sky-500/20 text-sky-400 text-xs px-2 py-1 rounded font-bold">REPORT</span>
                <h3 id="reportModalTitle" class="font-semibold truncate text-sm">Báo cáo</h3>
            </div>
            <div class="flex-1 relative bg-slate-950">
                <div id="reportIframeSpinner" class="absolute inset-0 flex items-center justify-center">
                    <div class="w-8 h-8 border-4 border-sky-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
                <iframe id="reportModalIframe" class="w-full h-full absolute inset-0 z-10" frameborder="0" onload="hideReportSpinner()"></iframe>
            </div>
        </div>
    </div>

    <!-- 3. Image Lightbox Modal -->
    <div id="imgLightboxModal" class="app-modal-backdrop flex items-center justify-center p-2 md:p-4">
        <div class="relative max-w-4xl w-full h-[90vh] flex flex-col items-center justify-center">
            <button onclick="closeImgLightbox()" class="absolute top-0 right-0 w-10 h-10 bg-black/50 rounded-full text-white z-10 flex items-center justify-center hover:bg-red-500 transition">✕</button>
            <img id="lightboxLargeImg" src="" class="max-w-full max-h-[80vh] object-contain rounded-lg">
            <p id="lightboxCaption" class="mt-4 text-center text-slate-300 text-sm"></p>
        </div>
    </div>

    <!-- 4. Admin Auth Modal -->
    <div id="adminAuthModal" class="app-modal-backdrop flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-700 p-6 rounded-xl w-full max-w-sm relative">
            <button onclick="closeAdminAuthModal()" class="absolute top-2 right-2 w-8 h-8 text-slate-400 hover:text-white flex items-center justify-center">✕</button>
            <h3 class="text-xl font-bold mb-4 text-amber-500">🔒 Admin Access</h3>
            <input type="password" id="adminPasswordInput" placeholder="Nhập mã PIN" class="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white mb-2" onkeydown="if(event.key==='Enter') submitAdminPassword()">
            <div id="adminPasswordError" class="hidden text-red-400 text-sm mb-3"><span id="adminPasswordErrorText">Sai mật khẩu!</span></div>
            <button onclick="submitAdminPassword()" class="w-full bg-amber-600 hover:bg-amber-500 text-white font-bold py-2 rounded">Xác nhận</button>
        </div>
    </div>

    <!-- 5. Edit Idea Modal -->
    <div id="editIdeaModal" class="app-modal-backdrop flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-2xl max-h-[90vh] flex flex-col">
            <div class="p-4 border-b border-slate-700 flex justify-between items-center shrink-0">
                <h3 class="font-bold text-lg">Chỉnh sửa Video</h3>
                <button onclick="closeEditIdeaModal()" class="w-8 h-8 text-slate-400 hover:text-white flex items-center justify-center">✕</button>
            </div>
            <div class="p-4 overflow-y-auto flex-1 text-sm space-y-3">
                <input type="hidden" id="editIdeaId">
                <div>
                    <label class="block text-slate-400 mb-1">Tiêu đề</label>
                    <input type="text" id="editIdeaTitle" class="w-full bg-slate-800 border border-slate-700 rounded p-2">
                </div>
                <div>
                    <label class="block text-slate-400 mb-1">Creator Name</label>
                    <input type="text" id="editIdeaCreatorName" class="w-full bg-slate-800 border border-slate-700 rounded p-2">
                </div>
                <div class="flex items-center gap-2 mt-2">
                    <input type="checkbox" id="editIdeaExcluded" class="w-4 h-4">
                    <label for="editIdeaExcluded" class="text-amber-400 font-semibold">Ẩn video này khỏi User (Chỉ Admin thấy)</label>
                </div>
                <!-- Other fields omitted for brevity but they are handled gracefully by JS if not found -->
                <div class="text-xs text-slate-500 mt-4">* Các trường khác đã được tinh giản trong form này. Chỉnh sửa chuyên sâu hãy dùng mã nguồn.</div>
            </div>
            <div class="p-4 border-t border-slate-700 flex justify-end gap-2 shrink-0">
                <button onclick="closeEditIdeaModal()" class="px-4 py-2 bg-slate-700 rounded hover:bg-slate-600">Hủy</button>
                <button onclick="saveEditedIdea()" class="px-4 py-2 bg-emerald-600 text-white rounded hover:bg-emerald-500">Lưu thay đổi</button>
            </div>
        </div>
    </div>

    <!-- 6. Delete Idea Modal -->
    <div id="deleteIdeaModal" class="app-modal-backdrop flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-red-500/30 rounded-xl w-full max-w-sm p-6 relative">
            <button onclick="closeDeleteIdeaModal()" class="absolute top-2 right-2 w-8 h-8 text-slate-400 hover:text-white flex items-center justify-center">✕</button>
            <h3 class="text-xl font-bold text-red-500 mb-2">Xác nhận xóa?</h3>
            <p class="text-sm text-slate-300 mb-4">Bạn có chắc chắn muốn xóa video <strong id="deleteIdeaTitleDisplay"></strong> khỏi phiên này không?</p>
            <input type="hidden" id="deleteIdeaTargetId">
            <div class="flex gap-2 justify-end">
                <button onclick="closeDeleteIdeaModal()" class="px-4 py-2 bg-slate-700 rounded hover:bg-slate-600">Hủy</button>
                <button onclick="confirmDeleteIdea()" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-500">Xóa Ngay</button>
            </div>
        </div>
    </div>

    <script src="ideas_data.js"></script>
    <script>
{js_content}
    </script>
    
    <!-- Modal Close Logic -->
    <script>
        // Modal interaction enhancements (close on backdrop click, swipe, esc)
        document.querySelectorAll('.app-modal-backdrop').forEach(modal => {{
            modal.addEventListener('click', e => {{
                if (e.target === modal) {{
                    const closeBtn = modal.querySelector('button[onclick^="close"]');
                    if (closeBtn) closeBtn.click();
                }}
            }});
            
            // Touch swipe down to close
            let touchStartY = 0;
            modal.addEventListener('touchstart', e => {{
                touchStartY = e.touches[0].clientY;
            }}, {{passive: true}});
            
            modal.addEventListener('touchend', e => {{
                const touchEndY = e.changedTouches[0].clientY;
                if (touchEndY - touchStartY > 100) {{ // swipe down threshold
                    const closeBtn = modal.querySelector('button[onclick^="close"]');
                    if (closeBtn) closeBtn.click();
                }}
            }}, {{passive: true}});
        }});
        
        document.addEventListener('keydown', e => {{
            if (e.key === 'Escape') {{
                document.querySelectorAll('.app-modal-backdrop').forEach(modal => {{
                    if (modal.style.display === 'flex' || !modal.classList.contains('hidden')) {{
                        const closeBtn = modal.querySelector('button[onclick^="close"]');
                        if (closeBtn) closeBtn.click();
                    }}
                }});
            }}
        }});
        
        // Prevent body scroll when modal open
        const originalOpenVideoModal = window.openVideoModal;
        window.openVideoModal = function(...args) {{
            if(originalOpenVideoModal) originalOpenVideoModal(...args);
            document.body.classList.add('modal-open');
        }};
        
        const originalCloseVideoModal = window.closeVideoModal;
        window.closeVideoModal = function(...args) {{
            if(originalCloseVideoModal) originalCloseVideoModal(...args);
            document.body.classList.remove('modal-open');
            // Pause video logic is already in original closeVideoModal
        }};
    </script>
</body>
</html>
"""

with open('index_v3.html', 'w', encoding='utf-8') as f:
    f.write(html_template)
print("Wrote index_v3.html")
