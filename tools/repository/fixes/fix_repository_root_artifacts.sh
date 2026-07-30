#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

BACKUP_DIR=".repository_backups/root_cleanup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "======================================"
echo " AletheusOS Repository Root Cleanup"
echo "======================================"
echo

backup_if_exists() {
    local f="$1"
    if [[ -f "$f" ]]; then
        cp "$f" "$BACKUP_DIR/"
        echo "Backed up: $f"
    fi
}

###############################################
# Replace temporary debug conftest.py
###############################################

if [[ -f conftest.py ]]; then
    backup_if_exists conftest.py

    cat > conftest.py <<'PY'
"""
Repository-wide pytest configuration.

This file intentionally exists at the repository root because pytest
discovers it automatically. It provides a canonical location for future
fixtures, hooks, markers, and repository-wide pytest configuration.

The previous temporary import-debug helper has been retired.
"""

# Intentionally minimal.
PY

    echo "Replaced repository conftest.py"
fi

###############################################
# Remove accidental scratch files
###############################################

for f in file.py test_file.py; do
    if [[ -f "$f" ]]; then
        CONTENT="$(tr -d '[:space:]' < "$f")"

        if [[ "$CONTENT" == "..." ]]; then
            backup_if_exists "$f"
            rm "$f"
            echo "Removed scratch file: $f"
        else
            echo "Keeping $f (contains real content)"
        fi
    fi
done

###############################################
# Summary
###############################################

echo
echo "======================================"
echo "Protected files intentionally preserved:"
echo "  - card_hawk_console.py"
echo "  - history.py"
echo "  - Root Nimble launcher scripts"
echo "======================================"
echo

if [[ -x ./tools/aletheus ]]; then
    echo "Running Repository Doctor..."
    ./tools/aletheus doctor
else
    echo "tools/aletheus not found."
fi

echo
echo "Cleanup complete."
echo "Backups stored in:"
echo "  $BACKUP_DIR"
