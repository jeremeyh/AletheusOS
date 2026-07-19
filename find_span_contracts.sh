#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo " AletheusOS SPAN Contract Locator"
echo "=========================================================="

FILES=(
"aletheus/span/api.py"
"aletheus/span/reporter.py"
"aletheus/span/profiles.py"
"aletheus/span/rule_loader.py"
"aletheus/span/rule_registry.py"
"aletheus/span/rule_engine.py"
)

echo
echo "Canonical files"
for f in "${FILES[@]}"; do
    [[ -f "$f" ]] && echo "✓ $f" || echo "✗ $f"
done

echo
echo "SPAN Python files"
find . -type f -path "*/span/*.py" | sort

echo
echo "Genesis scripts"
find . \( -name install.sh -o -name validate.sh -o -name rollback.sh \) | sort
