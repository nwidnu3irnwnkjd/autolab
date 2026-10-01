"""Carga de calculadoras (dueño: Constructor). Soporta "default_from": "params.clave.con.puntos" en inputs."""
import json, os
import ui

def _dig(params, path):
    v = params
    for k in path.split("."):
        v = v[k]
    return v

def load_calcs(root, params):
    calcs = []
    cdir = os.path.join(root, "calcs")
    for f in sorted(os.listdir(cdir)):
        if f.endswith(".json") and not f.endswith(".test.json"):
            c = json.load(open(os.path.join(cdir, f)))
            c["js"] = open(os.path.join(cdir, c["slug"] + ".js")).read()
            c["content"] = open(os.path.join(root, "content", c["slug"] + ".html")).read()
            c.setdefault("tema", ui.tema(c))
            for i in c["inputs"]:
                ref = i.get("default_from")
                if ref:
                    i["default"] = _dig(params, ref[len("params."):] if ref.startswith("params.") else ref)
            calcs.append(c)
    return calcs
