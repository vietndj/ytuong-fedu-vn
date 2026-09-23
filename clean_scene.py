import re

with open("scene.html", "r") as f:
    content = f.read()

# We want to remove the specific dict containing "IG_@creator_video_Video_video"
# The dict spans from line 2694 "  {" to line 2717 "  },"
# We will construct a regex to match it safely.
pattern = re.compile(r'\s*\{\s*"id":\s*"IG_@creator_video_Video_video"[\s\S]*?\},', re.MULTILINE)

new_content, count = pattern.subn('', content)
if count > 0:
    with open("scene.html", "w") as f:
        f.write(new_content)
    print(f"Replaced {count} instances.")
else:
    print("Not found.")
