#!/usr/bin/env bash

set -euo pipefail

required_variables=(
  NIMBLE_PROVIDER_ACTION
  NIMBLE_ENVIRONMENT
)

for variable in "${required_variables[@]}"; do
  if [[ -z "${!variable:-}" ]]; then
    echo "FAIL: missing provider variable: ${variable}" >&2
    exit 1
  fi
done

case "${NIMBLE_PROVIDER_ACTION}" in
  deploy)
    required_deploy_variables=(
      NIMBLE_RELEASE
      NIMBLE_REVISION
      NIMBLE_IMAGE
    )

    for variable in "${required_deploy_variables[@]}"; do
      if [[ -z "${!variable:-}" ]]; then
        echo "FAIL: missing deploy variable: ${variable}" >&2
        exit 1
      fi
    done

    echo "Nimble registered provider dry run"
    echo "Action: deploy"
    echo "Environment: ${NIMBLE_ENVIRONMENT}"
    echo "Release: ${NIMBLE_RELEASE}"
    echo "Revision: ${NIMBLE_REVISION}"
    echo "Image: ${NIMBLE_IMAGE}"
    ;;

  rollback)
    required_rollback_variables=(
      ROLLBACK_RELEASE
      ROLLBACK_REVISION
      ROLLBACK_IMAGE
    )

    for variable in "${required_rollback_variables[@]}"; do
      if [[ -z "${!variable:-}" ]]; then
        echo "FAIL: missing rollback variable: ${variable}" >&2
        exit 1
      fi
    done

    echo "Nimble registered provider dry run"
    echo "Action: rollback"
    echo "Environment: ${NIMBLE_ENVIRONMENT}"
    echo "Release: ${ROLLBACK_RELEASE}"
    echo "Revision: ${ROLLBACK_REVISION}"
    echo "Image: ${ROLLBACK_IMAGE}"
    ;;

  *)
    echo \
      "FAIL: unsupported provider action: " \
      "${NIMBLE_PROVIDER_ACTION}" \
      >&2
    exit 1
    ;;
esac
