#!/usr/bin/env python3
"""Read-only runtime health and telemetry contract foundation for AletheusOS.

This module defines constitutional data contracts and structured receipts only.
It performs no live probing, network transport, subsystem execution, storage
mutation, generalized command execution, or autonomous action.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

FOUNDATION_SCHEMA = "aletheus.runtime-health-telemetry-contract-foundation.v1"
HEALTH_RECEIPT_SCHEMA = "aletheus.runtime-health-receipt.v1"
TELEMETRY_RECEIPT_SCHEMA = "aletheus.runtime-telemetry-receipt.v1"
RECEIPT_SCHEMA_VERSION = "1.0.0"
CONTRACT_VERSION = "1.0.0"
EFFECT = "READ_ONLY"

HEALTH_STATES = ("HEALTHY", "DEGRADED", "UNAVAILABLE", "UNKNOWN")
F4H_ACTIVITY_STATES = ("idle", "focused", "engaged")
F4H_PROJECTED_STATES = ("idle", "focused", "engaged", "degraded")

SERVICE_REGISTRY = {
    "Platform Services": {
        "adapter_id": "platform-services.runtime-observation.v1",
        "contracts": {
            "health": "platform-services.health.v1",
            "telemetry": "platform-services.telemetry.v1",
        },
    },
    "A3ye": {
        "adapter_id": "a3ye.runtime-observation.v1",
        "contracts": {
            "health": "a3ye.health.v1",
            "telemetry": "a3ye.telemetry.v1",
        },
    },
    "Mammoth": {
        "adapter_id": "mammoth.runtime-observation.v1",
        "contracts": {
            "health": "mammoth.health.v1",
            "telemetry": "mammoth.telemetry.v1",
        },
    },
}


def _git(repo: Path, *args: str) -> str:
    run = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if run.returncode != 0:
        raise RuntimeError(run.stderr.strip() or "git command failed")
    return run.stdout.strip()


def resolve_exact_commit(repo: Path, commit: str) -> str:
    candidate = commit.strip()
    if len(candidate) != 40 or any(ch not in "0123456789abcdefABCDEF" for ch in candidate):
        raise ValueError("baseline commit must be an exact 40-character hexadecimal commit id")
    resolved = _git(repo, "rev-parse", "--verify", f"{candidate}^{{commit}}")
    if resolved.lower() != candidate.lower():
        raise ValueError("baseline commit did not resolve to the exact supplied commit id")
    return resolved.lower()


def _valid_observed_at(value: str) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    text = value.strip()
    try:
        parsed = datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _refusal(
    *,
    receipt_schema: str,
    service: str,
    capability: str,
    contract_id: str | None,
    adapter_id: str | None,
    observed_at: str | None,
    observation_source: str | None,
    health_state: str = "UNKNOWN",
    telemetry_payload_schema: str | None = None,
    failure_reason: str,
) -> dict[str, Any]:
    return {
        "receipt_schema": receipt_schema,
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "status": "REFUSED",
        "service": service,
        "capability": capability,
        "effect": EFFECT,
        "contract_id": contract_id,
        "contract_version": CONTRACT_VERSION,
        "adapter_id": adapter_id,
        "observed_at": observed_at,
        "observation_source": observation_source,
        "health_state": "UNKNOWN",
        "telemetry_payload_schema": telemetry_payload_schema,
        "telemetry_payload": None,
        "failure_reason": failure_reason,
        "f4g_required": True,
        "direct_execution_performed": False,
        "network_transport_performed": False,
        "mutation_performed": False,
    }


def resolve_contract(service: str, capability: str) -> dict[str, Any]:
    if service not in SERVICE_REGISTRY:
        return {
            "status": "REFUSED",
            "service": service,
            "capability": capability,
            "failure_reason": "UNKNOWN_SERVICE",
            "f4g_required": True,
            "direct_execution_performed": False,
        }
    if capability not in ("health", "telemetry"):
        return {
            "status": "REFUSED",
            "service": service,
            "capability": capability,
            "failure_reason": "UNKNOWN_CAPABILITY",
            "f4g_required": True,
            "direct_execution_performed": False,
        }
    record = SERVICE_REGISTRY[service]
    return {
        "status": "RESOLVED",
        "service": service,
        "capability": capability,
        "effect": EFFECT,
        "contract_id": record["contracts"][capability],
        "contract_version": CONTRACT_VERSION,
        "adapter_id": record["adapter_id"],
        "f4g_required": True,
        "allow_is_not_direct_execution": True,
        "direct_execution_performed": False,
    }


def _validate_binding(
    service: str,
    capability: str,
    contract_id: str,
    adapter_id: str,
) -> tuple[dict[str, Any] | None, str | None]:
    resolution = resolve_contract(service, capability)
    if resolution["status"] != "RESOLVED":
        return None, resolution["failure_reason"]
    if contract_id != resolution["contract_id"]:
        return None, "UNKNOWN_OR_MISMATCHED_CONTRACT"
    if adapter_id != resolution["adapter_id"]:
        return None, "UNKNOWN_OR_MISMATCHED_ADAPTER"
    return resolution, None


def build_health_receipt(
    *,
    service: str,
    contract_id: str,
    adapter_id: str,
    observed_at: str,
    observation_source: str,
    health_state: str,
    failure_reason: str | None = None,
) -> dict[str, Any]:
    resolution, binding_error = _validate_binding(service, "health", contract_id, adapter_id)
    if binding_error:
        return _refusal(
            receipt_schema=HEALTH_RECEIPT_SCHEMA,
            service=service,
            capability="health",
            contract_id=contract_id,
            adapter_id=adapter_id,
            observed_at=observed_at,
            observation_source=observation_source,
            failure_reason=binding_error,
        )

    if health_state not in HEALTH_STATES:
        return _refusal(
            receipt_schema=HEALTH_RECEIPT_SCHEMA,
            service=service,
            capability="health",
            contract_id=contract_id,
            adapter_id=adapter_id,
            observed_at=observed_at,
            observation_source=observation_source,
            failure_reason="INVALID_HEALTH_STATE",
        )

    if not _valid_observed_at(observed_at):
        return _refusal(
            receipt_schema=HEALTH_RECEIPT_SCHEMA,
            service=service,
            capability="health",
            contract_id=contract_id,
            adapter_id=adapter_id,
            observed_at=observed_at,
            observation_source=observation_source,
            failure_reason="INVALID_OR_MISSING_OBSERVATION_TIMESTAMP",
        )

    if not isinstance(observation_source, str) or not observation_source.strip():
        return _refusal(
            receipt_schema=HEALTH_RECEIPT_SCHEMA,
            service=service,
            capability="health",
            contract_id=contract_id,
            adapter_id=adapter_id,
            observed_at=observed_at,
            observation_source=observation_source,
            failure_reason="INVALID_OR_MISSING_OBSERVATION_SOURCE",
        )

    if health_state != "HEALTHY" and not failure_reason:
        failure_reason = f"OBSERVED_{health_state}"

    return {
        "receipt_schema": HEALTH_RECEIPT_SCHEMA,
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "status": "ACCEPTED",
        "service": service,
        "capability": "health",
        "effect": EFFECT,
        "contract_id": resolution["contract_id"],
        "contract_version": CONTRACT_VERSION,
        "adapter_id": resolution["adapter_id"],
        "observed_at": observed_at,
        "observation_source": observation_source,
        "health_state": health_state,
        "telemetry_payload_schema": None,
        "telemetry_payload": None,
        "failure_reason": failure_reason,
        "f4g_required": True,
        "direct_execution_performed": False,
        "network_transport_performed": False,
        "mutation_performed": False,
    }


def build_telemetry_receipt(
    *,
    service: str,
    contract_id: str,
    adapter_id: str,
    observed_at: str,
    observation_source: str,
    health_state: str,
    telemetry_payload_schema: str,
    telemetry_payload: Mapping[str, Any],
    failure_reason: str | None = None,
) -> dict[str, Any]:
    resolution, binding_error = _validate_binding(service, "telemetry", contract_id, adapter_id)
    if binding_error:
        return _refusal(
            receipt_schema=TELEMETRY_RECEIPT_SCHEMA,
            service=service,
            capability="telemetry",
            contract_id=contract_id,
            adapter_id=adapter_id,
            observed_at=observed_at,
            observation_source=observation_source,
            health_state=health_state,
            telemetry_payload_schema=telemetry_payload_schema,
            failure_reason=binding_error,
        )

    if health_state not in HEALTH_STATES:
        return _refusal(
            receipt_schema=TELEMETRY_RECEIPT_SCHEMA,
            service=service,
            capability="telemetry",
            contract_id=contract_id,
            adapter_id=adapter_id,
            observed_at=observed_at,
            observation_source=observation_source,
            telemetry_payload_schema=telemetry_payload_schema,
            failure_reason="INVALID_HEALTH_STATE",
        )

    if not _valid_observed_at(observed_at):
        return _refusal(
            receipt_schema=TELEMETRY_RECEIPT_SCHEMA,
            service=service,
            capability="telemetry",
            contract_id=contract_id,
            adapter_id=adapter_id,
            observed_at=observed_at,
            observation_source=observation_source,
            health_state=health_state,
            telemetry_payload_schema=telemetry_payload_schema,
            failure_reason="INVALID_OR_MISSING_OBSERVATION_TIMESTAMP",
        )

    if not isinstance(observation_source, str) or not observation_source.strip():
        return _refusal(
            receipt_schema=TELEMETRY_RECEIPT_SCHEMA,
            service=service,
            capability="telemetry",
            contract_id=contract_id,
            adapter_id=adapter_id,
            observed_at=observed_at,
            observation_source=observation_source,
            health_state=health_state,
            telemetry_payload_schema=telemetry_payload_schema,
            failure_reason="INVALID_OR_MISSING_OBSERVATION_SOURCE",
        )

    if not isinstance(telemetry_payload_schema, str) or not telemetry_payload_schema.strip():
        return _refusal(
            receipt_schema=TELEMETRY_RECEIPT_SCHEMA,
            service=service,
            capability="telemetry",
            contract_id=contract_id,
            adapter_id=adapter_id,
            observed_at=observed_at,
            observation_source=observation_source,
            health_state=health_state,
            telemetry_payload_schema=telemetry_payload_schema,
            failure_reason="INVALID_OR_MISSING_TELEMETRY_PAYLOAD_SCHEMA",
        )

    if not isinstance(telemetry_payload, Mapping):
        return _refusal(
            receipt_schema=TELEMETRY_RECEIPT_SCHEMA,
            service=service,
            capability="telemetry",
            contract_id=contract_id,
            adapter_id=adapter_id,
            observed_at=observed_at,
            observation_source=observation_source,
            health_state=health_state,
            telemetry_payload_schema=telemetry_payload_schema,
            failure_reason="INVALID_TELEMETRY_PAYLOAD",
        )

    if health_state != "HEALTHY" and not failure_reason:
        failure_reason = f"OBSERVED_{health_state}"

    return {
        "receipt_schema": TELEMETRY_RECEIPT_SCHEMA,
        "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
        "status": "ACCEPTED",
        "service": service,
        "capability": "telemetry",
        "effect": EFFECT,
        "contract_id": resolution["contract_id"],
        "contract_version": CONTRACT_VERSION,
        "adapter_id": resolution["adapter_id"],
        "observed_at": observed_at,
        "observation_source": observation_source,
        "health_state": health_state,
        "telemetry_payload_schema": telemetry_payload_schema,
        "telemetry_payload": dict(telemetry_payload),
        "failure_reason": failure_reason,
        "f4g_required": True,
        "direct_execution_performed": False,
        "network_transport_performed": False,
        "mutation_performed": False,
    }


def project_f4h_state(health_state: str, activity_state: str = "idle") -> str:
    if health_state != "HEALTHY":
        return "degraded"
    if activity_state not in F4H_ACTIVITY_STATES:
        return "degraded"
    return activity_state


def build_foundation_manifest(
    repo: Path,
    accepted_baseline: str,
    inherited_read_model_baseline: str,
) -> dict[str, Any]:
    repo = repo.resolve()
    accepted = resolve_exact_commit(repo, accepted_baseline)
    inherited = resolve_exact_commit(repo, inherited_read_model_baseline)

    read_model_path = (
        repo
        / "applications/constitutional_experience/living_frontend/app/src/platform_read_model.generated.json"
    )
    read_model_bytes = read_model_path.read_bytes()

    service_contracts = {}
    adapters = {}
    for service, record in SERVICE_REGISTRY.items():
        service_contracts[service] = {
            capability: {
                "contract_id": contract_id,
                "contract_version": CONTRACT_VERSION,
                "effect": EFFECT,
                "f4g_required": True,
                "direct_execution": False,
            }
            for capability, contract_id in record["contracts"].items()
        }
        adapters[service] = {
            "adapter_id": record["adapter_id"],
            "kind": "RUNTIME_OBSERVATION_FOUNDATION",
            "live_binding_present": False,
            "network_transport_present": False,
            "direct_subsystem_execution": False,
        }

    return {
        "schema": FOUNDATION_SCHEMA,
        "accepted_platform_integration_baseline": accepted,
        "inherited_read_model_baseline": inherited,
        "accepted_platform_read_model": {
            "path": str(read_model_path.relative_to(repo)),
            "sha256": hashlib.sha256(read_model_bytes).hexdigest(),
        },
        "effect": EFFECT,
        "capabilities": ["health", "telemetry"],
        "service_contract_registry": service_contracts,
        "service_adapter_registry": adapters,
        "receipt_schemas": {
            "health": {
                "receipt_schema": HEALTH_RECEIPT_SCHEMA,
                "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
                "required_fields": [
                    "service",
                    "contract_id",
                    "contract_version",
                    "adapter_id",
                    "observed_at",
                    "observation_source",
                    "health_state",
                    "failure_reason",
                    "receipt_schema",
                    "receipt_schema_version",
                ],
            },
            "telemetry": {
                "receipt_schema": TELEMETRY_RECEIPT_SCHEMA,
                "receipt_schema_version": RECEIPT_SCHEMA_VERSION,
                "required_fields": [
                    "service",
                    "contract_id",
                    "contract_version",
                    "adapter_id",
                    "observed_at",
                    "observation_source",
                    "health_state",
                    "telemetry_payload_schema",
                    "telemetry_payload",
                    "failure_reason",
                    "receipt_schema",
                    "receipt_schema_version",
                ],
            },
        },
        "health_states": list(HEALTH_STATES),
        "f4h_projection": {
            "healthy_preserves_activity_states": list(F4H_ACTIVITY_STATES),
            "non_healthy_projects": "degraded",
            "invalid_activity_projects": "degraded",
            "projected_states": list(F4H_PROJECTED_STATES),
            "visual_restyle_required": False,
        },
        "fail_closed_rules": [
            "unknown service refuses",
            "unknown capability refuses",
            "unknown contract refuses",
            "unknown adapter refuses",
            "missing or invalid observation timestamp refuses",
            "missing or invalid observation source refuses",
            "invalid health state refuses",
            "missing telemetry payload schema refuses",
            "invalid telemetry payload refuses",
            "refused observations never report HEALTHY",
        ],
        "f4g_fail_closed_gate_authoritative": True,
        "allow_is_not_direct_execution": True,
        "network_transport_implementation_authorized": False,
        "live_probe_binding_authorized": False,
        "rpc_binding_authorized": False,
        "websocket_binding_authorized": False,
        "http_endpoint_binding_authorized": False,
        "write_or_mutating_capabilities_authorized": False,
        "a3ye_general_command_execution_authorized": False,
        "autonomous_action_authorized": False,
        "opus_runtime_binding": "DEFERRED_PENDING_CONCRETE_RUNTIME_CONTRACT",
        "protected_mc84f4i_visual_restyle_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--accepted-baseline", required=True)
    parser.add_argument("--inherited-read-model-baseline", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    payload = json.dumps(
        build_foundation_manifest(
            Path(args.repo),
            args.accepted_baseline,
            args.inherited_read_model_baseline,
        ),
        indent=2,
        sort_keys=True,
    ) + "\n"

    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
