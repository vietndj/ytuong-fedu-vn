import asyncio
import os
import subprocess
import time
import json
from playwright.async_api import async_playwright

async def main():
    # 1. Start local server for dist/
    server = subprocess.Popen(
        ['python3', '-m', 'http.server', '8089', '--directory', 'dist'],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    time.sleep(1)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={'width': 1440, 'height': 900})
            page = await context.new_page()

            print("Navigating to http://127.0.0.1:8089/ ...")
            await page.goto("http://127.0.0.1:8089/", wait_until='networkidle')
            await page.wait_for_timeout(2000)

            # Get ideas from page
            ideas = await page.evaluate("""() => {
                return (window.FEDU_IDEAS_DATABASE?.ideas || []).filter(x => !x.is_excluded);
            }""")
            print(f"Loaded {len(ideas)} active ideas in page context.")

            # Target test specific items from user screenshots:
            test_targets = [
                # Image 1
                "DYKO1v3g3U2", # Withyuee #04
                "DXbzOkygG0v", # Withyuee #05
                # Image 2
                "IG_@Turkish_Airlines_DaxjeQ4A9dP_Video_by_turkishairlines", # Turkish #16
                "IG_@Steven_🇻🇳_Vu_DchxEAkJ9Hw_Video_by_steven.vuu",         # Steven Vu #17
                "IG_@Simeon_Kraeft_DY2XJzdioZg_Video_by_simeonkraeft",     # Simeon Kraeft #18
                # Image 3
                "DYcM_9FPr7I", # Jazzie #31
                "DXoss18j011", # Jazzie #32
                "DWERTvEjy7k"  # Jazzie #33
            ]

            print("\n=== TESTING TARGET USER ITEMS ===")
            for target_id in test_targets:
                res = await page.evaluate(f"""(id) => {{
                    const item = window.FEDU_IDEAS_DATABASE?.ideas?.find(x => x.id === id);
                    if (!item) return {{ id, error: 'Not found' }};
                    
                    const hook = item.media?.thumb_hook;
                    const key = item.media?.thumb_key;
                    const rep = item.media?.report_url;
                    const shots = item.media?.shots_count;
                    
                    return {{
                        id,
                        title: item.title_vi,
                        creator: item.creator?.name,
                        hook,
                        key,
                        report_url: rep,
                        shots_count: shots
                    }};
                }}""", target_id)
                print(f"\nTarget: {res.get('creator')} - {res.get('title')}")
                print(f"  ID: {res.get('id')}")
                print(f"  shots_count: {res.get('shots_count')}")
                print(f"  report_url: '{res.get('report_url')}'")

                # Simulate click on card
                action_result = await page.evaluate(f"""async (id) => {{
                    let openedModal = null;
                    let iframeSrc = null;
                    let toastMsg = null;
                    
                    // Spy on showToast
                    const origToast = window.showToast;
                    window.showToast = (msg) => {{ toastMsg = msg; if (origToast) origToast(msg); }};
                    
                    openReportModal(id);
                    await new Promise(r => setTimeout(r, 600));
                    
                    const repModal = document.getElementById('reportEmbedModal');
                    const vidModal = document.getElementById('videoModal');
                    const iframe = document.getElementById('reportModalIframe');
                    
                    if (repModal?.classList.contains('open')) {{
                        openedModal = 'reportEmbedModal';
                        iframeSrc = iframe?.src || null;
                    }} else if (vidModal?.classList.contains('open')) {{
                        openedModal = 'videoModal (fallback)';
                    }}
                    
                    // Close modals
                    repModal?.classList.remove('open');
                    vidModal?.classList.remove('open');
                    window.showToast = origToast;
                    
                    return {{ openedModal, iframeSrc, toastMsg }};
                }}""", target_id)
                print(f"  Action Result: Modal={action_result.get('openedModal')} | IframeSrc={action_result.get('iframeSrc')} | Toast={action_result.get('toastMsg')}")

            # Now test ALL ideas for report click behavior and thumbnail status
            print("\nScanning all ideas for report modal & iframe loading...")
            full_audit = []
            for item in ideas:
                iid = item['id']
                rep_url = item.get('media', {}).get('report_url', '')
                shots = item.get('media', {}).get('shots_count', 0)
                title = item.get('title_vi', '')
                creator = item.get('creator', {}).get('name', '')

                # Check what openReportModal does
                click_res = await page.evaluate(f"""(id) => {{
                    const item = window.FEDU_IDEAS_DATABASE?.ideas?.find(x => x.id === id);
                    if (!item) return {{ status: 'NOT_FOUND' }};
                    if (!item.media?.report_url) {{
                        if (item.media?.video_url || item.media?.youtube_id || item.media?.youtube_embed) {{
                            return {{ status: 'FALLBACK_TO_VIDEO_MODAL', reason: 'report_url is empty' }};
                        }}
                        return {{ status: 'SHOW_TOAST', reason: 'report_url is empty & no video' }};
                    }}
                    return {{ status: 'OPENS_REPORT_MODAL', report_url: item.media.report_url }};
                }}""", iid)

                full_audit.append({
                    'id': iid,
                    'creator': creator,
                    'title': title,
                    'shots_count': shots,
                    'report_url': rep_url,
                    'click_status': click_res['status']
                })

            with open('scratch/simulated_click_audit.json', 'w', encoding='utf-8') as out:
                json.dump(full_audit, out, ensure_ascii=False, indent=2)

            no_reports = [x for x in full_audit if x['click_status'] != 'OPENS_REPORT_MODAL']
            print(f"\nTotal ideas where click DOES NOT open report modal: {len(no_reports)}")
            for nr in no_reports[:10]:
                print(f"  [{nr['id']}] {nr['creator']} | Status: {nr['click_status']} | Title: {nr['title'][:45]}")

            await browser.close()
    finally:
        server.terminate()

asyncio.run(main())
