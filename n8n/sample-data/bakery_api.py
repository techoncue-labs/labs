#!/usr/bin/env python3
"""Made-up "Sunny Bakery" orders API for trying n8n (all data invented).

Serves orders.json at http://<this machine>:8000/orders
Usage: python3 bakery_api.py            (or PORT=8080 python3 bakery_api.py)
Stop with Ctrl+C.
"""
import http.server
import os
import pathlib

DATA = pathlib.Path(__file__).with_name("orders.json").read_bytes()
PORT = int(os.environ.get("PORT", "8000"))


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.rstrip("/") in ("/orders", "/api/orders"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(DATA)
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    print(f"Bakery API on http://0.0.0.0:{PORT}/orders  (Ctrl+C to stop)")
    http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
