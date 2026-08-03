#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "AletheusOS Genesis 37.21 distribution package"
echo "Manifest: $ROOT/manifest.json"
echo "This source-first package requires the outer Genesis installer to hydrate it into AletheusOS."
