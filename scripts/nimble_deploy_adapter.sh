#!/usr/bin/env bash

set -euo pipefail

required_variables=(
  NIMBLE_DEPLOY_MODE
  NIMBLE_ENVIRONMENT
  NIMBLE_RELEASE
  NIMBLE_REVISION
  NIMBLE_IMAGE
)

for variable in "${required_variables[@]}"; do
  if [[ -z "${!variable:-}" ]]; then
    echo "FAIL: missing required variable: ${variable}" >&2
    exit 1
  fi
done

case "${NIMBLE_DEPLOY_MODE}" in
  dry-run)
    echo "Nimble deployment dry run"
    echo "Environment: ${NIMBLE_ENVIRONMENT}"
    echo "Release: ${NIMBLE_RELEASE}"
    echo "Revision: ${NIMBLE_REVISION}"
    echo "Image: ${NIMBLE_IMAGE}"
    ;;

  execute)
    if [[ -z "${NIMBLE_DEPLOY_COMMAND:-}" ]]; then
      echo \
        "FAIL: execute mode requires NIMBLE_DEPLOY_COMMAND." \
        >&2
      exit 1
    fi

    echo "Executing governed deployment adapter."
    echo "Environment: ${NIMBLE_ENVIRONMENT}"
    echo "Release: ${NIMBLE_RELEASE}"
    echo "Revision: ${NIMBLE_REVISION}"
    echo "Image: ${NIMBLE_IMAGE}"

    exec bash -euo pipefail -c "${NIMBLE_DEPLOY_COMMAND}"
    ;;

  *)
    echo \
      "FAIL: unsupported NIMBLE_DEPLOY_MODE: " \
      "${NIMBLE_DEPLOY_MODE}" \
      >&2
    exit 1
    ;;
esac
