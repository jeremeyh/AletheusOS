#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_ROOT="${1:-$(pwd)}"
cd "$PROJECT_ROOT"

MARKER="reports/span/backups/genesis14_latest.txt"
if [[ ! -f "$MARKER" ]]; then
  echo "ERROR: No Genesis 14 backup marker exists."
  exit 1
fi

BACKUP="$(cat "$MARKER")"
if [[ ! -d "$BACKUP" ]]; then
  echo "ERROR: Backup directory does not exist: $BACKUP"
  exit 1
fi

restore_target() {
  local target="$1"
  rm -rf "$target"
  if [[ -e "$BACKUP/$target" ]]; then
    mkdir -p "$(dirname "$target")"
    cp -R "$BACKUP/$target" "$target"
  fi
}

restore_target "aletheus/span/api.py"
restore_target "aletheus/span/constitutional_context.py"
restore_target "aletheus/span/profiles.py"
restore_target "aletheus/span/reporter.py"
restore_target "aletheus/span/rules"
restore_target "aletheus/span/profiles"
restore_target "aletheus/span/docs"
restore_target "tests/span/test_genesis14.py"
restore_target "aletheus/span/__init__.py"

echo "Genesis 14 rollback completed from: $BACKUP"
