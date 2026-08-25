#!/usr/bin/env python3
"""A3ye read-only runtime health and telemetry observation foundation.

This module is an in-process observation boundary only. It does not probe
processes, execute A3ye commands, open network transports, or mutate runtime
state. Callers must supply explicit observations; the accepted generic runtime
observation contract remains authoritative for receipt validation/refusal.
"""
from __future__ import annotations

import argparse
import inspect
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from aletheus.platform.contracts import runtime_observation as foundation

SERVICE_IDENTITY = "A3ye"
SOURCE_IDENTITY = "a3ye.runtime-observation-source.v1"
SOURCE_KIND = "IN_PROCESS_READ_ONLY_OBSERVATION_SOURCE_FOUNDATION"
CAPABILITIES = ("health", "telemetry")
EFFECT = "READ_ONLY"
RUNTIME_LIVENESS_ESTABLISHED = False
LIVE_PROBE_BOUND = False
NETWORK_TRANSPORT_BOUND = False
GENERAL_COMMAND_EXECUTION_BOUND = False
AUTONOMOUS_ACTION_BOUND = False
WRITE_OR_MUTATING_CAPABILITY_BOUND = False


class A3yeObservationFoundationError(RuntimeError):
    """Raised when the accepted generic contract cannot be resolved safely."""


def _nested_value(value: Any, key_names: tuple[str, ...]) -> Any:
    wanted = {k.lower() for k in key_names}
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in wanted and child not in (None, ""):
                if isinstance(child, (str, int, float, bool)):
                    return child
            found = _nested_value(child, key_names)
            if found not in (None, ""):
                return found
    elif isinstance(value, (list, tuple)):
        for child in value:
            found = _nested_value(child, key_names)
            if found not in (None, ""):
                return found
    return None


def _version_from_identifier(identifier: str) -> str:
    match = re.search(r"(?:^|[._-])(v\d+)(?:$|[._-])", identifier, re.I)
    return match.group(1).lower() if match else "v1"


def _resolve_binding(capability: str) -> dict[str, str]:
    result = foundation.resolve_contract(SERVICE_IDENTITY, capability)
    if not isinstance(result, Mapping) or result.get("status") != "RESOLVED":
        raise A3yeObservationFoundationError(
            f"accepted contract refused A3ye/{capability}: {result!r}"
        )
    if result.get("effect") != EFFECT:
        raise A3yeObservationFoundationError(
            f"A3ye/{capability} is not READ_ONLY: {result!r}"
        )
    if result.get("f4g_required") is not True:
        raise A3yeObservationFoundationError(
            f"A3ye/{capability} does not require F4G: {result!r}"
        )
    if result.get("allow_is_not_direct_execution") is not True:
        raise A3yeObservationFoundationError(
            f"A3ye/{capability} violates ALLOW-not-execution boundary: {result!r}"
        )
    if result.get("direct_execution_performed") is not False:
        raise A3yeObservationFoundationError(
            f"A3ye/{capability} indicates direct execution: {result!r}"
        )

    registry = getattr(foundation, "SERVICE_REGISTRY", {})
    service_scope = registry.get(SERVICE_IDENTITY, {}) if isinstance(registry, Mapping) else {}
    capability_scope = (
        service_scope.get(capability, {})
        if isinstance(service_scope, Mapping)
        else {}
    )

    contract_id = _nested_value(result, ("contract_id", "contractId"))
    if not contract_id:
        contract_id = _nested_value(capability_scope, ("contract_id", "contractId", "id"))
    adapter_id = _nested_value(result, ("adapter_id", "adapterId"))
    if not adapter_id:
        adapter_id = _nested_value(capability_scope, ("adapter_id", "adapterId"))
    if not adapter_id:
        adapter_id = _nested_value(service_scope, ("adapter_id", "adapterId"))
    if not isinstance(contract_id, str) or not contract_id.strip():
        raise A3yeObservationFoundationError(
            f"A3ye/{capability} contract_id unavailable in accepted registry"
        )
    if not isinstance(adapter_id, str) or not adapter_id.strip():
        raise A3yeObservationFoundationError(
            f"A3ye/{capability} adapter_id unavailable in accepted registry"
        )

    contract_version = _nested_value(result, ("contract_version", "contractVersion"))
    adapter_version = _nested_value(result, ("adapter_version", "adapterVersion"))
    if not isinstance(contract_version, str) or not contract_version.strip():
        contract_version = _version_from_identifier(contract_id)
    if not isinstance(adapter_version, str) or not adapter_version.strip():
        adapter_version = _version_from_identifier(adapter_id)

    return {
        "contract_id": contract_id,
        "contract_version": str(contract_version),
        "adapter_id": adapter_id,
        "adapter_version": str(adapter_version),
    }


def _call_supported(builder: Any, **kwargs: Any) -> dict[str, Any]:
    signature = inspect.signature(builder)
    has_var_kwargs = any(
        parameter.kind is inspect.Parameter.VAR_KEYWORD
        for parameter in signature.parameters.values()
    )
    accepted = kwargs if has_var_kwargs else {
        k: v for k, v in kwargs.items() if k in signature.parameters
    }
    result = builder(**accepted)
    if not isinstance(result, dict):
        raise A3yeObservationFoundationError(
            f"accepted receipt builder returned non-dict: {type(result).__name__}"
        )
    return result


@dataclass(frozen=True)
class A3yeObservation:
    """Explicit caller-supplied observation; never inferred from repository state."""

    observed_at: str
    observation_source: str = SOURCE_IDENTITY
    health_state: str = "UNKNOWN"
    failure_reason: str = ""
    telemetry_payload_schema: str = ""
    telemetry_payload: Mapping[str, Any] = field(default_factory=dict)


class A3yeRuntimeObservationSource:
    """Authoritative A3ye observation API boundary, without live binding."""

    service_identity = SERVICE_IDENTITY
    source_identity = SOURCE_IDENTITY
    source_kind = SOURCE_KIND
    effect = EFFECT
    runtime_liveness_established = False
    live_probe_bound = False
    network_transport_bound = False

    def health(self, observation: A3yeObservation) -> dict[str, Any]:
        binding = _resolve_binding("health")
        return _call_supported(
            foundation.build_health_receipt,
            service=SERVICE_IDENTITY,
            contract_id=binding["contract_id"],
            adapter_id=binding["adapter_id"],
            observed_at=observation.observed_at,
            observation_source=observation.observation_source,
            health_state=observation.health_state,
            failure_reason=observation.failure_reason,
        )

    def telemetry(self, observation: A3yeObservation) -> dict[str, Any]:
        binding = _resolve_binding("telemetry")
        return _call_supported(
            foundation.build_telemetry_receipt,
            service=SERVICE_IDENTITY,
            contract_id=binding["contract_id"],
            adapter_id=binding["adapter_id"],
            observed_at=observation.observed_at,
            observation_source=observation.observation_source,
            health_state=observation.health_state,
            failure_reason=observation.failure_reason,
            telemetry_payload_schema=observation.telemetry_payload_schema,
            telemetry_payload=dict(observation.telemetry_payload),
        )


def build_manifest() -> dict[str, Any]:
    health = _resolve_binding("health")
    telemetry = _resolve_binding("telemetry")
    return {
        "schema": "aletheus.a3ye-runtime-observation-foundation.v1",
        "service_identity": SERVICE_IDENTITY,
        "source_identity": SOURCE_IDENTITY,
        "source_kind": SOURCE_KIND,
        "effect": EFFECT,
        "capabilities": list(CAPABILITIES),
        "health_states": list(foundation.HEALTH_STATES),
        "health_contract": health,
        "telemetry_contract": telemetry,
        "observation_fields": [
            "observed_at", "observation_source", "health_state", "failure_reason",
            "telemetry_payload_schema", "telemetry_payload",
        ],
        "f4g_fail_closed_gate_authoritative": True,
        "allow_is_not_direct_execution": True,
        "f4h_state_projection_foundation_required": True,
        "runtime_liveness_established": False,
        "repository_evidence_is_liveness": False,
        "live_probe_binding": False,
        "network_transport_binding": False,
        "rpc_binding": False,
        "websocket_binding": False,
        "http_endpoint_binding": False,
        "general_a3ye_command_execution": False,
        "autonomous_action": False,
        "write_or_mutating_capability": False,
        "direct_ungated_subsystem_reach_through": False,
        "opus_runtime_binding": "DEFERRED_PENDING_CONCRETE_RUNTIME_CONTRACT",
        "protected_mc84f4i_visual_change": False,
        "runtime_producer_authority_paths": ["aletheus/a3ye/runtime_observation.py"],
        "test_files_are_runtime_producer_authority": False,
        "mammoth_binding_implementation_authorized": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(build_manifest(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
