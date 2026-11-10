"""
Local HTTP Server untuk Aplikasi Web Kamera Infrared
Menjalankan server lokal pada port aman (default: 8080)
"""

import http.server
import socketserver
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"==================================================")
        print(f"  Server Kamera Infrared Aktif!")
        print(f"  Buka di Browser: http://localhost:{PORT}")
        print(f"==================================================")
        print("Tekan Ctrl+C untuk menghentikan server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer dihentikan.")

if __name__ == "__main__":
    run()
