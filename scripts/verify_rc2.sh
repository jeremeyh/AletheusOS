#!/usr/bin/env bash
set -e

echo "================================================="
echo "CardHawk OS RC2 Verification"
echo "================================================="

echo
echo "[1] Git Status"
git status --short

echo
echo "[2] Python Cache"
find . -name "__pycache__"
find . -name "*.pyc"

echo
echo "[3] Swap Files"
find . -name "*.swp" -o -name "*.swo" -o -name "*.swx"

echo
echo "[4] Duplicate Services"
find services -maxdepth 1 -type f | sort

echo
echo "[5] Runtime Modules"
find . -name "runtime.py" | sort

echo
echo "[6] Event Bus"
find . -name "event_bus.py"

echo
echo "[7] Engine Registry"
find . -name "engine_registry.py"

echo
echo "[8] Provider Registry"
find . -name "provider_registry.py"

echo
echo "[9] Boot Modules"
find . -name "bootstrap.py"

echo
echo "================================================="
echo "Verification Complete"
echo "================================================="
