import json
import os
import subprocess
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

base_dir = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn'
dist_dir = os.path.join(base_dir, 'dist')

class AdminHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=dist_dir, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/train':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            video_id = data.get('video_id')
            new_style = data.get('new_style')
            new_industry = data.get('new_industry')
            reason = data.get('reason')
            
            master_file = os.path.join(base_dir, 'master_classifications.json')
            try:
                with open(master_file, 'r', encoding='utf-8') as f:
                    master_data = json.load(f)
                video_data = master_data.get(video_id, {})
                creator = video_data.get('creator', video_id)
                
                if not new_style:
                    st = video_data.get('shooting_style')
                    if isinstance(st, dict): new_style = st.get('name', 'Giữ nguyên')
                    else: new_style = st or 'Giữ nguyên'
                if not new_industry:
                    ind = video_data.get('industry')
                    if isinstance(ind, dict): new_industry = ind.get('name', 'Giữ nguyên')
                    else: new_industry = ind or 'Giữ nguyên'
                    
                style_map = {
                    'walk-and-talk': 'Walk & Talk', 'voice-over': 'Lồng Tiếng', 'talking-head': 'Nói Trực Diện', 
                    'storytelling': 'Kể Chuyện', 'dien-anh': 'Chỉn Chu', 'chuyen-canh': 'Chuyển Cảnh', 'theo-nhip-nhac': 'Theo nhịp nhạc'
                }
                ind_map = {
                    'spa-lam-dep': 'Làm đẹp', 'thuong-hieu': 'Xây kênh', 'thoi-trang': 'Thời trang', 'am-thuc': 'F&B',
                    'du-lich': 'Du lịch', 'cong-nghe': 'Đồ công nghệ', 'kien-truc': 'Góc nhà đẹp', 'the-thao': 'Thể thao',
                    'ky-thuat-quay': 'Bố cục', 'ugc': 'UGC & Ads', 'phat-trien-ban-than': 'Tâm Lý'
                }
                new_style = style_map.get(new_style, new_style)
                new_industry = ind_map.get(new_industry, new_industry)
            except:
                creator = video_id
                
            cli_cmd = f'python3 feedback_learner.py "SUA: {creator} -> {new_style}, {new_industry}, Lý do: {reason}"'
            
            try:
                print(f"\\n[ADMIN SERVER] Running AI Training: {cli_cmd}\\n")
                subprocess.run(cli_cmd, shell=True, check=True, cwd=base_dir)
                print("\\n[ADMIN SERVER] Rebuilding site & syncing to dist/...\\n")
                subprocess.run('python3 build_ideas_bank.py', shell=True, check=True, cwd=base_dir)
                subprocess.run('python3 training_data_builder.py', shell=True, check=True, cwd=base_dir)
                print("\\n[ADMIN SERVER] Pushing to Git...\\n")
                subprocess.run('git add . && git commit -m "auto: huấn luyện AI qua Admin UI" && git push origin main', shell=True, cwd=base_dir)
                
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
                print("\\n[ADMIN SERVER] DONE! Site updated and pushed.\\n")
            except Exception as e:
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

def run_server():
    port = 8765
    server_address = ('', port)
    httpd = HTTPServer(server_address, AdminHandler)
    print(f'\\n🚀 TRẠM QUẢN TRỊ ADMIN ĐÃ MỞ TẠI: http://localhost:{port}')
    print('Bất kỳ thay đổi nào trên web này sẽ tự động gọi AI, build và đẩy thẳng lên Cloudflare!\\n')
    httpd.serve_forever()

if __name__ == "__main__":
    # Tự động đồng bộ dist trước khi mở
    subprocess.run('python3 build_ideas_bank.py', shell=True, cwd=base_dir, stdout=subprocess.DEVNULL)
    subprocess.run('python3 training_data_builder.py', shell=True, cwd=base_dir, stdout=subprocess.DEVNULL)
    
    thread = threading.Thread(target=run_server)
    thread.daemon = True
    thread.start()
    
    # Mở Chrome tự động
    webbrowser.open('http://localhost:8765')
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\\nĐã đóng trạm quản trị.")
