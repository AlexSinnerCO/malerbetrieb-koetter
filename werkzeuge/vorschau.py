# -*- coding: utf-8 -*-
"""Lokale Vorschau der Website mit sauberen Adressen (/leistungen statt /leistungen.html).

Aufruf (im Projektordner):  python werkzeuge/vorschau.py   ->  http://localhost:8770
Das Kontaktformular (PHP) funktioniert hier nicht, nur auf dem echten Webspace.
"""
import http.server
import os
import socketserver

PORT = 8770
WEB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "website")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=WEB, **k)

    def send_head(self):
        pfad = self.path.split("?", 1)[0].split("#", 1)[0]
        if pfad != "/" and "." not in os.path.basename(pfad):
            if os.path.exists(os.path.join(WEB, pfad.lstrip("/") + ".html")):
                self.path = pfad + ".html"
        elif not os.path.exists(os.path.join(WEB, pfad.lstrip("/"))) and pfad != "/":
            self.path = "/404.html"
        return super().send_head()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as srv:
    print(f"Vorschau: http://localhost:{PORT}")
    srv.serve_forever()
