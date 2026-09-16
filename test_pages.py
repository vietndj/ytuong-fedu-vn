import requests

names = ["ytuong-fedu-vn", "ytuong", "ytuong-fedu", "fedu-ytuong", "vietndj-ytuong", "kho-ytuong"]
for name in names:
    url = f"https://{name}.pages.dev"
    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 200 and "ideas_data.js" in r.text:
            print(f"FOUND: {url}")
    except:
        pass
