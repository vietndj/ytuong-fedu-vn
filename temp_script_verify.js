

const masterVideoUrl = "https://ytuong.fedu.vn/api/video?id=1aYhfPfGH0GvyuDSJOeZ0k8i0CbOMdwSF";
let currentMode = "master";
let currentEndTime = null;
const player = document.getElementById("mainPlayer");

function setPlayMode(mode) {
    currentMode = mode;
    document.getElementById("btnMasterMode").classList.toggle("active", mode === "master");
    document.getElementById("btnSlideMode").classList.toggle("active", mode === "slide");
    if (mode === "master") {
        loadVideoUrl(masterVideoUrl, "🎬 Phân cảnh: Toàn bộ Master Timeline");
    }
}

function loadVideoUrl(url, statusText) {
    if (player.src !== url) {
        player.src = url;
        player.load();
    }
    const directLink = document.getElementById("directVidLink");
    if (directLink) directLink.href = url;
    if (statusText) {
        document.getElementById("shotStatusTag").innerText = statusText;
    }
}

loadVideoUrl(masterVideoUrl, "🎬 Phân cảnh: Toàn bộ Master Timeline");

function playShot(startTime, endTime, label, slideVidUrl) {
    currentEndTime = (typeof endTime === "number") ? endTime : null;
    const tag = document.getElementById("shotStatusTag");
    if (currentMode === "master") {
        if (player.src !== masterVideoUrl) {
            loadVideoUrl(masterVideoUrl);
        }
        if (tag) {
            const endTxt = currentEndTime ? " - " + currentEndTime.toFixed(2) + "s" : "";
            tag.innerText = "🎬 " + (label || "Phân cảnh") + ": [" + startTime.toFixed(2) + "s" + endTxt + "]";
        }
        if(player) player.currentTime = startTime;
        player.play().catch(e => {
            player.muted = true;
            player.play();
        });
    } else {
        playSlideSingle(slideVidUrl, label, (endTime - startTime));
    }

    document.querySelectorAll(".sc").forEach(c => c.classList.remove("active-playing"));
    const matchCard = Array.from(document.querySelectorAll(".sc")).find(c => c.innerText.includes(label));
    if (matchCard) matchCard.classList.add("active-playing");

    if (window.innerWidth < 1024) {
        window.scrollTo({ top: 0, behavior: "smooth" });
    }
}

function playSlideSingle(slideVidUrl, label, duration) {
    currentEndTime = duration;
    loadVideoUrl(slideVidUrl, "🎬 Slide độc lập: " + label + " [0.00s - " + duration.toFixed(2) + "s]");
    player.currentTime = 0;
    player.play().catch(e => {
        player.muted = true;
        player.play();
    });
    document.getElementById("btnSlideMode").classList.add("active");
    document.getElementById("btnMasterMode").classList.remove("active");
    currentMode = "slide";

    document.querySelectorAll(".sc").forEach(c => c.classList.remove("active-playing"));
    const matchCard = Array.from(document.querySelectorAll(".sc")).find(c => c.innerText.includes(label));
    if (matchCard) matchCard.classList.add("active-playing");

    if (window.innerWidth < 1024) {
        window.scrollTo({ top: 0, behavior: "smooth" });
    }
}

player.addEventListener("timeupdate", () => {
    if (currentMode === "master" && currentEndTime !== null) {
        if (player.currentTime >= currentEndTime) {
            player.pause();
            currentEndTime = null;
        }
    }
});

function setSpeed(speed, btn) {
    player.playbackRate = speed;
    document.querySelectorAll(".speed-buttons-row .ctrl-btn").forEach(b => b.classList.remove("active"));
    if (btn) btn.classList.add("active");
}

function stepFrame(frames) {
    player.pause();
    player.currentTime += (frames * (1/30));
}

function toggleMute(btn) {
    player.muted = !player.muted;
    if (btn) btn.innerText = player.muted ? "🔇 Tắt Tiếng" : "🔊 Tiếng";
}

function switchView(view) {
    const sb = document.getElementById("storyboardView");
    const grid = document.getElementById("gridView");
    const tabDetail = document.getElementById("tabDetailBtn");
    const tabGrid = document.getElementById("tabGridBtn");
    if (view === "grid") {
        sb.style.display = "none";
        grid.style.display = "grid";
        tabDetail.classList.remove("active");
        tabGrid.classList.add("active");
    } else {
        sb.style.display = "flex";
        grid.style.display = "none";
        tabDetail.classList.add("active");
        tabGrid.classList.remove("active");
    }
}

function toggleDrawer(open) {
    const drawer = document.getElementById("drawerBackdrop");
    if (open) drawer.classList.add("open");
    else drawer.classList.remove("open");
}

function jumpToShot(shotNum, st, et, label, slideVidUrl) {
    toggleDrawer(false);
    switchView("detail");
    playShot(st, et, label, slideVidUrl);
    const targetCard = document.getElementById("shot-card-" + shotNum);
    if (targetCard) {
        targetCard.scrollIntoView({ behavior: "smooth", block: "center" });
    }
}

function openLightbox(src, caption) {
    const modal = document.getElementById("lightboxModal");
    const img = document.getElementById("lightboxImg");
    const cap = document.getElementById("lightboxCaption");
    img.src = src;
    cap.innerText = caption || "";
    modal.style.display = "flex";
}

function closeLightbox() {
    document.getElementById("lightboxModal").style.display = "none";
}

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        closeLightbox();
        toggleDrawer(false);
    } else if (e.key === " ") {
        if (document.activeElement.tagName !== "INPUT") {
            e.preventDefault();
            player.paused ? player.play() : player.pause();
        }
    }
});


function handleCreatorClick(e, handle, name) {
    if (e) e.preventDefault();
    try {
        if (window.parent && window.parent !== window) {
            window.parent.postMessage({ type: 'FILTER_CREATOR', handle: handle, name: name }, '*');
            if (typeof window.parent.filterByCreator === 'function') {
                window.parent.closeModal('reportEmbedModal');
                window.parent.filterByCreator(handle, name);
                return;
            }
        }
    } catch (err) {}
    window.location.href = '../index.html?creator=' + encodeURIComponent(handle);
}


function togglePlayerFullscreen() {
    const v = document.getElementById('mainPlayer');
    if (!v) return;
    if (!document.fullscreenElement && !document.webkitFullscreenElement) {
        if (v.requestFullscreen) {
            v.requestFullscreen().catch(() => {});
        } else if (v.webkitRequestFullscreen) {
            v.webkitRequestFullscreen();
        } else if (v.webkitEnterFullscreen) {
            v.webkitEnterFullscreen();
        }
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen().catch(() => {});
        } else if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
        }
    }
}

document.addEventListener('keydown', (e) => {
    if ((e.key === 'f' || e.key === 'F') && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
        e.preventDefault();
        togglePlayerFullscreen();
    }
});


