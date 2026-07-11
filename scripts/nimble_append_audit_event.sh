#!/usr/bin/env bash

set -euo pipefail

: "${NIMBLE_AUDIT_EVENT_TYPE:?Missing NIMBLE_AUDIT_EVENT_TYPE}"
: "${NIMBLE_ENVIRONMENT:?Missing NIMBLE_ENVIRONMENT}"
: "${NIMBLE_RELEASE:?Missing NIMBLE_RELEASE}"
: "${NIMBLE_REVISION:?Missing NIMBLE_REVISION}"

metadata="${NIMBLE_AUDIT_METADATA_JSON:-{}}"

python append_nimble_audit_event.py \
  --event-type "${NIMBLE_AUDIT_EVENT_TYPE}" \
  --environment "${NIMBLE_ENVIRONMENT}" \
  --release "${NIMBLE_RELEASE}" \
  --revision "${NIMBLE_REVISION}" \
  --metadata-json "${metadata}"
