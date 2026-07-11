#!/usr/bin/env bash

set -euo pipefail

: "${NIMBLE_ENVIRONMENT:?Missing NIMBLE_ENVIRONMENT}"
: "${NIMBLE_RELEASE:?Missing NIMBLE_RELEASE}"
: "${NIMBLE_REVISION:?Missing NIMBLE_REVISION}"
: "${NIMBLE_IMAGE:?Missing NIMBLE_IMAGE}"

exec python scripts/nimble_provider_dispatch.py \
  --action deploy \
  --environment "${NIMBLE_ENVIRONMENT}"
