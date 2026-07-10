#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(
  cd "$(dirname "${BASH_SOURCE[0]}")"
  pwd
)"

cd "$ROOT_DIR"

if [[ -f ".venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
fi

export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"

if [[ -s "$NVM_DIR/nvm.sh" ]]; then
  # shellcheck disable=SC1090
  source "$NVM_DIR/nvm.sh"
fi

if command -v nvm >/dev/null 2>&1; then
  nvm use 24 >/dev/null
fi

if ! command -v node >/dev/null 2>&1; then
  echo "FAIL: Node.js is not available on PATH."
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "FAIL: npm is not available on PATH."
  exit 1
fi

export NODE_OPTIONS="${NODE_OPTIONS:---use-system-ca}"
export CI="${CI:-1}"

python validate_nimble_production.py
