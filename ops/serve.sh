#!/bin/bash
# Sirve dist/ de un proyecto en local. Uso: bash ops/serve.sh decidir
cd "$(dirname "$0")/../projects/$1/dist" && python3 -m http.server 8787
