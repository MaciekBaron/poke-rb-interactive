from pkmn.config import PORTS
import http.server
import socketserver
import threading

PORT = int(PORTS.get('HTTPPort') or 8888)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="web", **kwargs)

    def log_request(self, arg):
        # Don't log
        pass

def _start():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Web layer ready, serving on port {PORT}")
        httpd.serve_forever()

def start_web_interface():
    web_thread = threading.Thread(target=_start)
    web_thread.start()
