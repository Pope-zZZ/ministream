from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CORSHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # 允许跨域
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def log_message(self, format, *args):
        print(f"[请求] {args[0]} {args[1]}")

# 切换到storage目录提供文件服务
os.chdir('D:/ministream/storage')
print("✅ 服务启动：http://localhost:8080")
print("📂 服务目录：D:/ministream/storage")

HTTPServer(('0.0.0.0', 8080), CORSHandler).serve_forever()