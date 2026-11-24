"""5주 실습용 아주 작은 HTTP 앱. 표준 라이브러리만 써요 (설치할 것 없음).

실행:  python3 app.py            (기본 포트 8000)
       PORT=8080 python3 app.py  (포트를 환경 변수로 바꾸기)
"""
import json
import os
import signal
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", "8000"))
GREETING = os.environ.get("GREETING", "안녕하세요")
STARTED = time.time()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = {"status": "ok", "uptime_seconds": int(time.time() - STARTED)}
        elif self.path == "/":
            body = {"message": f"{GREETING}, 리눅스!", "pid": os.getpid()}
        else:
            self.send_error(404, "Not Found")
            return
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        # 기본은 stderr 에 쓰는데, 서비스로 돌리면 journalctl 에서 보이도록 stdout 으로 보내요.
        print(f"{self.address_string()} {fmt % args}", flush=True)


def stop(signum, frame):
    # SIGTERM(15) 이나 Ctrl+C(SIGINT, 2) 를 받으면 깔끔하게 끝내요.
    print(f"신호 {signum} 를 받았어요. 정리하고 끝냅니다.", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"http://127.0.0.1:{PORT} 에서 기다리는 중 (pid={os.getpid()})", flush=True)
    server.serve_forever()
