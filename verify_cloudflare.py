import requests
import time

url_html = f"https://ytuong.fedu.vn?t={time.time()}"
url_js = f"https://ytuong.fedu.vn/ideas_data.js?t={time.time()}"

try:
    r_html = requests.get(url_html)
    print("=== HTML Headers ===")
    for k, v in r_html.headers.items():
        if k.lower() in ['server', 'x-vercel-id', 'cf-ray', 'cf-cache-status', 'x-robots-tag']:
            print(f"{k}: {v}")
            
    r_js = requests.get(url_js)
    if 'hook treo máy thẳng đứng' in r_js.text:
        print("\n[SUCCESS] JS is updated with new texts!")
    else:
        print("\n[FAIL] JS still has old texts!")
except Exception as e:
    print(f"Error: {e}")
