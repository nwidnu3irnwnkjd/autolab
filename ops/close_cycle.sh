#!/usr/bin/env bash
# Cierre de ciclo en un comando (T7). Dueño: Orquestador.
#   bash ops/close_cycle.sh <N> "<mensaje>" <5h%> <semanal%> <extraEUR> "<roles y tokens>" [--dry-run]
# Los % y el extra los da get_usage (MCP: no se puede llamar desde bash).
# Pasos: build + check + qa_static (rojo = salir SIN commit) -> páginas para el QA con navegador -> recuento de
# peticiones -> línea en journal/costes.md -> UN commit -> pull --rebase (+ repite 2-3 si trae live.json) -> push ->
# espera a que las páginas nuevas den 200 -> IndexNow -> resumen de 5 líneas para ESTADO.md (el script no lo escribe).
# --dry-run: ejecuta todo salvo commit, push, curl, IndexNow y la escritura en costes.md.
# Antes del build corre ops/gen_ejemplos.py (|| true): regenera projects/decidir/data/ejemplos.json con el calcular() real de las 9 insignia
# (osascript; en GitHub Actions no se ejecuta, el build solo lee el JSON). check.py lo verifica con --check.
# Variables opcionales: QA_PESO_BLOQ_KB (umbral bloqueante de peso por página, 75 por defecto).
set -euo pipefail

DRY=0; ARGS=()
for a in "$@"; do if [ "$a" = "--dry-run" ]; then DRY=1; else ARGS+=("$a"); fi; done
if [ "${#ARGS[@]}" -ne 6 ]; then
  echo 'Uso: bash ops/close_cycle.sh <N> "<mensaje>" <5h%> <semanal%> <extraEUR> "<roles y tokens>" [--dry-run]' >&2; exit 2
fi
N="${ARGS[0]}"; MSG="${ARGS[1]}"; H5="${ARGS[2]}"; SEM="${ARGS[3]}"; EXTRA="${ARGS[4]}"; ROLES="${ARGS[5]}"
case "$N" in ''|*[!0-9]*) echo "N debe ser un entero" >&2; exit 2;; esac

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"; cd "$ROOT"
SITE="https://entremuchos.com"
CH='!f(){ echo username=nwidnu3irnwnkjd; echo "password=$(cat ~/.config/autolab/github_token)"; }; f'
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
[ "$DRY" = 1 ] && echo ">>> DRY-RUN: no habrá commit, push, curl, IndexNow ni escritura en costes.md"

step() { echo; echo "== $* =="; }
red() { echo; echo "ROJO en '$1': cierre abortado SIN commit ni push." >&2; exit 1; }

# 2-3. build + check + QA estática
step "ejemplos resueltos (insignia; en local con osascript; el build solo lee data/ejemplos.json)"; python3 ops/gen_ejemplos.py >/dev/null || true
step "build"; (cd projects/decidir && python3 build.py) || red build
step "check"; python3 ops/check.py || red check
step "qa_static"; python3 ops/qa_static.py --changed | tee "$TMP/qa.txt" || red qa_static
step "qa_static --fiscal (T14 v3, informativo, no bloqueante)"; python3 ops/qa_static.py --fiscal --changed | tail -8 || true
NAVEG="$(grep '^PÁGINAS PARA EL QA' "$TMP/qa.txt" | sed 's/^[^:]*: //' || true)"
NAVISO="$(grep -c '^AVISO' "$TMP/qa.txt" || true)"
NPAG="$(find projects/decidir/dist -name index.html | wc -l | tr -d ' ')"

# 4. páginas para el QA con navegador
step "Páginas para el QA con navegador (solo navegador y cifras; lo estático ya está hecho)"
echo "${NAVEG:-/}"

# páginas NUEVAS (archivos nuevos de calcs/content -> directorios de dist con ese nombre)
NUEVAS="$( (git diff --name-only --diff-filter=A HEAD; git ls-files --others --exclude-standard) 2>/dev/null | python3 -c '
import os, sys
dist = "projects/decidir/dist"
dirs = {}
for r, ds, fs in os.walk(dist):
    if "index.html" in fs:
        p = "/" + os.path.relpath(r, dist).replace(os.sep, "/") + "/"
        dirs.setdefault(p.strip("/").split("/")[-1], []).append(p)
new = set()
for f in sys.stdin.read().split("\n"):
    if f.startswith("projects/decidir/calcs/") and f.endswith(".json") and not f.endswith(".test.json") \
       or f.startswith("projects/decidir/content/") and f.endswith(".html"):
        for p in dirs.get(os.path.basename(f).split(".")[0], []): new.add(p)
print(" ".join(sorted(new)))
')"
echo "Páginas nuevas: ${NUEVAS:-ninguna}"

# 5. recuento de peticiones abiertas
step "Peticiones abiertas (ops/requests.md)"
REQ_OUT="$(python3 - "$N" <<'PY'
import re, sys
n = int(sys.argv[1]); total = 0; old = 0
try: lines = open("ops/requests.md", encoding="utf-8").read().split("\n")
except FileNotFoundError: lines = []
for l in lines:
    if not re.match(r"\s*- \[ \]", l): continue
    total += 1
    m = re.search(r"abierta c(\d+)", l); o = re.search(r"\[([^\]]*->[^\]]*)\]", l)
    dueno = o.group(1).split("->")[-1].strip() if o else "?"
    if not m: print(f"  SIN Nº DE CICLO (cuenta como abierta > 1 ciclo): dueño {dueno}: {l.strip()[:110]}"); old += 1
    elif int(m.group(1)) < n - 1: print(f"  ABIERTA > 1 ciclo: dueño {dueno}: {l.strip()[:110]}"); old += 1
print(f"TOTAL {total} {old}")
PY
)"
echo "$REQ_OUT" | grep -v '^TOTAL' || true
read -r _ K KOLD <<<"$(echo "$REQ_OUT" | grep '^TOTAL')"
echo "Abiertas: $K (más de 1 ciclo: $KOLD)"

# 6. línea de costes.md
TS="$(date -u +%FT%RZ)"
LINE="$TS | $H5 | $SEM | $EXTRA | ciclo $N cierre: $ROLES; peticiones abiertas: $K; páginas: $NPAG"
step "journal/costes.md"
if [ "$DRY" = 1 ]; then echo "(dry-run) añadiría: $LINE"; else echo "$LINE" >> journal/costes.md; echo "añadida: $LINE"; fi

if [ "$DRY" = 1 ]; then
  step "RESUMEN (dry-run)"
  echo "1. Ciclo $N: (dry-run, sin commit) «$MSG»"
  echo "2. Páginas: $NPAG en dist; nuevas: ${NUEVAS:-ninguna}; para QA navegador: ${NAVEG:-/}"
  echo "3. Consumo: 5h $H5 % · semanal $SEM % · extra $EXTRA EUR"
  echo "4. Peticiones abiertas: $K (> 1 ciclo: $KOLD)"
  echo "5. QA estática: 0 BLOQUEANTE, $NAVISO AVISO; IndexNow: no ejecutado (dry-run)"
  exit 0
fi

# 7. UN commit, pull --rebase, push
step "commit"
git add -A
git commit -q -m "ciclo $N: $MSG

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
HASH="$(git rev-parse --short HEAD)"; echo "commit $HASH"

step "pull --rebase"
LIVE_BEFORE="$(git hash-object projects/decidir/data/live.json)"
git -c credential.helper="$CH" pull --rebase origin main
LIVE_AFTER="$(git hash-object projects/decidir/data/live.json)"
if [ "$LIVE_BEFORE" != "$LIVE_AFTER" ]; then
  echo "El pull trajo data/live.json nuevo: repito build + check + qa_static"
  (cd projects/decidir && python3 build.py) || red "build tras pull"
  python3 ops/check.py || red "check tras pull"
  python3 ops/qa_static.py | tail -3 || red "qa_static tras pull"
fi
step "push"
git -c credential.helper="$CH" push origin main
HASH="$(git rev-parse --short HEAD)"

# KPIs de tráfico (informativo, ~80 s por la URL Inspection API; una fila por hora)
(nohup python3 ops/inspect_all.py >/dev/null 2>&1 &)  # inspección de las 161 URL en segundo plano (1 vez/20 h)
step "KPIs (journal/kpis.md, informativo)"; python3 ops/kpis.py || true

# 8. esperar al deploy y IndexNow
(cd projects/decidir && python3 build.py >/dev/null)   # dist con el lastmod del commit empujado
step "Esperando al deploy (hasta 180 s)"
DEPLOY="no confirmado"
if [ -n "${NUEVAS:-}" ]; then
  pending="$NUEVAS"; t=0
  while [ -n "$pending" ] && [ "$t" -le 180 ]; do
    next=""
    for p in $pending; do
      code="$(curl -s -o /dev/null -w '%{http_code}' "$SITE$p" || echo 000)"
      if [ "$code" = 200 ]; then echo "  200 $p"; else next="$next $p"; fi
    done
    pending="$(echo $next)"
    [ -z "$pending" ] && break
    sleep 15; t=$((t+15))
  done
  if [ -z "$pending" ]; then DEPLOY="200 en ${NUEVAS}"; else DEPLOY="SIN 200 tras 180 s: $pending"; echo "AVISO: $DEPLOY"; fi
else
  t=0; LOCAL_SM="$(shasum projects/decidir/dist/sitemap.xml | cut -d' ' -f1)"
  while [ "$t" -le 180 ]; do
    live_sm="$(curl -s "$SITE/sitemap.xml" | shasum | cut -d' ' -f1 || true)"
    [ "$live_sm" = "$LOCAL_SM" ] && { DEPLOY="sitemap publicado = local"; break; }
    sleep 15; t=$((t+15))
  done
  [ "$DEPLOY" = "no confirmado" ] && echo "AVISO: el sitemap publicado no coincide con el local tras 180 s (lastmod o deploy en curso)" || echo "  $DEPLOY"
fi

step "IndexNow (su estado entra en el commit del ciclo siguiente)"
python3 ops/websub_ping.py >/dev/null 2>&1 || true
INDEXNOW="$(python3 ops/indexnow.py 2>&1 | tail -2 | tr '\n' ' ' || true)"
echo "$INDEXNOW"

# 9. resumen de 5 líneas
step "RESUMEN para ESTADO.md"
echo "1. Ciclo $N cerrado: commit $HASH «$MSG»"
echo "2. Páginas: $NPAG en dist; nuevas: ${NUEVAS:-ninguna}; deploy: $DEPLOY"
echo "3. Consumo: 5h $H5 % · semanal $SEM % · extra $EXTRA EUR ($TS)"
echo "4. Peticiones abiertas: $K (> 1 ciclo: $KOLD)"
echo "5. QA estática: 0 BLOQUEANTE, $NAVISO AVISO; IndexNow: ${INDEXNOW:-sin salida}"
