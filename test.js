// SCRIPT BLOCK 0

function scrollCarousel(dir) {
    var stack = document.querySelector('.carousel-stack');
    if(stack) {
        var h = stack.clientHeight;
        stack.scrollBy({ top: dir * h, behavior: 'smooth' });
    }
}

// SCRIPT BLOCK 1

// Video source resolution - try multiple paths
const rawVideoSrc = 'https://media.fedu.vn/videos/carousel_slides/IG_%40Chibuzor_Ossai_DdRGI36Aj0X_Carousel_Analysis/slide_01.mp4';
let currentEndTime = null;

function getCandidateUrls(src) {
    if (!src) return [];
    if (src.startsWith('http://') || src.startsWith('https://')) return [src];
    let clean = src.replace(/^(\.\.\/|\.\/)*/g, '').replace(/^(videos\/|reports\/)/, '');
    return [
        'https://media.fedu.vn/videos/' + encodeURI(clean),
        '../videos/' + clean,
        './videos/' + clean,
        './' + clean
    ];
}

const candidateUrls = getCandidateUrls(rawVideoSrc);
let candidateIdx = 0;
const player = document.getElementById('mainPlayer');
window.isYtMuted = false;

function loadVideoCandidate() {
    if (!player || player.tagName === 'IFRAME' || candidateIdx >= candidateUrls.length) return;
    player.src = candidateUrls[candidateIdx];
    var link = document.getElementById('directVidLink');
    if (link) link.href = candidateUrls[candidateIdx];
    player.load();
}

if (player && player.tagName !== 'IFRAME') {
    player.onerror = function() {
        candidateIdx++;
        if (candidateIdx < candidateUrls.length) loadVideoCandidate();
    };
    loadVideoCandidate();
}

function playShot(startTime, endTime, label) {
    var stack = document.querySelector('.carousel-stack');
    if (stack) {
        var match = label ? label.match(/SHOT\s+(\d+)/i) : null;
        var slideIndex = 0;
        if (match) {
            slideIndex = parseInt(match[1]) - 1;
        } else if (startTime > 0) {
            slideIndex = Math.floor(startTime);
        }
        var target = stack.children[slideIndex];
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        var tag = document.getElementById('shotStatusTag');
        if (tag) tag.innerText = (label || ('Slide ' + (slideIndex+1))) + ' (Đang xem)';
        return;
    }
    if (!player) return;
    currentEndTime = (typeof endTime === 'number') ? endTime : null;
    var tag = document.getElementById('shotStatusTag');
    if (tag) {
        var endTxt = currentEndTime ? ' - ' + currentEndTime.toFixed(2) + 's' : '';
        tag.innerText = (label || 'Phân cảnh') + ': [' + startTime.toFixed(2) + 's' + endTxt + ']';
    }
    if (player.tagName === 'IFRAME') {
        player.contentWindow.postMessage(JSON.stringify({
            event: 'command',
            func: 'seekTo',
            args: [startTime, true]
        }), '*');
        player.contentWindow.postMessage(JSON.stringify({
            event: 'command',
            func: 'playVideo',
            args: []
        }), '*');
    } else {
        if(player) player.currentTime = startTime;
        var p = player.play();
            });
        }
    }
    document.querySelectorAll('.shot-card').forEach(function(c) { c.classList.remove('active-playing'); });
    var cards = document.querySelectorAll('.shot-card');
    for (var i = 0; i < cards.length; i++) {
        if (cards[i].innerText.indexOf(label) !== -1) {
            cards[i].classList.add('active-playing');
            break;
        }
    }
    if (window.innerWidth < 1024) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function setSpeed(speed, btn) {
    if (!player) return;
    if (player.tagName === 'IFRAME') {
        player.contentWindow.postMessage(JSON.stringify({
            event: 'command',
            func: 'setPlaybackRate',
            args: [speed]
        }), '*');
    } else {
        player.playbackRate = speed;
    }
    document.querySelectorAll('.speed-row .ctrl-btn').forEach(function(b) { b.classList.remove('active'); });
    if (btn) btn.classList.add('active');
}

function stepFrame(frames) {
    if (!player) return;
    if (player.tagName !== 'IFRAME') {
        player.pause();
        player.currentTime += (frames * (1/30));
    }
}

function toggleMute(btn) {
    if (!player) return;
    if (player.tagName === 'IFRAME') {
        window.isYtMuted = !window.isYtMuted;
        player.contentWindow.postMessage(JSON.stringify({
            event: 'command',
            func: window.isYtMuted ? 'mute' : 'unMute',
            args: []
        }), '*');
        if (btn) btn.innerText = window.isYtMuted ? 'Tắt tiếng' : 'Âm thanh';
    } else {
        player.muted = !player.muted;
        if (btn) btn.innerText = player.muted ? 'Tắt tiếng' : 'Âm thanh';
    }
}

function togglePlayerFullscreen() {
    var v = document.getElementById('mainPlayer');
    if (!v) return;
    if (!document.fullscreenElement && !document.webkitFullscreenElement) {
        if (v.requestFullscreen) v.requestFullscreen().catch(function(){});
        else if (v.webkitRequestFullscreen) v.webkitRequestFullscreen();
        else if (v.webkitEnterFullscreen) v.webkitEnterFullscreen();
    } else {
        if (document.exitFullscreen) document.exitFullscreen().catch(function(){});
        else if (document.webkitExitFullscreen) document.webkitExitFullscreen();
    }
}

document.addEventListener('keydown', function(e) {
    if ((e.key === 'f' || e.key === 'F') && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
        togglePlayerFullscreen();
    }
    if (e.key === 'Escape') {
        closeLightbox();
        toggleDrawer(false);
    }
    if (e.key === ' ' && document.activeElement.tagName !== 'INPUT') {
        e.preventDefault();
        if (player) player.paused ? player.play() : player.pause();
    }
});

function switchView(view) {
    var sb = document.getElementById('storyboardView');
    var grid = document.getElementById('gridView');
    var tabD = document.getElementById('tabDetailBtn');
    var tabG = document.getElementById('tabGridBtn');
    if (view === 'grid') {
        sb.style.display = 'none';
        grid.style.display = 'grid';
        tabD.classList.remove('active');
        tabG.classList.add('active');
    } else {
        sb.style.display = 'flex';
        grid.style.display = 'none';
        tabD.classList.add('active');
        tabG.classList.remove('active');
    }
}

function toggleDrawer(open) {
    var d = document.getElementById('drawerBackdrop');
    if (open) d.classList.add('open');
    else d.classList.remove('open');
}

function jumpToShot(shotNum, st, et, label) {
    toggleDrawer(false);
    switchView('detail');
    playShot(st, et, label);
    var card = document.getElementById('shot-card-' + shotNum);
    if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function openLightbox(src, caption) {
    var modal = document.getElementById('lightboxModal');
    document.getElementById('lightboxImg').src = src;
    document.getElementById('lightboxCaption').innerText = caption || '';
    modal.style.display = 'flex';
}

function closeLightbox() {
    document.getElementById('lightboxModal').style.display = 'none';
}

function togglePromptAccordion(headerEl) {
    var card = headerEl.closest('.remake-prompt-card');
    if (!card) return;
    var body = card.querySelector('.prompt-accordion-body');
    var icon = card.querySelector('.toggle-icon');
    var label = card.querySelector('.toggle-label');
    if (!body) return;
    var collapsed = (body.style.display === 'none' || getComputedStyle(body).display === 'none');
    if (collapsed) {
        body.style.display = 'block';
        if (icon) icon.textContent = '▲';
        if (label) label.textContent = 'Thu gọn';
    } else {
        body.style.display = 'none';
        if (icon) icon.textContent = '▼';
        if (label) label.textContent = 'Mở xem';
    }
}

function copyMegaPrompt(e, btn) {
    if (e && e.stopPropagation) e.stopPropagation();
    var card = btn.closest('.remake-prompt-card');
    var codeEl = card ? card.querySelector('.prompt-code-content') : document.getElementById('megaPromptText');
    if (!codeEl) return;
    var text = codeEl.innerText || codeEl.textContent;
    navigator.clipboard.writeText(text).then(function() {
        var orig = btn.innerHTML;
        btn.innerHTML = '✅ Đã chép!';
        btn.style.background = '#16a34a';
        btn.style.color = '#fff';
        setTimeout(function() {
            btn.innerHTML = orig;
            btn.style.background = '';
            btn.style.color = '';
        }, 2000);
    }).catch(function() {
        alert('Lỗi sao chép, bạn bôi đen văn bản để copy nhé!');
    });
}

