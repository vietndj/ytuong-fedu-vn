import json
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        base_dir = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn'
        learned_file = os.path.join(base_dir, 'LEARNED_PATTERNS.json')
        
        if self.path == '/api/stats':
            try:
                with open(learned_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.wfile.write(json.dumps(data.get('stats', {})).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        elif self.path == '/api/corrections':
            try:
                with open(learned_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.wfile.write(json.dumps(data.get('learning_history_logs', [])).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))

    def do_POST(self):
        if self.path == '/api/train':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            video_id = data.get('video_id')
            new_style = data.get('new_style')
            new_industry = data.get('new_industry')
            reason = data.get('reason')
            
            
            # Since the CLI requires @creator, we need to find it
            base_dir = '/Users/vietmac/Documents/CODE/ytuong-fedu-vn'
            master_file = os.path.join(base_dir, 'master_classifications.json')
            try:
                with open(master_file, 'r', encoding='utf-8') as f:
                    master_data = json.load(f)
                video_data = master_data.get(video_id, {})
                creator = video_data.get('creator', video_id)
                
                # If new_style/new_industry are empty, keep the original
                if not new_style:
                    st = video_data.get('shooting_style')
                    if isinstance(st, dict): new_style = st.get('name', 'Giữ nguyên')
                    else: new_style = st or 'Giữ nguyên'
                if not new_industry:
                    ind = video_data.get('industry')
                    if isinstance(ind, dict): new_industry = ind.get('name', 'Giữ nguyên')
                    else: new_industry = ind or 'Giữ nguyên'
                    
                # Convert ID to Name for CLI if needed, but CLI is smart enough.
                # Actually, mapping ID to Name is safer.
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
                subprocess.run(cli_cmd, shell=True, check=True, cwd=base_dir)
                subprocess.run('python3 training_data_builder.py', shell=True, check=True, cwd=base_dir)
                
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Private-Network', 'true')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8765):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
