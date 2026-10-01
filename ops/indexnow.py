#!/usr/bin/env python3
"""Envía a IndexNow (Bing, Yandex, Seznam, Naver... comparten los envíos) las URLs nuevas o cambiadas del sitemap.
Solo stdlib. Ejecutar DESPUÉS de que el deploy esté publicado (la clave tiene que ser accesible en la raíz).

Uso:
  python3 ops/indexnow.py            # URLs con lastmod nuevo/cambiado desde el último envío (recomendado en cada ciclo)
  python3 ops/indexnow.py --all      # todas las URLs del sitemap (primer envío)
  python3 ops/indexnow.py --dry-run  # muestra qué enviaría, sin enviar
Opciones: --project decidir (por defecto) · --local (lee dist/sitemap.xml en vez del sitemap publicado)
Estado: ops/.indexnow-state.json guarda el lastmod enviado de cada URL.
"""
import glob, json, os, re, sys, urllib.request, urllib.error

OPS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(OPS)
ENDPOINT = "https://api.indexnow.org/indexnow"
STATE = os.path.join(OPS, ".indexnow-state.json")
UA = {"User-Agent": "entremuchos-indexnow/1.0"}

def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20) as r:
        return r.status, r.read().decode("utf-8", "replace")

def main():
    proj = arg("--project", "decidir"); pdir = os.path.join(ROOT, "projects", proj)
    base = json.load(open(os.path.join(pdir, "data/site.json")))["base_url"].rstrip("/")
    host = base.split("//")[1].split("/")[0]
    keys = [os.path.basename(f)[:-4] for f in glob.glob(os.path.join(pdir, "static", "*.txt"))
            if re.fullmatch(r"[a-f0-9]{32}", os.path.basename(f)[:-4])]
    if len(keys) != 1: sys.exit(f"Esperaba 1 clave IndexNow en projects/{proj}/static/, encontradas: {keys}")
    key = keys[0]; key_url = f"{base}/{key}.txt"

    if "--local" in sys.argv: sm = open(os.path.join(pdir, "dist/sitemap.xml")).read()
    else: sm = get(base + "/sitemap.xml")[1]
    entries = re.findall(r"<loc>(.*?)</loc>\s*<lastmod>(.*?)</lastmod>", sm)
    entries = [(u, d) for u, d in entries if u.split("//")[1].split("/")[0] == host]  # solo nuestro dominio

    state = json.load(open(STATE)) if os.path.exists(STATE) else {}
    todo = entries if "--all" in sys.argv else [(u, d) for u, d in entries if state.get(u) != d]
    print(f"{len(entries)} URLs en el sitemap; {len(todo)} para enviar.")
    for u, d in todo: print(f"  {d}  {u}")
    if not todo or "--dry-run" in sys.argv: return

    try:
        st, body = get(key_url)
        if st != 200 or body.strip() != key: sys.exit(f"La clave no está publicada correctamente en {key_url} (estado {st}). ¿Desplegado?")
    except urllib.error.URLError as e:
        sys.exit(f"No se puede leer {key_url}: {e}. Ejecuta tras el deploy.")

    payload = json.dumps({"host": host, "key": key, "keyLocation": key_url, "urlList": [u for u, _ in todo][:10000]}).encode()
    req = urllib.request.Request(ENDPOINT, data=payload, method="POST",
                                 headers=dict(UA, **{"Content-Type": "application/json; charset=utf-8"}))
    try:
        with urllib.request.urlopen(req, timeout=30) as r: code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
    meaning = {200: "OK", 202: "aceptado (validando clave)", 400: "petición mal formada", 403: "clave no válida",
               422: "URLs no coinciden con host/clave", 429: "demasiadas peticiones"}.get(code, "?")
    print(f"IndexNow → HTTP {code}: {meaning}")
    if code in (200, 202):
        state.update(dict(todo)); json.dump(state, open(STATE, "w"), indent=1, sort_keys=True)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
