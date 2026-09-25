import json
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

def main():
    parser = argparse.ArgumentParser(description="Hybrid Confidence Gate for Video Classifications")
    parser.add_argument('--dry-run', action='store_true', help='Do not save audit_queue.json')
    parser.add_argument('--telegram', action='store_true', help='Send summary via Telegram')
    args = parser.parse_args()

    # Load data
    classifications = load_json('master_classifications.json') or []
    learned_patterns = load_json('LEARNED_PATTERNS.json') or {}
    
    # Mocking corrections list based on context - normally this would load from a file
    # If there's an existing corrections file, you can modify this logic.
    corrections_list = set()
    
    results = {
        'GREEN': [],
        'YELLOW': [],
        'RED': []
    }
    
    audit_queue = []
    
    for video in classifications:
        score = compute_confidence(video, learned_patterns, corrections_list)
        
        tier = 'RED'
        if score >= 85:
            tier = 'GREEN'
        elif score >= 50:
            tier = 'YELLOW'
            
        results[tier].append(video)
        
        if tier in ['YELLOW', 'RED']:
            audit_queue.append({
                'id': video.get('id'),
                'creator': video.get('creator'),
                'title': video.get('title'),
                'current_style': video.get('shooting_style', {}).get('name'),
                'current_industry': video.get('industry', {}).get('name'),
                'confidence_score': score,
                'tier': tier,
                'reason_flagged': f"Low confidence score ({score})"
            })

    # Terminal output
    print(f"\n{Colors.BOLD}--- Confidence Gate Audit Summary ---{Colors.ENDC}")
    print(f"{Colors.GREEN}GREEN (≥85) Auto-approved:{Colors.ENDC} {len(results['GREEN'])}")
    print(f"{Colors.YELLOW}YELLOW (50-84) Needs mentor review:{Colors.ENDC} {len(results['YELLOW'])}")
    print(f"{Colors.RED}RED (<50) Priority review:{Colors.ENDC} {len(results['RED'])}")
    print(f"Total videos processed: {len(classifications)}\n")
    
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
