#!/usr/bin/env python3
"""Mammoth read-only runtime health and telemetry observation foundation.

This module establishes Mammoth's explicit service-owned in-process observation
boundary. It does not inspect storage engines, probe processes, open network
transports, perform persistence operations, or claim runtime liveness. Callers
must supply explicit observations; the accepted generic runtime observation
contract remains authoritative for receipt validation and refusal.
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

SERVICE_IDENTITY = "Mammoth"
SERVICE_ROLE = (
    "storage,persistence,indexing,replication,archive,recovery,lifecycle"
)
SOURCE_IDENTITY = "mammoth.runtime-observation-source.v1"
SOURCE_KIND = "IN_PROCESS_READ_ONLY_OBSERVATION_SOURCE_FOUNDATION"
CAPABILITIES = ("health", "telemetry")
EFFECT = "READ_ONLY"
RUNTIME_PRODUCER_AUTHORITY_PATH = "aletheus/mammoth/runtime_observation.py"

RUNTIME_LIVENESS_ESTABLISHED = False
REPOSITORY_EVIDENCE_IS_LIVENESS = False
LIVE_BINDING_PERFORMED = False
LIVE_PROBE_BOUND = False
NETWORK_TRANSPORT_BOUND = False
RPC_BOUND = False
WEBSOCKET_BOUND = False
HTTP_ENDPOINT_BOUND = False
WRITE_OR_MUTATING_CAPABILITY_BOUND = False
AUTONOMOUS_ACTION_BOUND = False
DIRECT_UNGATED_SUBSYSTEM_REACH_THROUGH_BOUND = False


class MammothObservationFoundationError(RuntimeError):
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
        raise MammothObservationFoundationError(
            f"accepted contract refused Mammoth/{capability}: {result!r}"
        )
    if result.get("effect") != EFFECT:
        raise MammothObservationFoundationError(
            f"Mammoth/{capability} is not READ_ONLY: {result!r}"
        )
    if result.get("f4g_required") is not True:
        raise MammothObservationFoundationError(
            f"Mammoth/{capability} does not require F4G: {result!r}"
        )
    if result.get("allow_is_not_direct_execution") is not True:
        raise MammothObservationFoundationError(
            f"Mammoth/{capability} violates ALLOW-not-execution boundary: {result!r}"
        )
    if result.get("direct_execution_performed") is not False:
        raise MammothObservationFoundationError(
            f"Mammoth/{capability} indicates direct execution: {result!r}"
        )

    contract_id = _nested_value(result, ("contract_id", "contractId"))
    adapter_id = _nested_value(result, ("adapter_id", "adapterId"))
    if not isinstance(contract_id, str) or not contract_id.strip():
        raise MammothObservationFoundationError(
            f"Mammoth/{capability} contract_id unavailable in accepted registry"
        )
    if not isinstance(adapter_id, str) or not adapter_id.strip():
        raise MammothObservationFoundationError(
            f"Mammoth/{capability} adapter_id unavailable in accepted registry"
        )

    contract_version = _nested_value(
        result, ("contract_version", "contractVersion")
    )
    adapter_version = _nested_value(
        result, ("adapter_version", "adapterVersion")
    )
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
    accepted = (
        kwargs
        if has_var_kwargs
        else {k: v for k, v in kwargs.items() if k in signature.parameters}
    )
    result = builder(**accepted)
    if not isinstance(result, dict):
        raise MammothObservationFoundationError(
            f"accepted receipt builder returned non-dict: {type(result).__name__}"
        )
    return result


def _receipt_schema_version() -> str:
    binding = _resolve_binding("health")
    sample = _call_supported(
        foundation.build_health_receipt,
        service=SERVICE_IDENTITY,
        contract_id=binding["contract_id"],
        adapter_id=binding["adapter_id"],
        observed_at="1970-01-01T00:00:00+00:00",
        observation_source=SOURCE_IDENTITY,
        health_state="UNKNOWN",
        failure_reason="schema-introspection-only",
    )
    schema = _nested_value(
        sample,
        (
            "receipt_schema_version",
            "receipt_schema",
            "schema_version",
            "schema",
        ),
    )
    if not isinstance(schema, str) or not schema.strip():
        raise MammothObservationFoundationError(
            "accepted generic receipt schema version unavailable"
        )
    return schema


@dataclass(frozen=True)
class MammothObservation:
    """Explicit caller-supplied observation; never inferred from repository state."""

    observed_at: str
    observation_source: str = SOURCE_IDENTITY
    health_state: str = "UNKNOWN"
    failure_reason: str = ""
    telemetry_payload_schema: str = ""
    telemetry_payload: Mapping[str, Any] = field(default_factory=dict)


class MammothRuntimeObservationSource:
    """Authoritative Mammoth observation API boundary, without live binding."""

    service_identity = SERVICE_IDENTITY
    service_role = SERVICE_ROLE
    source_identity = SOURCE_IDENTITY
    source_kind = SOURCE_KIND
    effect = EFFECT
    runtime_producer_authority_path = RUNTIME_PRODUCER_AUTHORITY_PATH
    runtime_liveness_established = False
    repository_evidence_is_liveness = False
    live_binding_performed = False
    live_probe_bound = False
    network_transport_bound = False

    def health(self, observation: MammothObservation) -> dict[str, Any]:
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

    def telemetry(self, observation: MammothObservation) -> dict[str, Any]:
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
        "schema": "aletheus.mammoth-runtime-observation-foundation.v1",
        "receipt_schema_version": _receipt_schema_version(),
        "service_identity": SERVICE_IDENTITY,
        "service_role": SERVICE_ROLE,
        "service_ownership_evidence": {
            "authority_path": RUNTIME_PRODUCER_AUTHORITY_PATH,
            "identity_constant": SERVICE_IDENTITY,
            "role_constant": SERVICE_ROLE,
        },
        "source_identity": SOURCE_IDENTITY,
        "source_kind": SOURCE_KIND,
        "effect": EFFECT,
        "capabilities": list(CAPABILITIES),
        "health_states": list(foundation.HEALTH_STATES),
        "health_contract": health,
        "telemetry_contract": telemetry,
        "observation_fields": [
            "observed_at",
            "observation_source",
            "health_state",
            "failure_reason",
            "telemetry_payload_schema",
            "telemetry_payload",
        ],
        "runtime_producer_authority_paths": [
            RUNTIME_PRODUCER_AUTHORITY_PATH
        ],
        "test_files_are_runtime_producer_authority": False,
        "fixture_files_are_runtime_producer_authority": False,
        "documentation_is_runtime_producer_authority": False,
        "backup_files_are_runtime_producer_authority": False,
        "report_files_are_runtime_producer_authority": False,
        "f4g_fail_closed_gate_authoritative": True,
        "allow_is_not_direct_execution": True,
        "f4h_state_projection_foundation_required": True,
        "runtime_liveness_established": False,
        "repository_evidence_is_liveness": False,
        "live_binding_performed": False,
        "live_probe_binding": False,
        "network_transport_binding": False,
        "rpc_binding": False,
        "websocket_binding": False,
        "http_endpoint_binding": False,
        "write_or_mutating_capability": False,
        "autonomous_action": False,
        "direct_ungated_subsystem_reach_through": False,
        "platform_services_binding_implementation": False,
        "a3ye_binding_implementation": False,
        "opus_runtime_binding": "DEFERRED_PENDING_CONCRETE_RUNTIME_CONTRACT",
        "protected_mc84f4i_visual_change": False,
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
