import socketserver
from http.server import BaseHTTPRequestHandler


class HealthHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Ok'.encode('ascii'))


def run_health_server():
    with socketserver.TCPServer(('', 9091), HealthHTTPRequestHandler) as httpd:
        httpd.serve_forever()


if __name__ == "__main__":
    run_health_server()
