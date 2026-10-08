"""lastmod estable (OPT3.2): data/lastmod.json = {clave: {"h": hash del contenido material, "d": fecha del último cambio}}.
La fecha solo cambia cuando cambia el hash; plantillas/CSS/ui.py/minify no entran en el hash.
Primera vez que se ve una clave: se conserva la fecha de partida (línea base, no se inventa)."""
import json, os, re, hashlib, datetime, subprocess
ROOT = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(ROOT, "data/lastmod.json")
TODAY = datetime.date.today().isoformat()
try: _S = json.load(open(PATH))
except Exception: _S = {}
_ORIG = json.dumps(_S, sort_keys=True)
_claimed = set()
_head = None

def head_date():
    """Fecha del último commit (tope de la línea base: lo sin commitear no cuenta como cambio de contenido)."""
    global _head
    if _head is None:
        try: _head = subprocess.run(["git", "log", "-1", "--format=%cs"], cwd=ROOT, capture_output=True, text=True, timeout=10).stdout.strip() or TODAY
        except Exception: _head = TODAY
    return _head

def _h(t): return hashlib.sha256(t.encode("utf-8")).hexdigest()[:16]

_DATES = re.compile(r"\d{4}-\d{2}-\d{2}|\d{1,2} de [a-záéíóú]+ de \d{4}|\d{1,2}/\d{1,2}/\d{4}")
def text_hash(html):
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", html)
    t = re.sub(r"<[^>]+>", " ", t)
    t = _DATES.sub("#", t)  # las fechas derivadas de este mismo sistema no cuentan (evita bucle); el cambio de cifras sí
    return _h(re.sub(r"\s+", " ", t).strip())

def get(key, material_hash, baseline, claim=True):
    e = _S.get(key)
    if e is None:
        _S[key] = {"h": material_hash, "d": min(baseline, head_date()) if baseline else TODAY}
    elif e["h"] != material_hash:
        _S[key] = {"h": material_hash, "d": TODAY}
    if claim: _claimed.add(key)
    return _S[key]["d"]

def material(*parts, root=ROOT):
    """Hash de textos/archivos: los str que existen como ruta relativa se leen; el resto cuenta como texto."""
    acc = []
    for p in parts:
        fp = os.path.join(root, p) if isinstance(p, str) and len(p) < 300 and "\n" not in p and os.path.isfile(os.path.join(root, p)) else None
        acc.append(open(fp, encoding="utf-8").read() if fp else str(p))
    return _h("\x00".join(acc))

def resolve(path, body, baseline):
    """Para write(): si la clave ya la fijó su dueño (calculadoras, guías) se respeta; si no, hash del texto visible del cuerpo."""
    if path in _claimed: return _S[path]["d"]
    return get(path, text_hash(body), baseline, claim=False)

def save():
    if json.dumps(_S, sort_keys=True) != _ORIG:
        open(PATH, "w").write(json.dumps(_S, sort_keys=True, indent=0, ensure_ascii=False) + "\n")
