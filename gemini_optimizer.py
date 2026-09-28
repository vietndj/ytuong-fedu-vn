#!/usr/bin/env python3
"""
gemini_optimizer.py — Chạy liên tục tiêu token Gemini để làm giàu dữ liệu ytuong.fedu.vn
Usage:
  python3 gemini_optimizer.py                        # Enrich 578 items, batch 10
  python3 gemini_optimizer.py --batch-size 20        # Batch lớn hơn
  python3 gemini_optimizer.py --dry-run --batch-size 3
  python3 gemini_optimizer.py --skip-done            # Resume từ lần trước
  python3 gemini_optimizer.py --model gemini-pro-latest  # Dùng Pro (chất lượng cao hơn)
  python3 gemini_optimizer.py --mode add-practice    # Chỉ thêm practice_scenario
"""

import os
import json
import time
import argparse
import logging
import sys
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("/Users/vietmac/Documents/CODE/ytuong-fedu-vn/optimizer.log", encoding="utf-8"),
    ]
)
logger = logging.getLogger(__name__)

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn"
MASTER_JSON_PATH = f"{BASE_DIR}/dist/master_classifications.json"
STATE_JSON_PATH  = f"{BASE_DIR}/optimizer_state.json"
IDEAS_JS_PATH    = f"{BASE_DIR}/dist/ideas_data.js"

# ── API Key ────────────────────────────────────────────────────────────────────
def get_api_key():
    # 1. ENV
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    # 2. Antigravity registry path
    agy_path = os.path.expanduser("~/.config/gemini/api_key")
    if os.path.exists(agy_path):
        return open(agy_path).read().strip()
    # 3. ~/.gemini/api_key
    fallback = os.path.expanduser("~/.gemini/api_key")
    if os.path.exists(fallback):
        return open(fallback).read().strip()
    return None

# ── Data I/O ──────────────────────────────────────────────────────────────────
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
            pass
    return {"processed_keys": [], "total_done": 0, "errors": 0}

def save_state(state):
    with open(STATE_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

# ── Item filter ───────────────────────────────────────────────────────────────
def needs_processing(item, mode):
    if mode == "enrich":
        fedu = item.get("fedu_optimization")
        if not fedu:
            return True
        if isinstance(fedu, dict):
            kp = str(fedu.get("key_optimization_point", ""))
            ps = str(fedu.get("practice_focus", ""))
            # Thiếu practice_focus hoặc ig_seeding_hook
            if len(kp) < 30:
                return True
            if not fedu.get("ig_seeding_hook"):
                return True
            if not fedu.get("practice_focus"):
                return True
        logic = str(item.get("logic_explanation", ""))
        if len(logic) < 80:
            return True
        if not item.get("practice_scenario"):
            return True
        return False
    elif mode == "add-practice":
        return not item.get("practice_scenario")
    elif mode == "fix-logic":
        return len(str(item.get("logic_explanation", ""))) < 80
    elif mode == "full":
        return True  # Reprocess everything
    return False

# ── Prompt builder ─────────────────────────────────────────────────────────────
def build_prompt(item):
    # Strip heavy fields to save tokens
    trimmed = {
        "id": item.get("id", ""),
        "creator": item.get("creator", ""),
        "title": item.get("title", ""),
        "shooting_style": item.get("shooting_style", {}),
        "industry": item.get("industry", {}),
        "purpose": item.get("purpose", ""),
        "tech_tags": item.get("tech_tags", []),
        "logic_explanation": item.get("logic_explanation", ""),
        "quick_takeaway": item.get("quick_takeaway", ""),
        "country": item.get("country", ""),
        "transition_level": item.get("transition_level", ""),
    }
    item_str = json.dumps(trimmed, ensure_ascii=False, indent=2)

    return f"""Bạn là chuyên gia phân tích video marketing thực chiến — huấn luyện kỹ năng làm video cho người Việt.

Dữ liệu video Instagram cần phân tích:
{item_str}

Trả về ĐÚNG JSON (không markdown, không giải thích thêm):
{{
  "fedu_optimization": {{
    "key_optimization_point": "1-2 câu cô đọng: kỹ thuật/cấu trúc tâm lý đặc trưng video này (chuyên sâu, không văn mẫu, tiếng Việt)",
    "practice_focus": "Bài tập thực chiến 1 câu: học viên cần quay/dựng thử ĐÚNG kỹ thuật nào, theo bối cảnh ngành nào",
    "ig_seeding_hook": "1 câu comment ngắn, kích thích tò mò, phù hợp để seeding dưới video gốc trên Instagram",
    "course_industry_mapping": "Tên ngành phù hợp nhất với học viên khóa video của anh Việt (VD: Spa & Làm Đẹp, Bất Động Sản, Coaching...)"
  }},
  "logic_explanation": "Giải thích cấu trúc kịch bản: hook là gì, thân bài tạo cảm xúc/tò mò như thế nào, kết thúc dẫn action gì — tối thiểu 120 ký tự",
  "practice_scenario": "Nếu bạn bán [ngành X], áp dụng video này bằng cách: [hành động cụ thể 1-2 câu]"
}}"""

# ── Response parser ────────────────────────────────────────────────────────────
def parse_response(text):
    text = text.strip()
    # Strip markdown fences
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try extracting first {...} block
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except Exception:
                pass
    logger.warning(f"Could not parse JSON from response: {text[:200]}")
    return None

# ── Apply updates to item ─────────────────────────────────────────────────────
def apply_update(item, updates):
    if not updates:
        return
    if "fedu_optimization" in updates and updates["fedu_optimization"]:
        existing = item.get("fedu_optimization") or {}
        if isinstance(existing, dict):
            existing.update(updates["fedu_optimization"])
            item["fedu_optimization"] = existing
        else:
            item["fedu_optimization"] = updates["fedu_optimization"]
    if "logic_explanation" in updates:
        new_logic = str(updates["logic_explanation"])
        old_logic = str(item.get("logic_explanation", ""))
        if len(new_logic) > len(old_logic):
            item["logic_explanation"] = new_logic
    if "practice_scenario" in updates and updates["practice_scenario"]:
        item["practice_scenario"] = updates["practice_scenario"]

# ── Stats printer ─────────────────────────────────────────────────────────────
def print_stats(done, total, errors, batch_num, total_batches, elapsed):
    pct = done * 100 // total if total else 0
    bar_len = 30
    filled = bar_len * done // total if total else 0
    bar = "█" * filled + "░" * (bar_len - filled)
    eta = ""
    if done > 0:
        per_item = elapsed / done
        remaining = (total - done) * per_item
        mins = int(remaining // 60)
        eta = f" ETA ~{mins}m"
    print(f"\n  [{bar}] {pct}% — {done}/{total} items  |  Batch {batch_num}/{total_batches}  |  Lỗi: {errors}{eta}\n")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Gemini Optimizer — ytuong.fedu.vn ideas bank")
    parser.add_argument("--dry-run", action="store_true", help="Không gọi API, chỉ in danh sách items")
    parser.add_argument("--batch-size", type=int, default=10, help="Số items mỗi batch (default: 10)")
    parser.add_argument("--mode", choices=["enrich", "add-practice", "fix-logic", "full"], default="enrich",
                        help="Mode xử lý (default: enrich)")
    parser.add_argument("--skip-done", action="store_true", help="Bỏ qua items đã xử lý trong session trước")
    parser.add_argument("--model", default="gemini-flash-latest",
                        help="Gemini model (default: gemini-flash-latest). Dùng gemini-pro-latest để chất lượng cao hơn")
    parser.add_argument("--delay", type=float, default=1.5,
                        help="Delay giữa mỗi API call (giây, default: 1.5)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Giới hạn số items xử lý (0 = không giới hạn)")
    args = parser.parse_args()

    # ── Setup Gemini client ──
    client = None
    if not args.dry_run:
        api_key = get_api_key()
        if not api_key:
            logger.error("❌ Không tìm thấy GEMINI_API_KEY. File: ~/.config/gemini/api_key")
            sys.exit(1)
        try:
            import google.genai as genai
            client = genai.Client(api_key=api_key)
            # Quick connectivity test
            test = client.models.generate_content(model=args.model, contents="OK?")
            logger.info(f"✅ Gemini API kết nối OK — Model: {args.model}")
        except Exception as e:
            logger.error(f"❌ Gemini API lỗi: {e}")
            sys.exit(1)

    # ── Load data ──
    data   = load_data()
    state  = load_state()
    processed_set = set(state.get("processed_keys", []))

    # ── Filter items ──
    queue = []
    for key, item in data.items():
        if args.skip_done and key in processed_set:
            continue
        if needs_processing(item, args.mode):
            queue.append((key, item))

    if args.limit > 0:
        queue = queue[:args.limit]

    total = len(queue)
    logger.info(f"📋 Tổng items cần xử lý: {total}  |  Mode: {args.mode}  |  Dry-run: {args.dry_run}")

    if total == 0:
        logger.info("✅ Tất cả items đã đủ data. Không cần xử lý thêm.")
        return

    if args.dry_run:
        for i, (k, _) in enumerate(queue[:20]):
            print(f"  [{i+1}] {k[:80]}")
        if total > 20:
            print(f"  ... và {total - 20} items khác")
        return

    # ── Process loop ──
    total_batches = (total + args.batch_size - 1) // args.batch_size
    done   = state.get("total_done", 0)
    errors = state.get("errors", 0)
    start  = time.time()
    session_done = 0

    print(f"\n🚀 Bắt đầu chạy {total} items / {total_batches} batches\n")

    for batch_num, i in enumerate(range(0, total, args.batch_size), 1):
        batch = queue[i : i + args.batch_size]
        logger.info(f"── Batch {batch_num}/{total_batches} ({len(batch)} items) ──")

        for key, item in batch:
            logger.info(f"  ⚙ {key[:70]}")
            prompt = build_prompt(item)

            retries = 4
            backoff = 2
            success = False

            while retries > 0:
                try:
                    resp = client.models.generate_content(model=args.model, contents=prompt)
                    updates = parse_response(resp.text)
                    if updates:
                        apply_update(data[key], updates)
                        success = True
                        session_done += 1
                        done += 1
                    else:
                        errors += 1
                    break
                except Exception as e:
                    err_str = str(e)
                    if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                        logger.warning(f"  ⏳ Rate limit — chờ {backoff}s...")
                        time.sleep(backoff)
                        backoff = min(backoff * 2, 60)
                        retries -= 1
                    else:
                        logger.error(f"  ❌ API error: {err_str[:100]}")
                        errors += 1
                        break

            # Mark processed
            if key not in processed_set:
                processed_set.add(key)
                state["processed_keys"].append(key)

            time.sleep(args.delay)

        # ── Save after every batch ──
        save_data(data)
        state["total_done"] = done
        state["errors"] = errors
        save_state(state)

        elapsed = time.time() - start
        print_stats(session_done, total, errors, batch_num, total_batches, elapsed)
        logger.info(f"  💾 Saved — {done} done total, {errors} errors")

    elapsed = time.time() - start
    print(f"\n{'='*60}")
    print(f"✅ HOÀN THÀNH")
    print(f"   Xử lý: {session_done} items  |  Lỗi: {errors}  |  Thời gian: {elapsed/60:.1f} phút")
    print(f"   File: {MASTER_JSON_PATH}")
    print(f"{'='*60}\n")

    # Suggest rebuild
    print("👉 Rebuild ideas_data.js:")
    print(f"   python3 {BASE_DIR}/build_ideas_bank.py\n")


if __name__ == "__main__":
    main()
