import requests

urls = [
    "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/IG_%40withyuee_DYKO1v3g3U2_Video_by_withyuee/shot_01_mid.jpg",
    "https://pub-447bd44dfdac4938912655c855b8631c.r2.dev/images/IG_%40withyuee_DYKO1v3g3U2_Video_by_withyuee/extracted_shots/shot_01_mid.jpg"
]

for url in urls:
    try:
        r = requests.head(url)
        print(f"{url}: {r.status_code}")
    except Exception as e:
        print(f"{url}: ERROR {e}")
