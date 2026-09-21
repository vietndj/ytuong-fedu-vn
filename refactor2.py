import re

FILES = [
    '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/dist/index.html',
    '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/index.html',
    '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/dist/ytuong.html',
    '/Users/vietmac/Documents/CODE/ytuong-fedu-vn/ytuong.html'
]

AVATAR_OLD = """<button 
                                    type="button"
                                    onclick="event.stopPropagation(); filterByCreator('${escapeJs(item.creator.handle)}', '${escapeJs(item.creator.name)}')"
                                    class="shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-slate-800 border border-slate-700 text-sm hover:border-sky-400 hover:bg-sky-500/10 hover:scale-105 transition cursor-pointer group"
                                    title="Lọc video của: ${escapeHtml(authorDisplayName)}"
                                >
                                    <span class="group-hover:hidden">👤</span>
                                    <span class="hidden group-hover:block text-sky-400">🔍</span>
                                </button>"""

AVATAR_NEW = """<a href="${igReelsUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" class="shrink-0 flex items-center justify-center w-8 h-8 rounded-full bg-slate-800 border border-slate-700 text-sm hover:border-pink-500 hover:bg-pink-500/10 hover:scale-105 transition" title="Xem Instagram Reels của ${escapeHtml(authorDisplayName)}">
                                    <span>👤</span>
                                </a>"""

NAME_OLD = """<button 
                                            type="button"
                                            onclick="event.stopPropagation(); filterByCreator('${escapeJs(item.creator.handle)}', '${escapeJs(item.creator.name)}')"
                                            class="font-bold text-sm text-white truncate hover:text-sky-400 transition" 
                                            title="Lọc tác giả: ${escapeHtml(authorDisplayName)}"
                                        >
                                            ${escapeHtml(authorDisplayName)}
                                        </button>"""

NAME_NEW = """<a href="${igReelsUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" class="font-bold text-sm text-white truncate hover:text-pink-400 hover:underline transition">
                                            ${escapeHtml(authorDisplayName)}
                                        </a>"""

INSTA_OLD = """<a href="${igPostUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" class="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white font-bold text-xs shadow-lg shadow-pink-500/20 border border-pink-500/50 hover:scale-105 transition">
                                        <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.012-3.584.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
                                        Theo dõi
                                    </a>"""
INSTA_NEW = """<a href="${item.ig_url || igPostUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation();" class="flex items-center justify-center h-8 w-8 rounded-lg bg-slate-800 border border-slate-700 hover:border-pink-500 hover:bg-pink-500/20 transition group" title="Xem video gốc trên Instagram">
                                        <svg class="w-4 h-4 text-slate-300 group-hover:text-pink-400" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.012-3.584.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
                                    </a>"""

for f in FILES:
    with open(f, 'r') as fp:
        c = fp.read()
    c = c.replace(AVATAR_OLD, AVATAR_NEW)
    c = c.replace(NAME_OLD, NAME_NEW)
    c = c.replace(INSTA_OLD, INSTA_NEW)
    with open(f, 'w') as fp:
        fp.write(c)

