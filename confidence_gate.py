import json
import glob
import os
import argparse
import sys
import subprocess

# Known valid IDs
KNOWN_STYLES = {'walk-and-talk', 'voice-over', 'talking-head', 'storytelling', 'dien-anh', 'chuyen-canh', 'theo-nhip-nhac', 'doi-thuong'}
KNOWN_INDUSTRIES = {'spa-lam-dep', 'thuong-hieu', 'thoi-trang', 'am-thuc', 'du-lich', 'cong-nghe', 'kien-truc', 'the-thao', 'ky-thuat-quay', 'ugc', 'phat-trien-ban-than'}

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in: {filepath}")
        return None

def compute_confidence(video, learned_patterns, corrections_list):
    # If video was previously corrected by mentor, confidence = 95
    if video.get('id') in corrections_list:
        return 95

    score = 30 # Base score

    # +15 if logic_explanation exists and len > 30 chars
    logic_explanation = video.get('logic_explanation', '')
    if logic_explanation and len(logic_explanation) > 30:
        score += 15
        
    # +15 if shooting_style.id is in known STYLES list
    shooting_style = video.get('shooting_style', {})
    if shooting_style and shooting_style.get('id') in KNOWN_STYLES:
        score += 15
        
    # +15 if industry.id is in known INDUSTRIES list
    industry = video.get('industry', {})
    if industry and industry.get('id') in KNOWN_INDUSTRIES:
        score += 15
        
    # +10 if tech_tags has 3+ items
    tech_tags = video.get('tech_tags', [])
    if isinstance(tech_tags, list) and len(tech_tags) >= 3:
        score += 10
        
    # +15 if any LEARNED_PATTERNS rule trigger_keywords appear in title+logic_explanation+purpose
    text_to_check = f"{video.get('title', '')} {logic_explanation} {video.get('purpose', '')}".lower()
    
    keyword_matched = False
    distilled_rules = learned_patterns.get('distilled_rules', [])
    for rule in distilled_rules:
        for keyword in rule.get('trigger_keywords', []):
            if keyword.lower() in text_to_check:
                keyword_matched = True
                break
        if keyword_matched:
            break
            
    if keyword_matched:
        score += 15
        
    # Cap at 100
    return min(100, score)

def send_telegram_summary(summary_text):
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("Telegram credentials not found in env vars. Skipping notification.")
        return

    print("Sending summary to Telegram...")
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": summary_text,
        "parse_mode": "HTML"
    }
    
    # Simple curl call to avoid needing requests library
    import shlex
    payload_json = json.dumps(payload)
    cmd = f"curl -s -X POST -H 'Content-Type: application/json' -d {shlex.quote(payload_json)} {url}"
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def load_corrections():
    """Load danh sách video_id đã được mentor sửa từ training_data.js"""
    td_path = os.path.join(os.path.dirname(__file__), 'training_data.js')
    try:
        with open(td_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Strip "var TRAINING_DATA = " prefix and trailing ";"
        import re
        match = re.search(r'var TRAINING_DATA\s*=\s*(\{[\s\S]*\})\s*;?\s*$', content)
        if match:
            data = json.loads(match.group(1))
            return {c.get('video_id') for c in data.get('corrections', []) if c.get('video_id')}
    except Exception:
        pass
    return set()

def main():
    parser = argparse.ArgumentParser(description="Hybrid Confidence Gate for Video Classifications")
    parser.add_argument('--dry-run', action='store_true', help='Do not save audit_queue.json')
    parser.add_argument('--telegram', action='store_true', help='Send summary via Telegram')
    args = parser.parse_args()

    # Load data — master_classifications.json is a dict {video_id: video_data}
    classifications_dict = load_json('master_classifications.json') or {}
    learned_patterns = load_json('LEARNED_PATTERNS.json') or {}
    corrections_list = load_corrections()

    results = {'GREEN': [], 'YELLOW': [], 'RED': []}
    audit_queue = []

    for video_id, video in classifications_dict.items():
        if not isinstance(video, dict):
            continue
        if video.get('is_excluded', False):
            continue

        score = compute_confidence(video, learned_patterns, corrections_list)

        tier = 'RED'
        if score >= 85:
            tier = 'GREEN'
        elif score >= 50:
            tier = 'YELLOW'

        results[tier].append(video)

        if tier in ['YELLOW', 'RED']:
            # LỌC GHOST ITEMS: Chỉ đưa vào hàng đợi nếu ĐÃ CÓ báo cáo HTML
            html_exists = False
            for r in glob.glob("reports/*.html"):
                if video.get('id', video_id) in r:
                    html_exists = True
                    break
            
            if not html_exists:
                continue

            shooting_style = video.get('shooting_style', {})
            industry = video.get('industry', {})
            if isinstance(industry, list):
                industry = industry[0] if industry else {}
            if isinstance(shooting_style, str):
                shooting_style = {'id': shooting_style, 'name': shooting_style}
            if isinstance(industry, str):
                industry = {'id': industry, 'name': industry}

            audit_queue.append({
                'id': video.get('id', video_id),
                'creator': video.get('creator', ''),
                'title': video.get('title', ''),
                'current_style': shooting_style.get('name', '') if isinstance(shooting_style, dict) else str(shooting_style),
                'current_industry': industry.get('name', '') if isinstance(industry, dict) else str(industry),
                'tech_tags': video.get('tech_tags', []),
                'confidence_score': score,
                'tier': tier,
                'reason_flagged': f"Confidence {score}/100"
            })

    total = sum(len(v) for v in results.values())
    print(f"\n{Colors.BOLD}{'='*50}")
    print(f"  CONFIDENCE GATE AUDIT — Kho Ý Tưởng")
    print(f"{'='*50}{Colors.ENDC}")
    print(f"{Colors.GREEN}  ✅ GREEN (≥85) Auto-approved:      {len(results['GREEN']):>4}{Colors.ENDC}")
    print(f"{Colors.YELLOW}  ⚠️  YELLOW (50-84) Cần anh duyệt:  {len(results['YELLOW']):>4}{Colors.ENDC}")
    print(f"{Colors.RED}  🔴 RED (<50) Ưu tiên duyệt:       {len(results['RED']):>4}{Colors.ENDC}")
    print(f"  {'─'*46}")
    print(f"  Tổng video xử lý:                  {total:>4}")
    pct_auto = round(len(results['GREEN'])/total*100, 1) if total else 0
    print(f"  Tỷ lệ auto-approve:                {pct_auto}%\n")
    
    # Save queue
    if not args.dry_run:
        with open('audit_queue.json', 'w', encoding='utf-8') as f:
            json.dump(audit_queue, f, indent=4, ensure_ascii=False)
        print(f"Saved {len(audit_queue)} items to audit_queue.json")
    else:
        print("Dry run mode: audit_queue.json was not saved.")

    # Telegram notification
    if args.telegram:
        summary_text = (
            f"<b>Confidence Gate Audit Summary</b>\n"
            f"🟢 Auto-approved: {len(results['GREEN'])}\n"
            f"🟡 Needs mentor review: {len(results['YELLOW'])}\n"
            f"🔴 Priority review: {len(results['RED'])}\n"
            f"Total processed: {len(classifications)}"
        )
        send_telegram_summary(summary_text)

if __name__ == '__main__':
    main()
