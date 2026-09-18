import urllib.request
import os
import concurrent.futures

os.makedirs('/tmp/review_25_29', exist_ok=True)
urls = [
    ("https://media.fedu.vn/images/IG_%403413882081_Dcx7pQpS6zs_Video_by_syooaann/shot_01_mid.jpg", "/tmp/review_25_29/shot_25.jpg"),
    ("https://media.fedu.vn/images/IG_%40Megan_Tan_DOd8XMMjxcH_Video_by_megantanhweewen/shot_01_mid.jpg", "/tmp/review_25_29/shot_26.jpg"),
    ("https://media.fedu.vn/images/IG_%40Caleb_Natale_Dcbn7Bix-X-_Video_by_calebnatale/shot_01_mid.jpg", "/tmp/review_25_29/shot_27.jpg"),
    ("https://media.fedu.vn/images/IG_%40AL%2C_The_Creator_Videography_Reels_DdTeHleIqkg_Video_by_shogentle/shot_01_mid.jpg", "/tmp/review_25_29/shot_28.jpg"),
    ("https://media.fedu.vn/images/IG_%40iman.lizi_Dc6qXoKoYKh/shot_01_mid.jpg", "/tmp/review_25_29/shot_29.jpg")
]

def dl(u, p):
    try:
        urllib.request.urlretrieve(u, p)
        return p
    except Exception as e:
        return f"{p} Error: {e}"

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(dl, u, p) for u, p in urls]
    for future in concurrent.futures.as_completed(futures):
        print(future.result())

os.system('ls -lh /tmp/review_25_29/')
