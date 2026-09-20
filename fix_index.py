import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Nút Insta 404
# We need to hide it if ig_url is empty or '#'.
# The current template is:
# ${item.ig_url ? `
#     <a href="${item.ig_url}" ...
# ` : ''}

# Let's change the condition from `${item.ig_url ? \`` to `${(item.ig_url && item.ig_url !== '#' && item.ig_url.trim() !== '') ? \``
content = content.replace('${item.ig_url ? `\n                                    <a href="${item.ig_url}"', '${(item.ig_url && item.ig_url !== \'#\' && item.ig_url.trim() !== \'\') ? `\n                                    <a href="${item.ig_url}"')

# 2. Add Download button right after the Play button and before the Report button.
# Current:
#                                 ` : ''}
#                                 <button onclick="openReportModal('${item.id}')" class="w-7 h-7 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center justify-center transition tooltip shrink-0" title="Báo Cáo">📄</button>
# 
# We'll insert it right after the play button block ends.

play_block_end = r"` : ''}\s*<button onclick=\"openReportModal\('\${item\.id}'\)\""
download_button = r"""` : ''}
                                ${(item.media.video_url || item.media.download_url) ? `
                                    <button onclick="forceDownloadVideo('${item.media.download_url || item.media.video_url}', '${item.id}.mp4'); event.stopPropagation();" class="w-7 h-7 rounded-lg bg-emerald-500/15 hover:bg-emerald-500/25 text-emerald-400 border border-emerald-500/30 flex items-center justify-center transition tooltip shrink-0" title="Tải Về">⬇</button>
                                ` : ''}
                                <button onclick="openReportModal('${item.id}')\""""

content = re.sub(play_block_end, download_button, content)

# 3. Download function
# We need to add forceDownloadVideo function. I will replace downloadCurrentIdea logic and also add forceDownloadVideo.
download_func = """
        function forceDownloadVideo(url, filename) {
            showToast("Đang chuẩn bị tải về...", "⬇️");
            fetch(url)
                .then(response => {
                    if (!response.ok) throw new Error("Network response was not ok");
                    return response.blob();
                })
                .then(blob => {
                    const blobUrl = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.style.display = 'none';
                    a.href = blobUrl;
                    a.download = filename || 'video.mp4';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(blobUrl);
                    document.body.removeChild(a);
                    showToast("Tải về thành công!", "✅");
                })
                .catch(err => {
                    console.error("Lỗi tải video:", err);
                    window.open(url, '_blank');
                    showToast("Mở link do lỗi tải xuống.", "⚠️");
                });
        }

        function downloadCurrentIdea() {
            if (!appState.targetIdeaId) {
                showToast("Không tìm thấy dữ liệu ý tưởng!", "⚠️");
                return;
            }
            const idea = window.FEDU_IDEAS_DATABASE.ideas ? window.FEDU_IDEAS_DATABASE.ideas.find(i => i.id === appState.targetIdeaId) : window.FEDU_IDEAS_DATABASE.find(i => i.id === appState.targetIdeaId);
            if (!idea) return;
            let url = idea.media?.video_url || idea.media?.download_url || idea.video_url || idea.report_url || idea.thumbnail_url;
            if (!url) {
                showToast("Không có tài nguyên để tải về!", "⚠️");
                return;
            }
            forceDownloadVideo(url, idea.id + '.mp4');
        }
"""
# Replace the original downloadCurrentIdea with our new version
content = re.sub(r'function downloadCurrentIdea\(\) \{[\s\S]*?showToast\("Đang mở link tải về...", "⬇️"\);\n\s*\}', download_func, content)


# 4. "Video không ấn được: Kiểm tra logic render thẻ HTML, đảm bảo DOM không bị đè click."
# Let's fix the z-index issue on the video player in the modal if any, OR change the poster onclick to openVideoModal.
# Looking closely at the posters:
content = content.replace('onclick="openReportModal(\'${item.id}\')" title="Bấm để xem báo cáo">\n                                <img \n                                    src="${item.media.thumb_hook}"',
                          'onclick="openVideoModal(\'${item.id}\')" title="Bấm để xem video">\n                                <img \n                                    src="${item.media.thumb_hook}"')
content = content.replace('onclick="openReportModal(\'${item.id}\')" title="Bấm để xem báo cáo">\n                                <img \n                                    src="${item.media.thumb_key}"',
                          'onclick="openVideoModal(\'${item.id}\')" title="Bấm để xem video">\n                                <img \n                                    src="${item.media.thumb_key}"')


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Modifications done')
