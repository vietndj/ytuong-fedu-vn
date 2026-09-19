import json

def main():
    try:
        with open('master_classifications.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print("Error reading master_classifications.json:", e)
        return

    jade_ids = []
    mridu_ids = []

    for vid_id, info in data.items():
        if isinstance(info, dict):
            creator = str(info.get('creator', '')).lower()
            if 'jade.got.curious' in creator:
                jade_ids.append(vid_id)
            elif 'mridupawasharma' in creator:
                mridu_ids.append(vid_id)

    print("Jade IDs:", len(jade_ids))
    print(jade_ids)
    print("Mridu IDs:", len(mridu_ids))
    print(mridu_ids)

if __name__ == "__main__":
    main()
