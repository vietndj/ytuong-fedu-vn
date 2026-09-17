import urllib.request
url = "https://media.fedu.vn/images/Hong_Kong_Urban_Transitions_-_%40withyuee/img_001_f338d92e.jpg"
try:
    req = urllib.request.Request(url, method='HEAD')
    with urllib.request.urlopen(req) as res:
        print("Status:", res.status)
except Exception as e:
    print("Error:", e)
