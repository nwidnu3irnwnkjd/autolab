#!/usr/bin/env python3
"""Avisa al hub WebSub (Google, sin cuenta) de que /feed.xml y /noticias/feed.xml cambiaron. Ejecutar tras el deploy, junto a indexnow.py.
Uso: python3 ops/websub_ping.py   (204 = aceptado)"""
import urllib.request, urllib.parse, urllib.error
HUB = "https://pubsubhubbub.appspot.com/"; FEEDS = ["https://entremuchos.com/feed.xml", "https://entremuchos.com/noticias/feed.xml"]  # general + noticias
data = urllib.parse.urlencode([("hub.mode", "publish")] + [("hub.url", f) for f in FEEDS]).encode()
try:
    with urllib.request.urlopen(urllib.request.Request(HUB, data=data, method="POST", headers={"User-Agent": "entremuchos-websub/1.0"}), timeout=20) as r: code = r.status
except urllib.error.HTTPError as e: code = e.code
except Exception as e: print("WebSub: sin respuesta:", e); raise SystemExit(0)
print(f"WebSub -> HTTP {code} ({'OK' if code in (200, 202, 204) else 'revisar'})")
