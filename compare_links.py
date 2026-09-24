import json
import sys

# The 35 links provided by the user
user_links = """
https://www.instagram.com/p/DLakrprhSVh/
https://www.instagram.com/p/DKP4OCBOXQd/
https://www.instagram.com/p/DKaoC1hubgG/
https://www.instagram.com/p/DLAaGcyOjOL/
https://www.instagram.com/p/DLX_lN1ONpU/
https://www.instagram.com/p/DLfo2SLuQuH/
https://www.instagram.com/p/DLyV_yAOmZH/
https://www.instagram.com/p/DMBn77kOmBx/
https://www.instagram.com/p/DMnnDfDulMJ/
https://www.instagram.com/p/DNZaV0HOLAG/
https://www.instagram.com/p/DOuRCZ6DiHe/
https://www.instagram.com/p/DLspS29Onhu/
https://www.instagram.com/p/DOVse1YjaHj/
https://www.instagram.com/p/DIbUxabzEB8/
https://www.instagram.com/p/DK2WSvnie5C/
https://www.instagram.com/p/DOTeeFyjLT3/
https://www.instagram.com/p/DMil8s4RwGv/
https://www.instagram.com/p/DIWWgiQxzJK/
https://www.instagram.com/p/DOGyKFujIhh/
https://www.instagram.com/p/DAkGVqExyfO/
https://www.instagram.com/p/DKll7VoJfNV/
https://www.instagram.com/p/DNTBMUbutnF/
https://www.instagram.com/p/DK8_vmMMdj_/
https://www.instagram.com/p/DOTKFoTiAhd/
https://www.instagram.com/p/DI_or3asYE-/
https://www.instagram.com/p/DHMd4jehYmv/
https://www.instagram.com/p/DIW_Lczsdlv/
https://www.instagram.com/p/DHMj9Y1MG0x/
https://www.instagram.com/p/DJJqppogUiZ/
https://www.instagram.com/p/DKZkBSrpe8G/
https://www.instagram.com/p/DI4KtJ_KGLL/
https://www.instagram.com/p/DJHsPsoBOzd/
https://www.instagram.com/p/DLH6C27vyFn/
https://www.instagram.com/p/DLhLH26z0H_/
https://www.instagram.com/p/DJSeYXRBYBA/
""".strip().split('\n')

# Read master classifications
try:
    with open('master_classifications.json', 'r', encoding='utf-8') as f:
        master = json.load(f)
except Exception as e:
    print(f"Error reading DB: {e}")
    sys.exit(1)

# Get all existing IDs in DB
existing_ids_in_db = set(master.keys())

missing_links = []
for link in user_links:
    link = link.strip()
    if not link: continue
    
    # Extract shortcode
    # Example: https://www.instagram.com/p/DLakrprhSVh/ -> DLakrprhSVh
    parts = link.split('/')
    # The shortcode is usually the one after /p/ or /reel/
    shortcode = ""
    if '/p/' in link:
        shortcode = link.split('/p/')[1].split('/')[0]
    elif '/reel/' in link:
        shortcode = link.split('/reel/')[1].split('/')[0]
        
    if shortcode:
        # Check if shortcode is substring of any key in DB
        found = False
        for db_id in existing_ids_in_db:
            if shortcode in db_id:
                found = True
                break
        
        if not found:
            missing_links.append((link, shortcode))

print("### KẾT QUẢ ĐỐI SOÁT")
print(f"- Tổng số link bạn gửi: {len(user_links)}")
print(f"- Số link CHƯA CÓ trong Kho Ý Tưởng (master_classifications.json): {len(missing_links)}\n")

if missing_links:
    print("| STT | Link Instagram Chưa Có | ID (Shortcode) |")
    print("|---|---|---|")
    for i, (link, code) in enumerate(missing_links, 1):
        print(f"| {i} | [{link}]({link}) | `{code}` |")
else:
    print("Tất cả các link bạn gửi đều đã có trong kho dữ liệu.")
