import subprocess
import urllib.parse

def curl_status(url):
    if not url: return 0
    cmd = ['curl', '-s', '-I', '-o', '/dev/null', '-w', '%{http_code}', '--connect-timeout', '5', '--max-time', '10', url]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        return int(r.stdout.strip()) if r.stdout.strip().isdigit() else 0
    except:
        return 0

# Check items 1-6 for shot_02
folders = [
    "IG_@The_Tree_Church_Logan_DcoGfdghNwd_Video_by_treechurchlogan",
    "IG_@daiki.shino_Dbk4X4tjJ8A_London_Cinematic_Video_Postcards_Carousel",
    "IG_@JAEHYUNG_DdWa3o2zc0w_Video_by__hyungs",
    "IG_@Five_Oars_Coffee_Roasters_DcxcVGtxjNl_Video_by_focr.sg",
    "IG_@%EA%B1%B0%EB%B6%81%EC%9D%B4_%EC%86%8C%EC%98%81_Db0tHr8Bs7x_Video_by_slowkoreanvlog",
    "IG_@3413882081_Dcx7pQpS6zs_Video_by_syooaann"
]

print("Checking shot_02 for items 1-6:")
for f in folders:
    url_02 = f"https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/{f}/shot_02_mid.webp"
    code = curl_status(url_02)
    print(f"  {f[:40]}... shot_02: {code}")

# Check Ulanzi YouTube and JPGs
print("\nChecking Ulanzi alternatives:")
ulanzi_tests = [
    "https://img.youtube.com/vi/InZ6HgASLnE/hqdefault.jpg",
    "https://img.youtube.com/vi/InZ6HgASLnE/mqdefault.jpg",
    "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/LAZADA_Ulanzi_%C4%90%C3%A8n_LED_Thanh_B%C6%A1m_H%C6%A1i_UA20%2C__thumb.jpg",
    "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/LAZADA_Ulanzi_Ch%C3%A2n_%C4%90%E1%BA%BF_T%E1%BB%B1_S%C6%B0%E1%BB%9Bng_C%C3%B3_T%E1%BB%AB_T%C3%ADnh__thumb.jpg"
]
for u in ulanzi_tests:
    print(f"  {u.split('/')[-1]}: {curl_status(u)}")
