import json
import subprocess
import sys
import os
import time

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

with open('state.json', 'r') as f:
    state = json.load(f)

idx = state['currentIndex']
if idx >= len(state['reports']):
    print("ALL_DONE")
    sys.exit(0)

fileName = state['reports'][idx]
print(f"Processing: {fileName}")

res = run_cmd(f'node process_report.js "{fileName}"')

if "ERROR_QUOTA" in res.stdout or "ERROR_QUOTA" in res.stderr:
    print("ERROR_QUOTA")
    sys.exit(1)

if "NO_IG_LINK" in res.stdout:
    state['results'].append(f"| {idx+1} | {fileName} | - | - | - | - | Không có link IG gốc |")
    state['currentIndex'] += 1
    with open('state.json', 'w') as f:
        json.dump(state, f, indent=4)
    print("SKIPPED_NO_IG")
    sys.exit(0)

if "SINGLE_VIDEO" in res.stdout:
    state['results'].append(f"| {idx+1} | {fileName} | - | - | - | - | Single video, không cần sửa |")
    state['currentIndex'] += 1
    with open('state.json', 'w') as f:
        json.dump(state, f, indent=4)
    print("SKIPPED_SINGLE")
    sys.exit(0)

if "SUCCESS:" in res.stdout:
    ytIds = res.stdout.split("SUCCESS:")[1].strip().split(',')
    
    # Git push
    run_cmd(f'git add reports/"{fileName}".html dist/reports/"{fileName}".html')
    run_cmd(f'git commit -m "Auto update {fileName}"')
    run_cmd('git push origin main')
    
    # Wait for deploy
    liveUrl = f"https://ytuong.fedu.vn/reports/{fileName}.html"
    deployed = False
    print("Waiting for deploy...")
    for i in range(60):
        out = run_cmd(f'curl -s "{liveUrl}" | grep -i "youtube.com/embed/{ytIds[0]}"')
        if out.stdout.strip():
            deployed = True
            break
        time.sleep(5)
        
    if not deployed:
        state['results'].append(f"| {idx+1} | {fileName} | {len(ytIds)} | {','.join(ytIds)} | DEPLOY_TIMEOUT | - | ❌ |")
        state['currentIndex'] += 1
        with open('state.json', 'w') as f:
            json.dump(state, f, indent=4)
        print("DEPLOY_TIMEOUT")
        sys.exit(0)
        
    # Playwright verification script
    pw_script = f"""
const {{ chromium }} = require('playwright');
const fs = require('fs');
(async () => {{
    const browser = await chromium.launch();
    const page = await browser.newPage();
    let hasError = false;
    page.on('pageerror', err => {{
        hasError = true;
        console.error("PAGE_ERROR:", err.message);
    }});
    await page.goto('{liveUrl}', {{ waitUntil: 'networkidle', timeout: 30000 }});
    if (!fs.existsSync('screenshots')) fs.mkdirSync('screenshots');
    await page.screenshot({{ path: 'screenshots/{fileName}.png', fullPage: true }});
    await browser.close();
    if (hasError) process.exit(1);
}})();
"""
    with open('pw.js', 'w') as f:
        f.write(pw_script)
        
    pw_res = run_cmd('node pw.js')
    js_error = 'Yes' if pw_res.returncode != 0 else 'No'
    
    state['current_screenshot'] = f"screenshots/{fileName}.png"
    state['current_live_url'] = liveUrl
    state['current_ytIds'] = ytIds
    state['current_jsError'] = js_error
    state['currentIndex'] += 1
    
    with open('state.json', 'w') as f:
        json.dump(state, f, indent=4)
        
    print(f"READY_FOR_VISION_CHECK:{fileName}")
    sys.exit(0)
    
print("ERROR_UNKNOWN")
print(res.stdout)
print(res.stderr)
sys.exit(1)
