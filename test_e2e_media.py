import os
import re
import concurrent.futures
import requests

def get_drive_ids_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            matches = re.findall(r'api/video\?id=([a-zA-Z0-9_-]+)', content)
            return matches
    except Exception as e:
        return []

def main():
    base_dir = "/Users/vietmac/Documents/CODE/ytuong-fedu-vn"
    ideas_js = os.path.join(base_dir, "ideas_data.js")
    reports_dir = os.path.join(base_dir, "reports")
    
    ids = set()
    
    if os.path.exists(ideas_js):
        ids.update(get_drive_ids_from_file(ideas_js))
        
    if os.path.exists(reports_dir):
        for root, dirs, files in os.walk(reports_dir):
            for file in files:
                if file.endswith('.html'):
                    ids.update(get_drive_ids_from_file(os.path.join(root, file)))
                    
    id_list = list(ids)
    print(f"Tổng số ID đã quét: {len(id_list)}")
    
    pass_ids = []
    fail_ids = []
    
    def check_id(drive_id):
        url = f"https://ytuong.fedu.vn/api/video?id={drive_id}"
        try:
            response = requests.head(url, timeout=10)
            if response.status_code == 200:
                return (drive_id, True)
            else:
                return (drive_id, False)
        except Exception:
            return (drive_id, False)
            
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_id, id_list)
        
    for drive_id, passed in results:
        if passed:
            pass_ids.append(drive_id)
        else:
            fail_ids.append(drive_id)
            
    print(f"Số ID Pass: {len(pass_ids)}")
    print(f"Số ID Fail: {len(fail_ids)}")
    if fail_ids:
        print("Chi tiết các ID bị hỏng:")
        for fail_id in fail_ids:
            print(f"- {fail_id}")

if __name__ == "__main__":
    main()
