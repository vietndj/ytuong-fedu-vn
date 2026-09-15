#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator for clean, optimized report:
IG_@Victoria_Morse_DbESOapo-p3_Video_by_victoriamorse.html
Following user request:
"Sửa lại không để nhiều ảnh giống nhau chỉ đếm cảnh + kịch bản nói + megaprompt làm lại kịch bản thôi"
"""

import json
import os

JSON_PATH = "/Users/vietmac/Documents/CODE/Video phan tich/output_packages/IG_@Victoria_Morse_DbESOapo-p3_Video_by_victoriamorse/shot_info.json"

with open(JSON_PATH, "r", encoding="utf-8") as f:
    shots = json.load(f)

# Build JavaScript SHOTS array: [id, start, end, dur, img, headline, action, vo_vi, vo_en, phase]
# Phase: 1 for Hook (0-7.8s, shots 1-10), 2 for Story (7.8-41.8s, shots 11-41), 3 for Takeaway (41.8-61.5s, shots 42-69)
shots_js_data = []
for s in shots:
    sid = s["shot_id"]
    st = round(float(s["start_time"]), 2)
    et = round(float(s["end_time"]), 2)
    dur = round(float(s["duration"]), 2)
    img = s["img_url"]
    hl = s["headline"]
    act = s["subject_action"]
    vo_vi = s.get("dialogue_vi", "")
    vo_en = s.get("dialogue_en", "")
    
    if et <= 7.85:
        phase = "hook"
    elif et <= 41.85:
        phase = "story"
    else:
        phase = "takeaway"
        
    shots_js_data.append([sid, st, et, dur, img, hl, act, vo_vi, vo_en, phase])

shots_json_str = json.dumps(shots_js_data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>The Art of Authentic Voiceover Storytelling — @victoriamorse</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root {{
  --bg-main: #ffffff;
  --bg-sub: #f8fafc;
  --bg-card: #ffffff;
  --border: #e2e8f0;
  --border-active: #2563eb;
  --text-title: #0f172a;
  --text-body: #334155;
  --text-muted: #64748b;
  --accent: #2563eb;
  --accent-light: #eff6ff;
  --accent-tint: rgba(37, 99, 235, 0.08);
  --emerald: #059669;
  --emerald-bg: #f0fdf4;
  --amber: #d97706;
  --amber-bg: #fffbeb;
  --font-h: 'Plus Jakarta Sans', -apple-system, sans-serif;
  --font-b: 'Be Vietnam Pro', -apple-system, sans-serif;
  --font-m: 'JetBrains Mono', monospace;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
body {{
  background: var(--bg-sub);
  color: var(--text-body);
  font-family: var(--font-b);
  font-size: 14px;
  line-height: 1.55;
}}
.layout {{
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}}
@media (min-width: 1024px) {{
  .layout {{
    display: grid;
    grid-template-columns: 430px 1fr;
    height: 100vh;
    overflow: hidden;
  }}
}}

/* LEFT COLUMN: STICKY PLAYER */
.player-col {{
  background: #000;
  border-right: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  flex-direction: column;
}}
@media (min-width: 1024px) {{
  .player-col {{
    height: 100vh;
    overflow-y: auto;
  }}
}}
.video-box {{
  position: relative;
  width: 100%;
  aspect-ratio: 9/16;
  max-height: 46vh;
  background: #000;
  display: flex;
  align-items: center;
  justify-content: center;
}}
@media (min-width: 1024px) {{
  .video-box {{
    max-height: none;
    width: 100%;
    flex: 1;
  }}
}}
video#mainVid {{
  width: 100%;
  height: 100%;
  object-fit: contain;
}}
.director-bar {{
  background: #0f172a;
  color: #fff;
  padding: 10px 14px;
  display: flex;
  flex-direction: column;
  gap: 7px;
  font-family: var(--font-m);
  font-size: 11px;
}}
.dir-row {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}}
.btn-c {{
  background: #1e293b;
  border: 1px solid #334155;
  color: #cbd5e1;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.15s;
}}
.btn-c:hover {{ background: #334155; color: #fff; }}
.btn-c.active {{
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
  font-weight: 700;
}}
.time-pill {{
  background: #1e293b;
  padding: 3px 8px;
  border-radius: 4px;
  color: #38bdf8;
  font-weight: 600;
  font-size: 11.5px;
}}

/* RIGHT COLUMN: CONTENT */
.content-col {{
  background: var(--bg-sub);
  padding: 14px;
  overflow-y: auto;
}}
@media (min-width: 768px) {{
  .content-col {{
    padding: 22px 28px;
  }}
}}

/* HERO CARD */
.hero-card {{
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 18px 20px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}}
.hero-badge {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: var(--accent-light);
  color: var(--accent);
  font-size: 11px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 99px;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}}
.hero-title {{
  font-family: var(--font-h);
  font-size: 21px;
  font-weight: 800;
  color: var(--text-title);
  line-height: 1.3;
  margin-bottom: 5px;
}}
.hero-creator {{
  font-size: 13.5px;
  color: var(--text-muted);
  margin-bottom: 14px;
}}
.hero-stats {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
  gap: 8px;
  margin-bottom: 14px;
}}
.stat-box {{
  background: var(--bg-sub);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 10px;
  text-align: center;
}}
.stat-val {{
  font-family: var(--font-h);
  font-size: 17px;
  font-weight: 800;
  color: var(--accent);
}}
.stat-lbl {{
  font-size: 10px;
  color: var(--text-muted);
  font-weight: 600;
  text-transform: uppercase;
  margin-top: 2px;
}}
.director-rules {{
  background: #fffbeb;
  border-left: 3px solid #f59e0b;
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 12.5px;
  color: #92400e;
  line-height: 1.5;
}}

/* SECTION TABS NAV */
.nav-tabs {{
  display: flex;
  gap: 4px;
  background: #e2e8f0;
  padding: 4px;
  border-radius: 9px;
  margin-bottom: 16px;
  position: sticky;
  top: 0;
  z-index: 50;
}}
.nav-tab-btn {{
  flex: 1;
  background: transparent;
  border: none;
  padding: 8px 12px;
  font-size: 12.5px;
  font-weight: 700;
  font-family: var(--font-h);
  color: var(--text-muted);
  border-radius: 7px;
  cursor: pointer;
  transition: all 0.15s;
  text-align: center;
  white-space: nowrap;
}}
.nav-tab-btn.active {{
  background: #fff;
  color: var(--text-title);
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}}

/* SECTION COMMON */
.sec-card {{
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px 20px;
  margin-bottom: 18px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}}
.sec-header {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
  flex-wrap: wrap;
  gap: 8px;
}}
.sec-title {{
  font-family: var(--font-h);
  font-size: 17px;
  font-weight: 800;
  color: var(--text-title);
  display: flex;
  align-items: center;
  gap: 8px;
}}

/* ═══ 1. BẢNG ĐẾM CẢNH (SCENE COUNTER TABLE) ═══ */
.filter-pills {{
  display: flex;
  gap: 6px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}}
.filter-btn {{
  background: var(--bg-sub);
  border: 1px solid var(--border);
  color: var(--text-muted);
  font-size: 11.5px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 99px;
  cursor: pointer;
  transition: all 0.15s;
}}
.filter-btn:hover {{
  background: #e2e8f0;
  color: var(--text-title);
}}
.filter-btn.active {{
  background: var(--accent);
  color: #fff;
  border-color: var(--accent);
}}
.scene-list {{
  display: flex;
  flex-direction: column;
  gap: 8px;
}}
.scene-row {{
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 10px 12px;
  display: grid;
  grid-template-columns: 46px 64px 54px 1fr;
  gap: 12px;
  align-items: center;
  transition: all 0.15s;
  cursor: pointer;
}}
@media (max-width: 640px) {{
  .scene-row {{
    grid-template-columns: 42px 50px 1fr;
    gap: 8px;
  }}
  .scene-dur-col {{
    display: none;
  }}
}}
.scene-row:hover {{
  border-color: #93c5fd;
  background: #fafcff;
}}
.scene-row.active-scene {{
  border-color: var(--accent);
  background: var(--accent-light);
  box-shadow: 0 0 0 2px rgba(37,99,235,0.25);
}}
.scene-num-badge {{
  background: var(--text-title);
  color: #fff;
  font-family: var(--font-m);
  font-size: 11px;
  font-weight: 700;
  padding: 4px 6px;
  border-radius: 6px;
  text-align: center;
}}
.scene-dur-col {{
  font-family: var(--font-m);
  font-size: 10.5px;
  color: var(--accent);
  font-weight: 600;
  text-align: center;
  white-space: nowrap;
}}
.scene-thumb-wrap {{
  position: relative;
  width: 52px;
  aspect-ratio: 9/16;
  border-radius: 6px;
  overflow: hidden;
  background: #000;
  border: 1px solid var(--border);
  flex-shrink: 0;
}}
.scene-thumb-wrap img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}}
.scene-desc-col {{
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}}
.scene-headline {{
  font-family: var(--font-h);
  font-size: 13px;
  font-weight: 700;
  color: var(--text-title);
  line-height: 1.35;
}}
.scene-action {{
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.4;
}}
.scene-vo-line {{
  font-size: 11.5px;
  color: var(--accent);
  font-style: italic;
  margin-top: 2px;
}}

/* ═══ 2. KỊCH BẢN NÓI (VOICE-OVER SCRIPT) ═══ */
.vo-phase-box {{
  margin-bottom: 20px;
}}
.phase-kicker {{
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--font-h);
  font-size: 12px;
  font-weight: 800;
  padding: 3px 10px;
  border-radius: 6px;
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}}
.phase-kicker.hook {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}
.phase-kicker.story {{ background: #fefce8; color: #854d0e; border: 1px solid #fef08a; }}
.phase-kicker.takeaway {{ background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }}

.vo-table {{
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
  margin-bottom: 8px;
}}
.vo-table th {{
  background: var(--bg-sub);
  padding: 7px 10px;
  text-align: left;
  font-family: var(--font-h);
  font-weight: 700;
  border-bottom: 1px solid var(--border);
  color: var(--text-title);
  font-size: 11.5px;
}}
.vo-table td {{
  padding: 8px 10px;
  border-bottom: 1px solid var(--border);
  vertical-align: top;
}}
.vo-table tr:hover {{
  background: var(--accent-light);
}}
.vo-time-btn {{
  background: #fff;
  border: 1px solid var(--border);
  font-family: var(--font-m);
  font-size: 10px;
  color: var(--accent);
  font-weight: 700;
  padding: 3px 6px;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
}}
.vo-time-btn:hover {{
  background: var(--accent);
  color: #fff;
}}
.vo-vi-text {{
  font-weight: 600;
  color: var(--text-title);
  line-height: 1.5;
}}
.vo-en-text {{
  color: var(--text-muted);
  font-size: 11px;
  font-style: italic;
  margin-top: 3px;
}}

/* ═══ 3. MEGAPROMPT LÀM LẠI KỊCH BẢN ═══ */
.prompt-container {{
  background: #0f172a;
  color: #f8fafc;
  border-radius: 10px;
  padding: 16px;
  position: relative;
  font-family: var(--font-m);
  font-size: 11.5px;
  line-height: 1.6;
  overflow-x: auto;
  margin-bottom: 16px;
}}
.copy-btn {{
  position: absolute;
  top: 10px;
  right: 10px;
  background: #2563eb;
  color: #fff;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  font-family: var(--font-h);
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all 0.15s;
}}
.copy-btn:hover {{ background: #1d4ed8; }}
.copy-toast {{
  display: none;
  position: fixed;
  bottom: 24px;
  right: 24px;
  background: #059669;
  color: #fff;
  padding: 10px 18px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 13px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 9999;
}}

.example-card {{
  background: var(--bg-sub);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 14px;
  margin-bottom: 10px;
}}
.example-head {{
  font-family: var(--font-h);
  font-weight: 700;
  font-size: 13px;
  color: var(--text-title);
  margin-bottom: 4px;
}}
.example-body {{
  font-size: 12px;
  color: var(--text-body);
  line-height: 1.5;
}}

/* LIGHTBOX */
.lightbox {{
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.92);
  z-index: 2000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 14px;
  flex-direction: column;
}}
.lightbox.open {{ display: flex; }}
.lightbox-img {{
  max-width: 90vw;
  max-height: 80vh;
  object-fit: contain;
  border-radius: 6px;
}}
.lightbox-cap {{
  color: #fff;
  margin-top: 8px;
  font-size: 12px;
  text-align: center;
  max-width: 500px;
}}
.lightbox-close {{
  position: absolute;
  top: 14px;
  right: 18px;
  color: #fff;
  font-size: 26px;
  background: none;
  border: none;
  cursor: pointer;
}}
</style>
</head>
<body>
<div class="layout">
  <!-- LEFT: STICKY DIRECTOR PLAYER -->
  <aside class="player-col">
    <div class="video-box">
      <video id="mainVid" src="https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/videos/DbESOapo-p3.mp4" playsinline preload="metadata"></video>
    </div>
    <div class="director-bar">
      <div class="dir-row">
        <button class="btn-c" onclick="togglePlay()" id="playBtn">▶ Phát</button>
        <span class="time-pill" id="curTime">00:00.00 / 61.53s</span>
        <button class="btn-c" onclick="toggleLoop()" id="loopBtn">🔁 Lặp: Tắt</button>
      </div>
      <div class="dir-row">
        <span>Tốc độ:</span>
        <div style="display:flex; gap:3px;">
          <button class="btn-c" onclick="setSpeed(0.25)">0.25x</button>
          <button class="btn-c" onclick="setSpeed(0.5)">0.5x</button>
          <button class="btn-c active" onclick="setSpeed(1.0)">1x</button>
          <button class="btn-c" onclick="setSpeed(1.25)">1.25x</button>
        </div>
        <div style="display:flex; gap:3px;">
          <button class="btn-c" onclick="stepFrame(-1)">◀ Frame</button>
          <button class="btn-c" onclick="stepFrame(1)">Frame ▶</button>
        </div>
      </div>
    </div>
  </aside>

  <!-- RIGHT: MAIN CONTENT -->
  <main class="content-col">
    <!-- HERO SUMMARY -->
    <header class="hero-card">
      <span class="hero-badge">🎬 Báo Cáo Phân Tích Kịch Bản &amp; Đếm Cảnh</span>
      <h1 class="hero-title">The Art of Authentic Voiceover Storytelling</h1>
      <p class="hero-creator">Đạo diễn: <strong>Victoria Morse (@victoriamorse)</strong> • Cựu Đạo Diễn Phim Quảng Cáo Thương Mại</p>
      <div class="hero-stats">
        <div class="stat-box"><div class="stat-val">69</div><div class="stat-lbl">Phân Cảnh</div></div>
        <div class="stat-box"><div class="stat-val">61.53s</div><div class="stat-lbl">Thời Lượng</div></div>
        <div class="stat-box"><div class="stat-val">0.89s</div><div class="stat-lbl">Nhịp Cắt TB</div></div>
        <div class="stat-box"><div class="stat-val">Voice-Over</div><div class="stat-lbl">Chiến Lược</div></div>
      </div>
      <div class="director-rules">
        <strong>💡 Triết lý kể chuyện Voice-Over từ Victoria Morse:</strong><br>
        1. <strong>Voice-Over First:</strong> Thu âm giọng dẫn trước khi bấm nhát cắt dựng đầu tiên để định hình nhịp thở.<br>
        2. <strong>Kịch bản là Nhật Ký:</strong> Viết tự nhiên như một mẩu voice note gửi bạn thân, không gò ép văn mẫu quảng cáo.<br>
        3. <strong>Bản sắc con người:</strong> AI có thể tóm tắt lịch trình, nhưng không thể cảm nhận vì sao buổi sáng đó lại có ý nghĩa với bạn.<br>
        4. <strong>Công thức 3 phần:</strong> Cú móc (Hook: 0-8s) ➔ Thân bài (Story: 9-41s) ➔ Đọng lại (Takeaway: 42-61s).
      </div>
    </header>

    <!-- NAVIGATION TABS -->
    <nav class="nav-tabs">
      <button class="nav-tab-btn active" onclick="switchSection('scene-section')" id="tabBtnScene">🎬 1. Đếm Cảnh (69 Cảnh)</button>
      <button class="nav-tab-btn" onclick="switchSection('vo-section')" id="tabBtnVo">🎙️ 2. Kịch Bản Nói</button>
      <button class="nav-tab-btn" onclick="switchSection('prompt-section')" id="tabBtnPrompt">🪄 3. Megaprompt Làm Lại</button>
    </nav>

    <!-- ═══ PHẦN 1: BẢNG ĐẾM CẢNH (SCENE COUNTER) ═══ -->
    <section id="scene-section" class="sec-card">
      <div class="sec-header">
        <h2 class="sec-title">🎬 Bảng Đếm Cảnh &amp; Nhịp Dựng B-Roll</h2>
        <div class="filter-pills">
          <button class="filter-btn active" onclick="filterShots('all')">Tất cả (69)</button>
          <button class="filter-btn" onclick="filterShots('hook')">Hook (Cảnh 1-10)</button>
          <button class="filter-btn" onclick="filterShots('story')">Story (Cảnh 11-41)</button>
          <button class="filter-btn" onclick="filterShots('takeaway')">Takeaway (Cảnh 42-69)</button>
        </div>
      </div>
      <p style="font-size:12.5px;color:var(--text-muted);margin-bottom:12px;">
        💡 <em>Mỗi cảnh chỉ giữ 1 thumbnail đại diện duy nhất (chống trùng lặp ảnh). Nhấn vào bất kỳ cảnh nào để video tự động nhảy đến đúng thời điểm đó.</em>
      </p>
      <div class="scene-list" id="sceneList">
        <!-- Rendered by JavaScript -->
      </div>
    </section>

    <!-- ═══ PHẦN 2: KỊCH BẢN NÓI (VOICE-OVER MASTER SCRIPT) ═══ -->
    <section id="vo-section" class="sec-card" style="display:none;">
      <div class="sec-header">
        <h2 class="sec-title">🎙️ Kịch Bản Lời Thoại Song Ngữ Chuẩn 3 Phần</h2>
        <span style="font-size:12px;color:var(--text-muted);font-weight:600;">12 Khối Thoại • 61.53 Giây</span>
      </div>

      <!-- HOOK -->
      <div class="vo-phase-box">
        <span class="phase-kicker hook">PHẦN 1: THE HOOK (0.0s – 7.8s) — Mở màn bằng bài học xương máu</span>
        <table class="vo-table">
          <thead><tr><th style="width:75px;">Thời gian</th><th>Kịch bản nói (Bản dịch Tiếng Việt mộc mạc)</th><th style="width:38%;">Nguyên văn Tiếng Anh</th></tr></thead>
          <tbody>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(0.0, 3.4)">▶ 0.0-3.4s</button></td>
              <td><div class="vo-vi-text">Tôi kể chuyện hay hơn hẳn sau những năm tháng làm đạo diễn quảng cáo chuyên nghiệp.</div></td>
              <td><div class="vo-en-text">I became a better storyteller after directing commercials for a living.</div></td>
            </tr>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(3.4, 7.8)">▶ 3.4-7.8s</button></td>
              <td><div class="vo-vi-text">Kể chuyện không phải là cố viết cho thật bóng bẩy, mà là làm sao để chạm được vào cảm xúc người nghe.</div></td>
              <td><div class="vo-en-text">Storytelling isn't about being the best writer, it's about making people feel something.</div></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- STORY -->
      <div class="vo-phase-box">
        <span class="phase-kicker story">PHẦN 2: THE STORY (7.8s – 41.8s) — Tự sự nhật ký &amp; Bản sắc độc bản AI không sao chép được</span>
        <table class="vo-table">
          <thead><tr><th style="width:75px;">Thời gian</th><th>Kịch bản nói (Bản dịch Tiếng Việt mộc mạc)</th><th style="width:38%;">Nguyên văn Tiếng Anh</th></tr></thead>
          <tbody>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(7.8, 13.1)">▶ 7.8-13.1s</button></td>
              <td><div class="vo-vi-text">Tôi luôn khuyên bạn hãy phát triển câu chuyện thật kỹ trước khi mở phần mềm lên bấm nhát cắt đầu tiên.</div></td>
              <td><div class="vo-en-text">I recommend developing your story before you even start editing.</div></td>
            </tr>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(13.1, 16.6)">▶ 13.1-16.6s</button></td>
              <td><div class="vo-vi-text">Tôi luôn thu âm Voice-Over trước tiên, vì nó chính là chiếc móng vững chắc cho mọi thứ còn lại.</div></td>
              <td><div class="vo-en-text">I always record my voice-overs first because it sets the foundation for everything else.</div></td>
            </tr>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(16.6, 19.7)">▶ 16.6-19.7s</button></td>
              <td><div class="vo-vi-text">Mọi bộ phim vĩ đại, chương trình truyền hình hay thước phim quảng cáo đều luôn bắt đầu từ một kịch bản chỉn chu.</div></td>
              <td><div class="vo-en-text">Every great movie, TV show, or commercial starts with a script.</div></td>
            </tr>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(19.7, 23.0)">▶ 19.7-23.0s</button></td>
              <td><div class="vo-vi-text">Nhưng thay vì xem nó như một kịch bản gò bó, hãy nghĩ về nó như một trang nhật ký đời thường.</div></td>
              <td><div class="vo-en-text">But instead of thinking of it as a script, think of it as a diary entry.</div></td>
            </tr>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(23.0, 26.7)">▶ 23.0-26.7s</button></td>
              <td><div class="vo-vi-text">Đúng là AI giúp bạn sắp xếp ý tứ rất nhanh, nhưng nó không bao giờ có thể kể được câu chuyện của chính bạn.</div></td>
              <td><div class="vo-en-text">Yes, AI can help you organize your thoughts, but it can't tell your story.</div></td>
            </tr>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(26.7, 34.6)">▶ 26.7-34.6s</button></td>
              <td><div class="vo-vi-text">Claude hay ChatGPT có thể mô tả vanh vách lịch trình buổi sáng của tôi, nhưng nó không bao giờ hiểu được vì sao buổi sáng hôm đó lại có ý nghĩa với tôi, trong đầu tôi trăn trở điều gì, hay cảm xúc bên trong tôi xáo trộn ra sao.</div></td>
              <td><div class="vo-en-text">Claude can tell my routine, but not why that morning mattered, what was on my mind, or how I was feeling.</div></td>
            </tr>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(34.6, 41.8)">▶ 34.6-41.8s</button></td>
              <td><div class="vo-vi-text">Bản chất mạng xã hội sinh ra là để con người kết nối với nhau. Và sự chân thật độc bản của bạn chính là thứ duy nhất không một ai, không một thuật toán nào có thể sao chép được.</div></td>
              <td><div class="vo-en-text">Social media is for connection and authenticity is the one thing no one can copy.</div></td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- TAKEAWAY -->
      <div class="vo-phase-box">
        <span class="phase-kicker takeaway">PHẦN 3: THE TAKEAWAY (41.8s – 61.5s) — Công thức 3 câu hỏi &amp; Dư vị cảm xúc</span>
        <table class="vo-table">
          <thead><tr><th style="width:75px;">Thời gian</th><th>Kịch bản nói (Bản dịch Tiếng Việt mộc mạc)</th><th style="width:38%;">Nguyên văn Tiếng Anh</th></tr></thead>
          <tbody>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(41.8, 54.1)">▶ 41.8-54.1s</button></td>
              <td><div class="vo-vi-text">Nên lần tới khi ngồi vào bàn sáng tạo nội dung, hãy bắt đầu với 3 phần rõ ràng: 1. Cú móc (The Hook): Câu chuyện này nói về cái gì? 2. Thân bài (The Story): Hiện tại tôi đang học được bài học gì hay đang gặp thử thách nào? 3. Đọng lại (The Takeaway): Tôi thực sự am hiểu chuyên môn gì và người xem có thể soi chiếu lại bản thân thế nào?</div></td>
              <td><div class="vo-en-text">Start with three parts: What is my story about (hook)? What am I learning or what is challenging me (story)? What am I an expert in or how can someone reflect on this (takeaway)?</div></td>
            </tr>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(54.1, 57.0)">▶ 54.1-57.0s</button></td>
              <td><div class="vo-vi-text">Hãy viết kịch bản như thể bạn đang gõ tin nhắn cho một người bạn thân hay gửi một mẩu voice note ngắn ngủi.</div></td>
              <td><div class="vo-en-text">Write it like you're texting a friend or leaving a voice note.</div></td>
            </tr>
            <tr>
              <td><button class="vo-time-btn" onclick="jumpToTime(57.0, 61.5)">▶ 57.0-61.5s</button></td>
              <td><div class="vo-vi-text">Người ta có thể quên những việc bạn làm trong ngày, nhưng họ sẽ nhớ mãi cảm xúc mà câu chuyện của bạn mang lại.</div></td>
              <td><div class="vo-en-text">We won't remember what you did, but we'll remember how a story made us feel.</div></td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- ═══ PHẦN 3: MEGAPROMPT LÀM LẠI KỊCH BẢN ═══ -->
    <section id="prompt-section" class="sec-card" style="display:none;">
      <div class="sec-header">
        <h2 class="sec-title">🪄 Megaprompt Làm Lại Kịch Bản Thực Chiến (STU Remake)</h2>
        <button class="copy-btn" onclick="copyMegaprompt()">📋 Sao chép Megaprompt</button>
      </div>
      <p style="font-size:12.5px;color:var(--text-muted);margin-bottom:12px;">
        💡 <em>Sao chép toàn bộ Prompt dưới đây, dán vào Gemini / Claude / ChatGPT, điền thông tin ngành nghề của bạn để tạo kịch bản Voice-Over chuẩn phong cách Victoria Morse.</em>
      </p>

      <div class="prompt-container">
        <pre id="promptCode" style="white-space:pre-wrap; font-family:var(--font-m);">
[VAI TRÒ]:
Bạn là Đạo diễn Biên kịch Video ngắn chuyên nghiệp theo phong cách "Authentic Voiceover & Visual Diary" của Victoria Morse. Bạn chuyên giúp các chuyên gia, chủ tiệm và người kinh doanh thực chiến chuyển thể trải nghiệm làm nghề thành kịch bản video 60 giây chạm cảm xúc, giữ chân người xem cao, không dùng từ ngữ sáo rỗng.

[THÔNG TIN ĐẦU VÀO CỦA TÔI]:
- Ngành nghề / Lĩnh vực: [ĐIỀN NGÀNH NGHỀ CỦA BẠN: Spa/Nội thất/Cafe/Thời trang/Nông sản...]
- Sản phẩm / Dịch vụ cụ thể: [MÔ TẢ SẢN PHẨM HOẶC DỊCH VỤ CỦA BẠN]
- Trải nghiệm / Bài học xương máu tôi nhận ra: [ĐIỀN 1 BÀI HỌC THẬT TỪ CÔNG VIỆC]
- Khó khăn / Điều trăn trở gần đây: [ĐIỀN KHÓ KHĂN BẠN GẶP PHẢI]

[CẤU TRÚC KỊCH BẢN BẮT BUỘC - 3 PHẦN]:

1. THE HOOK (0s – 8s) — MỞ ĐẦU PHẢN TRỰC GIÁC:
   - Đi thẳng vào bài học xương máu sau [X] năm làm nghề: "Tôi nhận ra điều này sau [X] năm làm nghề...".
   - Tuyên ngôn chạm cảm xúc: Khẳng định làm nghề không phải là phô diễn kỹ xảo hay khoe khoang máy móc, mà là chạm vào cảm giác thật của khách hàng.
   - Gợi ý B-roll (3-4 shot): Bàn làm việc, góc ánh sáng cửa sổ, cận cảnh công cụ làm nghề quen thuộc.

2. THE STORY (8s – 42s) — TỰ SỰ NHẬT KÝ & BẢN SẮC ĐỘC BẢN:
   - Viết như một trang nhật ký cá nhân (Diary Entry) hoặc voice note gửi bạn thân: nói về một buổi sáng chuẩn bị, một ca làm việc khó, một cảm giác trăn trở.
   - So sánh với AI / máy móc: "AI có thể vẽ bản phối cảnh / tạo công thức / viết bài quảng cáo trong 10 giây, nhưng AI không thể cảm nhận được vì sao khoảnh khắc đó lại có ý nghĩa với khách hàng...".
   - Khẳng định: Bản chất mạng xã hội là kết nối con người; sự chân thật và kinh nghiệm sống là thứ duy nhất thuật toán không sao chép được.
   - Gợi ý B-roll (10-15 shot nhịp nhanh 0.8s-1.2s): Các thao tác tay đời thường, chi tiết sản phẩm thật, nến thơm, tách cafe, ngòi bút viết sổ, màn hình làm việc.

3. THE TAKEAWAY (42s – 60s) — BÀI HỌC & CÂU CHỐT CẢM XÚC:
   - Đúc kết công thức 3 câu hỏi cho người xem: 1. Cốt lõi của điều này là gì? 2. Bạn đang học được bài học gì từ khó khăn? 3. Giá trị thực tế người khác soi chiếu được là gì?
   - Câu chốt cảm xúc (Emotional Punchline): "Người ta có thể quên những việc bạn làm trong ngày, nhưng họ sẽ nhớ mãi cảm xúc mà câu chuyện của bạn mang lại."
   - Gợi ý B-roll (3-4 shot): Bàn tay gõ phím, ánh nắng cuối ngày, cử chỉ thư thái.

[QUY TẮC NGÔN TỪ]:
- Viết 100% bằng văn phong mộc mạc, gần gũi của người Việt làm nghề thực chiến.
- TUYỆT ĐỐI KHÔNG dùng văn mẫu AI sáo rỗng: "đắm chìm", "nâng tầm", "tuyệt mỹ", "hãy cùng tôi", "tối ưu hóa vượt trội".
- Ngắt câu ngắn gọn (mỗi câu không quá 15 từ) để khi thu âm đọc tự nhiên, êm tai.
        </pre>
      </div>

      <h3 style="font-family:var(--font-h);font-size:14px;font-weight:800;color:var(--text-title);margin-bottom:10px;">
        💡 3 Kịch Bản Mẫu Ánh Xạ Theo Đúng Cấu Trúc Này Cho Học Viên STU:
      </h3>

      <div class="example-card">
        <div class="example-head">💆 Mẫu 1: Chủ Tiệm Spa &amp; Điều Trị Da Liễu</div>
        <div class="example-body">
          <strong>Hook (0-8s):</strong> "Tôi hiểu làn da hay hơn hẳn sau 6 năm tự tay nặn từng cồi mụn viêm cho khách. Chữa lành cho da không phải là bôi cả tá mỹ phẩm đắt tiền, mà là lắng nghe cơ thể đang muốn nói điều gì."<br>
          <strong>Story (9-42s):</strong> "Trước khi kê bất kỳ liệu trình nào, tôi luôn ngồi hỏi khách về thói quen ăn ngủ và áp lực công việc. AI có thể phân tích ảnh chụp bề mặt da trong 3 giây, nhưng nó không biết vì sao tối hôm đó khách hàng lại khóc và mất ngủ. Sự thấu hiểu và đôi bàn tay chăm sóc là thứ không thuật toán nào thay thế được."<br>
          <strong>Takeaway (43-60s):</strong> "Lần tới chăm sóc da, hãy tự hỏi: Da bạn đang thực sự thiếu ẩm hay đang kiệt sức? Khách hàng có thể quên tên hoạt chất, nhưng họ sẽ nhớ mãi cảm giác nhẹ nhõm khi bước ra khỏi phòng spa."
        </div>
      </div>

      <div class="example-card">
        <div class="example-head">🏡 Mẫu 2: Kiến Trúc Sư &amp; Thiết Kế Nội Thất</div>
        <div class="example-body">
          <strong>Hook (0-8s):</strong> "Tôi vẽ nhà đẹp hơn hẳn sau những lần ngồi lắng nghe tâm sự của các cặp vợ chồng trẻ. Kiến trúc không phải là vẽ cho thật lộng lẫy, mà là làm sao để mỗi khi trở về, họ thấy lòng mình bình yên."<br>
          <strong>Story (9-42s):</strong> "Tôi luôn phác thảo thói quen sống trước khi bấm nhát chuột 3D đầu tiên. AI có thể render một căn phòng như tạp chí trong 10 giây, nhưng nó không hiểu vì sao người mẹ lại cần góc bếp nhìn thấy con đang chơi ngoài ban công. Sự chân thật trong từng góc sống là thứ không render nào sao chép được."<br>
          <strong>Takeaway (43-60s):</strong> "Một ngôi nhà tốt bắt đầu từ 3 câu hỏi: Không gian này phục vụ ai? Thói quen nào cần được nâng đỡ? Và điều gì làm căn nhà ấm cúng? Người ta có thể quên màu sơn tường, nhưng sẽ nhớ mãi cảm giác ấm áp mỗi bữa cơm tối."
        </div>
      </div>

      <div class="example-card">
        <div class="example-head">☕ Mẫu 3: Chủ Quán Cafe &amp; F&amp;B Đời Thường</div>
        <div class="example-body">
          <strong>Hook (0-8s):</strong> "Tôi hiểu khách hàng hơn hẳn sau 4 năm đứng sau quầy pha chế mỗi sáng sớm. Một ly cafe ngon không phải là kỹ thuật latte art cầu kỳ, mà là đúng hương vị làm người ta thấy sẵn sàng cho một ngày mới."<br>
          <strong>Story (9-42s):</strong> "Tôi luôn quan sát ánh mắt khách quen trước khi bắt đầu bấm máy xay. Công thức pha chế thì AI liệt kê ra cả trăm cách, nhưng AI không biết vì sao sáng nay vị khách bàn số 3 lại cần một ly ít đường và một góc ngồi thật yên lặng. Mạng xã hội là để kết nối; sự chăm chút mộc mạc chính là lý do khách quay lại."<br>
          <strong>Takeaway (43-60s):</strong> "Lần tới ghé quán, hãy để ý: Món đồ uống này nói gì về tâm trạng của bạn hôm nay? Khách hàng có thể quên giá tiền của cốc nước, nhưng họ sẽ nhớ mãi sự dịu dàng của buổi sáng hôm đó."
        </div>
      </div>
    </section>
  </main>
</div>

<!-- TOAST -->
<div class="copy-toast" id="copyToast">✓ Đã sao chép Megaprompt vào Clipboard!</div>

<!-- LIGHTBOX -->
<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <button class="lightbox-close" onclick="closeLightbox()">✕</button>
  <img src="" class="lightbox-img" id="lightboxImg" onclick="event.stopPropagation()">
  <div class="lightbox-cap" id="lightboxCap"></div>
</div>

<script>
const SHOTS = {shots_json_str};

const vid = document.getElementById('mainVid');
const playBtn = document.getElementById('playBtn');
const loopBtn = document.getElementById('loopBtn');
const curTimeEl = document.getElementById('curTime');
const sceneListEl = document.getElementById('sceneList');

let isLoop = false;
let loopRange = null;
let currentFilter = 'all';

// Render Scene List
function renderSceneList() {{
  let html = '';
  SHOTS.forEach((s) => {{
    const [id, st, et, dur, img, hl, act, vo_vi, vo_en, phase] = s;
    if (currentFilter !== 'all' && phase !== currentFilter) return;
    const pId = String(id).padStart(2, '0');
    
    html += `
    <div class="scene-row" id="scene-${{id}}" onclick="jumpToShot(${{id}}, ${{st}}, ${{et}})">
      <div class="scene-num-badge">#${{pId}}</div>
      <div class="scene-dur-col">${{dur.toFixed(2)}}s<br><span style="font-size:9.5px;color:var(--text-muted);">${{st.toFixed(1)}}s</span></div>
      <div class="scene-thumb-wrap" onclick="event.stopPropagation(); openLightbox('${{img}}', 'Cảnh ${{pId}} (${{st.toFixed(2)}}s - ${{et.toFixed(2)}}s): ${{hl.replace(/'/g, "\\\\\\'")}}')">
        <img src="${{img}}" loading="lazy" alt="Cảnh ${{pId}}">
      </div>
      <div class="scene-desc-col">
        <div class="scene-headline">${{hl}}</div>
        <div class="scene-action">${{act}}</div>
        ${{vo_vi ? `<div class="scene-vo-line">🎙️ "${{vo_vi}}"</div>` : ''}}
      </div>
    </div>`;
  }});
  sceneListEl.innerHTML = html;
}}

// Filter Shots
function filterShots(phase) {{
  currentFilter = phase;
  document.querySelectorAll('.filter-btn').forEach(btn => {{
    if (btn.textContent.toLowerCase().includes(phase) || (phase === 'all' && btn.textContent.includes('Tất cả'))) {{
      btn.classList.add('active');
    }} else {{
      btn.classList.remove('active');
    }}
  }});
  renderSceneList();
}}

// Switch Section
function switchSection(secId) {{
  document.getElementById('scene-section').style.display = (secId === 'scene-section') ? 'block' : 'none';
  document.getElementById('vo-section').style.display = (secId === 'vo-section') ? 'block' : 'none';
  document.getElementById('prompt-section').style.display = (secId === 'prompt-section') ? 'block' : 'none';

  document.getElementById('tabBtnScene').classList.toggle('active', secId === 'scene-section');
  document.getElementById('tabBtnVo').classList.toggle('active', secId === 'vo-section');
  document.getElementById('tabBtnPrompt').classList.toggle('active', secId === 'prompt-section');
}}

// Video Player Controls
vid.addEventListener('timeupdate', () => {{
  const ct = vid.currentTime;
  const m = Math.floor(ct / 60);
  const s = Math.floor(ct % 60);
  const ms = Math.floor((ct % 1) * 100);
  curTimeEl.textContent = `${{String(m).padStart(2, '0')}}:${{String(s).padStart(2, '0')}}.${{String(ms).padStart(2, '0')}} / 61.53s`;

  if (isLoop && loopRange && ct >= loopRange.end) {{
    vid.currentTime = loopRange.start;
    vid.play();
  }}

  // Highlight active scene
  for (let s of SHOTS) {{
    if (ct >= s[1] && ct <= s[2]) {{
      document.querySelectorAll('.scene-row').forEach(r => r.classList.remove('active-scene'));
      const row = document.getElementById('scene-' + s[0]);
      if (row) {{
        row.classList.add('active-scene');
      }}
      break;
    }}
  }}
}});

function togglePlay() {{
  if (vid.paused) {{
    vid.play();
    playBtn.textContent = '⏸ Tạm dừng';
  }} else {{
    vid.pause();
    playBtn.textContent = '▶ Phát';
  }}
}}

function setSpeed(sp) {{
  vid.playbackRate = sp;
  document.querySelectorAll('.dir-row .btn-c').forEach(b => {{
    if (b.textContent.includes(sp + 'x')) b.classList.add('active');
    else if (b.textContent.includes('x')) b.classList.remove('active');
  }});
}}

function stepFrame(d) {{
  vid.pause();
  playBtn.textContent = '▶ Phát';
  vid.currentTime = Math.max(0, vid.currentTime + (d * (1 / 30)));
}}

function toggleLoop() {{
  isLoop = !isLoop;
  if (isLoop) {{
    loopBtn.classList.add('active');
    loopBtn.textContent = '🔁 Lặp: Bật';
  }} else {{
    loopBtn.classList.remove('active');
    loopBtn.textContent = '🔁 Lặp: Tắt';
    loopRange = null;
  }}
}}

function jumpToShot(id, st, et) {{
  loopRange = {{ start: st, end: et }};
  vid.currentTime = st;
  vid.play();
  playBtn.textContent = '⏸ Tạm dừng';
  
  const row = document.getElementById('scene-' + id);
  if (row) {{
    row.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    document.querySelectorAll('.scene-row').forEach(r => r.classList.remove('active-scene'));
    row.classList.add('active-scene');
  }}
}}

function jumpToTime(st, et) {{
  loopRange = {{ start: st, end: et }};
  vid.currentTime = st;
  vid.play();
  playBtn.textContent = '⏸ Tạm dừng';
}}

// Lightbox
function openLightbox(src, cap) {{
  document.getElementById('lightboxImg').src = src;
  document.getElementById('lightboxCap').textContent = cap || '';
  document.getElementById('lightbox').classList.add('open');
}}
function closeLightbox() {{
  document.getElementById('lightbox').classList.remove('open');
}}

// Copy Megaprompt
function copyMegaprompt() {{
  const code = document.getElementById('promptCode').innerText;
  navigator.clipboard.writeText(code).then(() => {{
    const toast = document.getElementById('copyToast');
    toast.style.display = 'block';
    setTimeout(() => {{ toast.style.display = 'none'; }}, 2500);
  }}).catch(() => {{
    alert('Đã sao chép prompt!');
  }});
}}

document.addEventListener('DOMContentLoaded', () => {{
  renderSceneList();
}});
</script>
</body>
</html>
"""

OUTPUT_PATHS = [
    "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/reports/IG_@Victoria_Morse_DbESOapo-p3_Video_by_victoriamorse.html",
    "/Users/vietmac/Documents/CODE/vietndj.github.io/reports/IG_@Victoria_Morse_DbESOapo-p3_Video_by_victoriamorse.html",
    "/Users/vietmac/Documents/CODE/Video phan tich/output_packages/IG_@Victoria_Morse_DbESOapo-p3_Video_by_victoriamorse/IG_@Victoria_Morse_DbESOapo-p3_Video_by_victoriamorse.html"
]

for p in OUTPUT_PATHS:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[✓] Successfully wrote clean report ({len(html_content)} bytes) to {p}")
