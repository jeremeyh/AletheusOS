#!/usr/bin/env bash

set -euo pipefail

: "${NIMBLE_ENVIRONMENT:?Missing NIMBLE_ENVIRONMENT}"
: "${ROLLBACK_RELEASE:?Missing ROLLBACK_RELEASE}"
: "${ROLLBACK_REVISION:?Missing ROLLBACK_REVISION}"
: "${ROLLBACK_IMAGE:?Missing ROLLBACK_IMAGE}"

exec python scripts/nimble_provider_dispatch.py \
  --action rollback \
  --environment "${NIMBLE_ENVIRONMENT}"
