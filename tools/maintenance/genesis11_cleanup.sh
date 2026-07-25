#!/usr/bin/env bash
set -Eeuo pipefail

echo "========================================"
echo "Genesis 11 Cleanup Pipeline"
echo "========================================"

echo
echo "[1/5] Safe Ruff auto-fixes..."
ruff check . --fix

echo
echo "[2/5] Import sorting..."
ruff check . --select I --fix

echo
echo "[3/5] Compiling repository..."
python -m compileall .

echo
echo "[4/5] Running full test suite..."
pytest

echo
echo "[5/5] Ruff statistics..."
ruff check . --statistics || true

echo
echo "========================================"
echo "Cleanup complete."
echo "========================================"
