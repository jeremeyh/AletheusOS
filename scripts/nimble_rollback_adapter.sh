#!/usr/bin/env bash

set -euo pipefail

required_variables=(
  NIMBLE_DEPLOY_MODE
  NIMBLE_ENVIRONMENT
  ROLLBACK_RELEASE
  ROLLBACK_REVISION
  ROLLBACK_IMAGE
)

for variable in "${required_variables[@]}"; do
  if [[ -z "${!variable:-}" ]]; then
    echo "FAIL: missing required variable: ${variable}" >&2
    exit 1
  fi
done

case "${NIMBLE_DEPLOY_MODE}" in
  dry-run)
    echo "Nimble rollback dry run"
    echo "Environment: ${NIMBLE_ENVIRONMENT}"
    echo "Release: ${ROLLBACK_RELEASE}"
    echo "Revision: ${ROLLBACK_REVISION}"
    echo "Image: ${ROLLBACK_IMAGE}"
    ;;

  execute)
    if [[ -z "${NIMBLE_ROLLBACK_COMMAND:-}" ]]; then
      echo \
        "FAIL: execute mode requires " \
        "NIMBLE_ROLLBACK_COMMAND." \
        >&2
      exit 1
    fi

    echo "Executing governed rollback adapter."

    exec bash -euo pipefail -c \
      "${NIMBLE_ROLLBACK_COMMAND}"
    ;;

  *)
    echo \
      "FAIL: unsupported NIMBLE_DEPLOY_MODE: " \
      "${NIMBLE_DEPLOY_MODE}" \
      >&2
    exit 1
    ;;
esac
