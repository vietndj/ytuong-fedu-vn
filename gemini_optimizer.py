import os
import json
import time
import argparse
import logging
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

MASTER_JSON_PATH = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/master_classifications.json"
STATE_JSON_PATH = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn/optimizer_state.json"

def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key
        
    config_path = os.path.expanduser("~/.gemini/config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                return config.get("api_key") or config.get("GEMINI_API_KEY")
        except Exception as e:
            logger.warning(f"Failed to read {config_path}: {e}")
            
    # Try Antigravity config
    agy_config_path = os.path.expanduser("~/.gemini/antigravity/config.json")
    if os.path.exists(agy_config_path):
         try:
            with open(agy_config_path, "r") as f:
                config = json.load(f)
                return config.get("api_key") or config.get("GEMINI_API_KEY")
         except Exception as e:
            pass
            
    return None

def load_data():
    with open(MASTER_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(MASTER_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_state():
    if os.path.exists(STATE_JSON_PATH):
        try:
            with open(STATE_JSON_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"processed_keys": []}
    return {"processed_keys": []}

def save_state(state):
    with open(STATE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def needs_processing(item, args):
    if args.mode == 'enrich':
        fedu_opt = item.get("fedu_optimization")
        if not fedu_opt or (isinstance(fedu_opt, dict) and len(str(fedu_opt.get("key_optimization_point", ""))) < 10):
            return True
        logic = item.get("logic_explanation", "")
        if len(str(logic)) < 100:
            return True
        if "practice_scenario" not in item:
            return True
        if "ig_seeding_hook" not in item:
            return True
    elif args.mode == 'fix-slugs':
        return True # Filter later based on slugs
    elif args.mode == 'add-practice':
        if "practice_scenario" not in item:
            return True
    return False

def build_prompt(item, mode):
    item_str = json.dumps(item, ensure_ascii=False, indent=2)
    return f"""
Bạn là một chuyên gia phân tích và tối ưu hóa nội dung video thực chiến.
Dựa vào dữ liệu video sau, hãy tạo ra các trường thông tin còn thiếu hoặc nâng cấp các trường hiện tại.

DỮ LIỆU VIDEO GỐC:
{item_str}

YÊU CẦU ĐẦU RA (JSON format - chỉ trả về đúng JSON, không format markdown, không giải thích):
{{
  "fedu_optimization": {{
    "key_optimization_point": "Hướng dẫn tối ưu hóa video logic cho riêng ngành này (sâu sắc, thực chiến, không văn mẫu)"
  }},
  "logic_explanation": "Giải thích logic kịch bản, tâm lý học đằng sau video, cấu trúc hook, thân, kết (phải dài hơn 100 ký tự)",
  "shooting_style_slug": "chuỗi-slug-chuẩn-hóa (ví dụ: dien-anh, chuyen-canh, talking-head)",
  "industry_slug": "chuỗi-slug-ngành-chuẩn-hóa (ví dụ: spa-lam-dep, thoi-trang, phat-trien-ban-than)",
  "practice_scenario": "Một tình huống thực hành cụ thể dành cho học viên (ngắn gọn, action-oriented)",
  "ig_seeding_hook": "Một câu hook giật gân, khơi gợi tò mò để dùng đi comment seeding trên Instagram"
}}
"""

def parse_llm_response(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}\n{text}")
        return None

def process_batch(items_to_process, model, args):
    results = {}
    for key, item in items_to_process:
        logger.info(f"Processing: {key}")
        if args.dry_run:
            results[key] = {"status": "dry_run"}
            continue
            
        prompt = build_prompt(item, args.mode)
        
        retries = 3
        backoff = 2
        success = False
        
        while retries > 0 and not success:
            try:
                # Need to specify generation_config to encourage JSON if supported, or just text
                response = model.generate_content(prompt, generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                ))
                parsed = parse_llm_response(response.text)
                if parsed:
                    results[key] = parsed
                    success = True
                else:
                    logger.warning(f"Invalid JSON for {key}")
                    break
            except ResourceExhausted:
                logger.warning(f"Rate limited. Waiting {backoff}s...")
                time.sleep(backoff)
                backoff *= 2
                retries -= 1
            except Exception as e:
                logger.error(f"Error calling API for {key}: {e}")
                break
                
        time.sleep(1) # Base delay to prevent rate limit
        
    return results

def apply_results(data, results):
    for key, updates in results.items():
        if key not in data or updates.get("status") == "dry_run":
            continue
            
        item = data[key]
        if "fedu_optimization" in updates:
            item["fedu_optimization"] = updates["fedu_optimization"]
        if "logic_explanation" in updates:
            item["logic_explanation"] = updates["logic_explanation"]
        if "practice_scenario" in updates:
            item["practice_scenario"] = updates["practice_scenario"]
        if "ig_seeding_hook" in updates:
            item["ig_seeding_hook"] = updates["ig_seeding_hook"]
            
        # Update slugs if valid
        ss_slug = updates.get("shooting_style_slug")
        if ss_slug and isinstance(item.get("shooting_style"), dict):
            item["shooting_style"]["id"] = ss_slug
            
        ind_slug = updates.get("industry_slug")
        if ind_slug and isinstance(item.get("industry"), dict):
            item["industry"]["id"] = ind_slug

def main():
    parser = argparse.ArgumentParser(description="Gemini Optimizer for Video Ideas Bank")
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen without calling API")
    parser.add_argument("--batch-size", type=int, default=10, help="Number of items per batch")
    parser.add_argument("--mode", type=str, choices=["enrich", "fix-slugs", "add-practice"], default="enrich", help="Processing mode")
    parser.add_argument("--skip-done", action="store_true", help="Skip items already processed in state JSON")
    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key and not args.dry_run:
        logger.error("GEMINI_API_KEY not found. Please set the environment variable.")
        return

    if not args.dry_run:
        genai.configure(api_key=api_key)
        
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        logger.warning(f"Could not load gemini-2.5-flash, trying gemini-1.5-flash. Error: {e}")
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception:
            model = None

    data = load_data()
    state = load_state()
    
    processed_keys = set(state.get("processed_keys", []))
    
    # Filter items
    items_to_process = []
    for key, item in data.items():
        if args.skip_done and key in processed_keys:
            continue
            
        if needs_processing(item, args):
            items_to_process.append((key, item))
            
    total_items = len(items_to_process)
    logger.info(f"Total items needing processing: {total_items}")
    
    if total_items == 0:
        logger.info("Nothing to do.")
        return
        
    # Process in batches
    for i in range(0, total_items, args.batch_size):
        batch = items_to_process[i:i + args.batch_size]
        logger.info(f"--- Batch {i//args.batch_size + 1}/{(total_items + args.batch_size - 1)//args.batch_size} ({len(batch)} items) ---")
        
        results = process_batch(batch, model, args)
        
        if not args.dry_run:
            apply_results(data, results)
            save_data(data)
            
            # Update state
            for key in results.keys():
                if key not in processed_keys:
                    processed_keys.add(key)
                    state["processed_keys"].append(key)
            save_state(state)
            
        logger.info(f"Batch completed.")

if __name__ == "__main__":
    main()
