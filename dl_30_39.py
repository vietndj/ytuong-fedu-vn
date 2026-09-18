import urllib.request
import os
import concurrent.futures

os.makedirs('/tmp/review_30_39', exist_ok=True)
urls = [
    ("https://media.fedu.vn/images/IG_%40hayancook_DdSUI9BvhqR/shot_01_mid.jpg", "/tmp/review_30_39/shot_30.jpg"),
    ("https://media.fedu.vn/images/IG_%40cushygarden_DdL6pHDSKRc/shot_01_mid.jpg", "/tmp/review_30_39/shot_31.jpg"),
    ("https://media.fedu.vn/images/IG_%40dev_zero_Db-S8i1hXwF/shot_01_mid.jpg", "/tmp/review_30_39/shot_32.jpg"),
    ("https://media.fedu.vn/images/IG_%40nagisa.decor_Dco_DevvUla/shot_01_mid.jpg", "/tmp/review_30_39/shot_33.jpg"),
    ("https://media.fedu.vn/images/IG_%40yuto_creator_DdBlAWRO1Hl/shot_01_mid.jpg", "/tmp/review_30_39/shot_34.jpg"),
    ("https://media.fedu.vn/images/IG_%40beixin_DdRGd8evPK-/shot_01_mid.jpg", "/tmp/review_30_39/shot_35.jpg"),
    ("https://media.fedu.vn/images/IG_%40layton_video_DdKGq2TMhf4/shot_01_mid.jpg", "/tmp/review_30_39/shot_36.jpg"),
    ("https://media.fedu.vn/images/IG_%40kienobifilms_DdPLvUpBwCl/shot_01_mid.jpg", "/tmp/review_30_39/shot_37.jpg"),
    ("https://media.fedu.vn/images/IG_%40aki_japan_DaDFH_TSii8/shot_01_mid.jpg", "/tmp/review_30_39/shot_38.jpg"),
    ("https://media.fedu.vn/images/IG_%40nathanael.lct_DdRg_ybtlKI/shot_01_mid.jpg", "/tmp/review_30_39/shot_39.jpg")
]

import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def dl(u, p):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response, open(p, 'wb') as out_file:
            out_file.write(response.read())
        return p
    except Exception as e:
        return f"{p} Error: {e}"

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(dl, u, p) for u, p in urls]
    for future in concurrent.futures.as_completed(futures):
        print(future.result())

os.system('ls -lh /tmp/review_30_39/')
