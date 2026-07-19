#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

if [[ ! -d "${ROOT}/aletheus/strategic" ]]; then
  echo "ERROR: ${ROOT}/aletheus/strategic does not exist."
  echo "Install and validate Genesis Drop 012A first."
  exit 1
fi

mkdir -p "${ROOT}/aletheus/strategic/runtime"
mkdir -p "${ROOT}/tests/strategic/runtime"
mkdir -p "${ROOT}/docs/strategic"

BUNDLE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

copy_file() {
  local rel="$1"
  mkdir -p "$(dirname "${ROOT}/${rel}")"
  cp "${BUNDLE_DIR}/files/${rel}" "${ROOT}/${rel}"
}

copy_file "aletheus/strategic/runtime/__init__.py"
copy_file "aletheus/strategic/runtime/contracts.py"
copy_file "aletheus/strategic/runtime/models.py"
copy_file "aletheus/strategic/runtime/service.py"
copy_file "aletheus/strategic/runtime/bootstrap.py"
copy_file "tests/strategic/runtime/test_runtime_service.py"
copy_file "tests/strategic/runtime/test_runtime_bootstrap.py"
copy_file "docs/strategic/span_runtime_integration.md"

echo
echo "Genesis Drop 012B installed."
echo
echo "Validate with:"
echo "  PYTHONPATH=. python -m pytest tests/strategic/runtime -q"
echo "  python -m compileall aletheus/strategic/runtime"
