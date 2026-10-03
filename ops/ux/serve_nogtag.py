#!/usr/bin/env python3
"""Sirve projects/decidir/dist sin GA4/AdSense (auditorías UX sin ensuciar GA4).
Uso: [UX_ROOT=copia_de_dist] python3 ops/ux/serve_nogtag.py [puerto]  (por defecto 8791, solo 127.0.0.1)"""
import http.server, os, re, sys
ROOT = os.environ.get("UX_ROOT") or os.path.join(os.path.dirname(__file__), "..", "..", "projects", "decidir", "dist")
PAT = re.compile(rb'<script[^>]*(googletagmanager|pagead2|plausible)[^>]*></script>(<script>window\.dataLayer.*?</script>)?', re.S)
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s, *a, **k): super().__init__(*a, directory=os.path.abspath(ROOT), **k)
    def log_message(s, *a): pass
    def send_head(s):
        p = s.translate_path(s.path)
        if os.path.isdir(p): p = os.path.join(p, "index.html")
        if not p.endswith(".html") or not os.path.isfile(p): return super().send_head()
        b = PAT.sub(b"", open(p, "rb").read())
        s.send_response(200); s.send_header("Content-Type", "text/html; charset=utf-8")
        s.send_header("Content-Length", str(len(b))); s.end_headers()
        import io; return io.BytesIO(b)
http.server.ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1]) if len(sys.argv) > 1 else 8791), H).serve_forever()
