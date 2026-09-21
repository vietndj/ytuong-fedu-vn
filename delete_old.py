import subprocess

def run_cmd(cmd, capture=False):
    if capture:
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.stdout.strip()
    else:
        subprocess.run(cmd, check=True)

print("Listing root mp4 files in videos/...")
ls_out = run_cmd(["rclone", "lsf", "r2:vietndjmedia/videos"], capture=True)
files = [f for f in ls_out.split('\n') if f.endswith('.mp4') and '/' not in f]

print(f"Found {len(files)} files to delete.")
with open("files_to_delete.txt", "w") as f:
    for filename in files:
        f.write(filename + "\n")

if len(files) > 0:
    print("Deleting from R2...")
    run_cmd(["rclone", "delete", "--files-from", "files_to_delete.txt", "r2:vietndjmedia/videos"])
    print("Done!")
else:
    print("No files to delete.")
