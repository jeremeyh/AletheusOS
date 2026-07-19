#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

echo "== Python compilation =="
python -m py_compile tools/repository/*.py

echo
echo "== Repository hardening dry run =="
python tools/repository/harden.py

echo
echo "== Repository Doctor =="
python tools/repository/doctor.py

echo
echo "== Repository Steward dry run =="
python tools/repository/steward.py

echo
echo "== Git status =="
git status --short
