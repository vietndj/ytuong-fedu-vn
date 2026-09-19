import json

def main():
    try:
        with open('master_classifications.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print("Error reading master_classifications.json:", e)
        return

    try:
        with open('curation_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print("Error reading curation_config.json:", e)
        return

    excluded = set(config.get('excluded_ids', []))

    for vid_id, info in data.items():
        if isinstance(info, dict):
            creator = str(info.get('creator', '')).lower()
            if 'jade.got.curious' in creator or 'mridupawasharma' in creator:
                excluded.add(vid_id)

    config['excluded_ids'] = list(excluded)

    try:
        with open('curation_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        print("Updated curation_config.json")
    except Exception as e:
        print("Error writing curation_config.json:", e)

if __name__ == "__main__":
    main()
