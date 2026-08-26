#!/usr/bin/env python3
"""Mission Control read-only in-process runtime health + telemetry binding.

This coordinator binds only already-authorized observation sources:
- Platform Services: exact allowlisted in-process producer methods on caller-supplied
  existing producer instances. The coordinator never instantiates platform runtimes.
- A3ye: exact accepted service-specific runtime observation authority.
- Mammoth: exact accepted service-specific runtime observation authority.

The coordinator requires an explicit normalized F4G ALLOW handoff before invoking
any source. F4G ALLOW is a prerequisite, not execution. This module performs no
network transport, process/liveness probe, persistence mutation, autonomous action,
or Opus binding.
"""
from __future__ import annotations

import importlib
import inspect
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from aletheus.platform.contracts import runtime_observation as foundation

ARCHITECTURE = "CONSTITUTIONAL_PLATFORM_EXECUTION_BRIDGE"
TRANCHE = "RUNTIME_HEALTH_TELEMETRY_IN_PROCESS_BINDING"
EFFECT = "READ_ONLY"
SERVICES = ("Platform Services", "A3ye", "Mammoth")
CAPABILITIES = ("health", "telemetry")
BINDING_RECEIPT_SCHEMA = (
    "aletheus.mission-control-runtime-health-telemetry-binding-receipt.v1"
)
F4G_HANDOFF_SOURCE = "CONSTITUTIONAL_INTERACTION_CAPABILITY_BRIDGE"
F4G_HANDOFF_SCHEMA = "aletheus.f4g-binding-authorization.v1"

A3YE_AUTHORITY_MODULE = "aletheus.a3ye.runtime_observation"
A3YE_SOURCE_CLASS = "A3yeRuntimeObservationSource"
A3YE_AUTHORITY_PATH = "aletheus/a3ye/runtime_observation.py"

MAMMOTH_AUTHORITY_MODULE = "aletheus.mammoth.runtime_observation"
MAMMOTH_SOURCE_CLASS = "MammothRuntimeObservationSource"
MAMMOTH_AUTHORITY_PATH = "aletheus/mammoth/runtime_observation.py"

PLATFORM_HEALTH_AUTHORITIES = frozenset(
    {
        "aletheus.platform.application_runtime.ApplicationRuntime.health",
        "aletheus.platform.contracts.service.PlatformService.health",
        "aletheus.platform.service_registry.ServiceRegistry.health",
        "aletheus.runtime.adapter.DefaultRuntimeAdapter.health",
        "aletheus.runtime.adapter.DefaultRuntimeAdapter.status",
        "aletheus.runtime.adapter.RuntimeAdapterProtocol.health",
        "aletheus.runtime.adapter.RuntimeAdapterProtocol.status",
        "aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.health_report",
        "aletheus.runtime.core.AletheusRuntime.health",
    }
)

PLATFORM_TELEMETRY_AUTHORITIES = frozenset(
    {
        "aletheus.platform.contracts.service.PlatformService.metrics",
        "aletheus.platform.contracts.service.PlatformService.snapshot",
        "aletheus.runtime.adapters.compatibility_adapter.CompatibilityCommandAdapter.statistics",
        "aletheus.runtime.adapters.event_adapter.EventCommandAdapter.statistics",
        "aletheus.runtime.adapters.mission_adapter.MissionCommandAdapter.stats",
        "aletheus.runtime.adapters.prediction_adapter.PredictionAdapter.statistics",
        "aletheus.runtime.adapters.prediction_adapter.PredictionAdapter.stats",
        "aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.snapshot",
        "aletheus.runtime.adapters.topology_registry_adapter.TopologyRegistryAdapter.snapshot",
        "aletheus.runtime.adapters.universal_intelligence_adapter.UniversalIntelligenceAdapter.snapshot",
        "aletheus.runtime.adapters.universal_intelligence_adapter.UniversalIntelligenceAdapter.stats",
    }
)

REPOSITORY_EVIDENCE_IS_LIVENESS = False
ACTUAL_PROCESS_LIVENESS_ESTABLISHED = False
LIVE_BINDING_PERFORMED = False
NETWORK_TRANSPORT_IMPLEMENTED = False
LIVE_PROBE_IMPLEMENTED = False
RPC_IMPLEMENTED = False
WEBSOCKET_IMPLEMENTED = False
HTTP_ENDPOINT_IMPLEMENTED = False
WRITE_OR_MUTATING_CAPABILITY_IMPLEMENTED = False
AUTONOMOUS_ACTION_IMPLEMENTED = False
OPUS_RUNTIME_BINDING_IMPLEMENTED = False
PROTECTED_MC84F4I_VISUAL_CHANGE_PERFORMED = False


class RuntimeHealthTelemetryBindingError(RuntimeError):
    """Internal binding error converted to a fail-closed refusal receipt."""


def _nested_scalar(value: Any, keys: tuple[str, ...]) -> Any:
    wanted = {k.lower() for k in keys}
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).lower() in wanted and isinstance(
                child, (str, int, float, bool)
            ):
                return child
        for child in value.values():
            found = _nested_scalar(child, keys)
            if found not in (None, ""):
                return found
    elif isinstance(value, (list, tuple)):
        for child in value:
            found = _nested_scalar(child, keys)
            if found not in (None, ""):
                return found
    return None


def _call_supported(builder: Any, **kwargs: Any) -> dict[str, Any]:
    signature = inspect.signature(builder)
    has_var_kwargs = any(
        p.kind is inspect.Parameter.VAR_KEYWORD
        for p in signature.parameters.values()
    )
    accepted = (
        kwargs
        if has_var_kwargs
        else {k: v for k, v in kwargs.items() if k in signature.parameters}
    )
    result = builder(**accepted)
    if not isinstance(result, dict):
        raise RuntimeHealthTelemetryBindingError(
            f"receipt builder returned {type(result).__name__}, expected dict"
        )
    return result


def _resolved_contract(service: str, capability: str) -> dict[str, Any]:
    result = foundation.resolve_contract(service, capability)
    if not isinstance(result, Mapping) or result.get("status") != "RESOLVED":
        raise RuntimeHealthTelemetryBindingError(
            f"contract resolution refused {service}/{capability}"
        )
    if result.get("effect") != EFFECT:
        raise RuntimeHealthTelemetryBindingError("contract effect is not READ_ONLY")
    if result.get("f4g_required") is not True:
        raise RuntimeHealthTelemetryBindingError("contract does not require F4G")
    if result.get("allow_is_not_direct_execution") is not True:
        raise RuntimeHealthTelemetryBindingError(
            "contract violates ALLOW-not-direct-execution boundary"
        )
    if result.get("direct_execution_performed") is not False:
        raise RuntimeHealthTelemetryBindingError(
            "contract incorrectly claims direct execution"
        )
    return dict(result)


def _resolved_identity(result: Mapping[str, Any], key: str) -> str:
    aliases = {
        "contract_id": ("contract_id", "contractId"),
        "adapter_id": ("adapter_id", "adapterId"),
    }
    value = _nested_scalar(result, aliases[key])
    if not isinstance(value, str) or not value.strip():
        raise RuntimeHealthTelemetryBindingError(f"{key} unavailable")
    return value


@dataclass(frozen=True)
class F4GAuthorization:
    """Normalized handoff from the authoritative F4G evaluation layer."""

    service: str
    capability: str
    effect: str = EFFECT
    status: str = "ALLOW"
    source: str = F4G_HANDOFF_SOURCE
    schema: str = F4G_HANDOFF_SCHEMA
    direct_execution_performed: bool = False


def normalize_f4g_authorization(
    receipt: F4GAuthorization | Mapping[str, Any],
    *,
    service: str,
    capability: str,
) -> F4GAuthorization:
    if isinstance(receipt, F4GAuthorization):
        auth = receipt
    elif isinstance(receipt, Mapping):
        auth = F4GAuthorization(
            service=str(receipt.get("service", "")),
            capability=str(receipt.get("capability", "")),
            effect=str(receipt.get("effect", "")),
            status=str(receipt.get("status", receipt.get("decision", ""))),
            source=str(receipt.get("source", "")),
            schema=str(receipt.get("schema", "")),
            direct_execution_performed=bool(
                receipt.get("direct_execution_performed", False)
            ),
        )
    else:
        raise RuntimeHealthTelemetryBindingError("F4G receipt is not structured")

    if auth.schema != F4G_HANDOFF_SCHEMA:
        raise RuntimeHealthTelemetryBindingError("unknown F4G handoff schema")
    if auth.source != F4G_HANDOFF_SOURCE:
        raise RuntimeHealthTelemetryBindingError("unknown F4G handoff source")
    if auth.status != "ALLOW":
        raise RuntimeHealthTelemetryBindingError("F4G did not ALLOW")
    if auth.service != service:
        raise RuntimeHealthTelemetryBindingError("F4G service mismatch")
    if auth.capability != capability:
        raise RuntimeHealthTelemetryBindingError("F4G capability mismatch")
    if auth.effect != EFFECT:
        raise RuntimeHealthTelemetryBindingError("F4G effect mismatch")
    if auth.direct_execution_performed is not False:
        raise RuntimeHealthTelemetryBindingError(
            "F4G receipt indicates direct execution"
        )
    return auth


def _refusal(
    *,
    service: str,
    capability: str,
    reason: str,
    activity: str = "idle",
) -> dict[str, Any]:
    try:
        f4h_state = foundation.project_f4h_state("UNKNOWN", activity)
    except Exception:
        f4h_state = "degraded"
    return {
        "schema": BINDING_RECEIPT_SCHEMA,
        "status": "REFUSED",
        "service": service,
        "capability": capability,
        "effect": EFFECT,
        "health_state": "UNKNOWN",
        "failure_reason": reason,
        "f4h_state": f4h_state,
        "f4g_authorized": False,
        "allow_is_not_direct_execution": True,
        "direct_execution_performed": False,
        "repository_evidence_is_liveness": False,
        "actual_process_liveness_established": False,
        "live_binding_performed": False,
    }


def _validate_activity(activity: str) -> None:
    if activity not in {"idle", "focused", "engaged"}:
        raise RuntimeHealthTelemetryBindingError("unknown F4H activity")


def _validate_upstream_receipt(
    receipt: Mapping[str, Any],
    *,
    service: str,
    capability: str,
    resolved: Mapping[str, Any],
) -> tuple[str, str, str]:
    if receipt.get("status") == "REFUSED":
        raise RuntimeHealthTelemetryBindingError(
            str(receipt.get("failure_reason") or "upstream observation refused")
        )
    if receipt.get("service") != service:
        raise RuntimeHealthTelemetryBindingError("upstream service mismatch")
    if receipt.get("effect") != EFFECT:
        raise RuntimeHealthTelemetryBindingError("upstream effect mismatch")

    expected_contract = _resolved_identity(resolved, "contract_id")
    expected_adapter = _resolved_identity(resolved, "adapter_id")
    actual_contract = _nested_scalar(receipt, ("contract_id", "contractId"))
    actual_adapter = _nested_scalar(receipt, ("adapter_id", "adapterId"))

    if actual_contract != expected_contract:
        raise RuntimeHealthTelemetryBindingError("upstream contract mismatch")
    if actual_adapter != expected_adapter:
        raise RuntimeHealthTelemetryBindingError("upstream adapter mismatch")

    observed_at = _nested_scalar(
        receipt, ("observed_at", "observedAt", "observation_timestamp")
    )
    observation_source = _nested_scalar(
        receipt, ("observation_source", "observationSource", "source")
    )
    health_state = _nested_scalar(receipt, ("health_state", "healthState"))

    if not isinstance(observed_at, str) or not observed_at.strip():
        raise RuntimeHealthTelemetryBindingError("missing observation timestamp")
    if not isinstance(observation_source, str) or not observation_source.strip():
        raise RuntimeHealthTelemetryBindingError("missing observation source")
    if health_state not in foundation.HEALTH_STATES:
        raise RuntimeHealthTelemetryBindingError("invalid upstream health state")

    if capability == "telemetry":
        telemetry_schema = _nested_scalar(
            receipt,
            (
                "telemetry_payload_schema",
                "telemetry_schema",
                "payload_schema",
            ),
        )
        if not isinstance(telemetry_schema, str) or not telemetry_schema.strip():
            raise RuntimeHealthTelemetryBindingError("missing telemetry schema")

    return str(observed_at), str(observation_source), str(health_state)


def _binding_receipt(
    *,
    service: str,
    capability: str,
    authority: str,
    upstream: Mapping[str, Any],
    resolved: Mapping[str, Any],
    activity: str,
) -> dict[str, Any]:
    observed_at, observation_source, health_state = _validate_upstream_receipt(
        upstream,
        service=service,
        capability=capability,
        resolved=resolved,
    )
    f4h_state = foundation.project_f4h_state(health_state, activity)
    failure_reason = _nested_scalar(upstream, ("failure_reason", "failureReason"))
    return {
        "schema": BINDING_RECEIPT_SCHEMA,
        "status": "BOUND",
        "service": service,
        "capability": capability,
        "effect": EFFECT,
        "authority": authority,
        "contract_id": _resolved_identity(resolved, "contract_id"),
        "adapter_id": _resolved_identity(resolved, "adapter_id"),
        "observed_at": observed_at,
        "observation_source": observation_source,
        "health_state": health_state,
        "failure_reason": str(failure_reason or ""),
        "f4h_state": f4h_state,
        "f4g_authorized": True,
        "allow_is_not_direct_execution": True,
        "direct_execution_performed": False,
        "repository_evidence_is_liveness": False,
        "actual_process_liveness_established": False,
        "live_binding_performed": False,
        "upstream_receipt": dict(upstream),
    }


def _platform_callable_identity(producer: Any, method_name: str) -> str:
    cls = producer.__class__
    module = getattr(cls, "__module__", "")
    qualname = getattr(cls, "__qualname__", getattr(cls, "__name__", ""))
    if not module or not qualname:
        raise RuntimeHealthTelemetryBindingError(
            "platform producer identity unavailable"
        )
    return f"{module}.{qualname}.{method_name}"


def _extract_platform_health_state(result: Any) -> str:
    if isinstance(result, str):
        state = result.upper()
    elif isinstance(result, Mapping):
        raw = _nested_scalar(result, ("health_state", "healthState", "state", "status"))
        state = str(raw).upper() if raw not in (None, "") else ""
    else:
        state = ""
    if state not in foundation.HEALTH_STATES:
        raise RuntimeHealthTelemetryBindingError(
            "platform producer did not emit an explicit accepted health state"
        )
    return state


def _invoke_platform_method(producer: Any, method_name: str) -> Any:
    method = getattr(producer, method_name, None)
    if method is None or not callable(method):
        raise RuntimeHealthTelemetryBindingError("platform producer method missing")
    signature = inspect.signature(method)
    required = [
        p
        for p in signature.parameters.values()
        if p.default is inspect.Parameter.empty
        and p.kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        )
    ]
    if required:
        raise RuntimeHealthTelemetryBindingError(
            "platform producer requires invocation arguments"
        )
    return method()


def _platform_upstream_receipt(
    *,
    capability: str,
    producer: Any,
    authority: str,
    observed_at: str,
    observation_source: str,
    telemetry_payload_schema: str,
) -> dict[str, Any]:
    if not observed_at:
        raise RuntimeHealthTelemetryBindingError("missing observation timestamp")
    if not observation_source:
        raise RuntimeHealthTelemetryBindingError("missing observation source")

    method_name = authority.rsplit(".", 1)[-1]
    actual_identity = _platform_callable_identity(producer, method_name)
    if actual_identity != authority:
        raise RuntimeHealthTelemetryBindingError(
            f"platform producer identity mismatch: {actual_identity}"
        )

    allowed = (
        PLATFORM_HEALTH_AUTHORITIES
        if capability == "health"
        else PLATFORM_TELEMETRY_AUTHORITIES
    )
    if authority not in allowed:
        raise RuntimeHealthTelemetryBindingError(
            "platform producer authority not allowlisted"
        )

    result = _invoke_platform_method(producer, method_name)
    resolved = _resolved_contract("Platform Services", capability)
    kwargs = {
        "service": "Platform Services",
        "contract_id": _resolved_identity(resolved, "contract_id"),
        "adapter_id": _resolved_identity(resolved, "adapter_id"),
        "observed_at": observed_at,
        "observation_source": observation_source,
        "failure_reason": "",
    }

    if capability == "health":
        kwargs["health_state"] = _extract_platform_health_state(result)
        return _call_supported(foundation.build_health_receipt, **kwargs)

    if not isinstance(result, Mapping):
        raise RuntimeHealthTelemetryBindingError(
            "platform telemetry producer must return a mapping"
        )
    if not telemetry_payload_schema:
        raise RuntimeHealthTelemetryBindingError("missing telemetry payload schema")

    try:
        health_state = _extract_platform_health_state(result)
    except RuntimeHealthTelemetryBindingError:
        health_state = "UNKNOWN"

    kwargs.update(
        {
            "health_state": health_state,
            "telemetry_payload_schema": telemetry_payload_schema,
            "telemetry_payload": dict(result),
        }
    )
    return _call_supported(foundation.build_telemetry_receipt, **kwargs)


def _service_specific_upstream_receipt(
    *,
    service: str,
    capability: str,
    observation: Any,
) -> tuple[str, dict[str, Any]]:
    if service == "A3ye":
        module_name = A3YE_AUTHORITY_MODULE
        source_class_name = A3YE_SOURCE_CLASS
        authority_path = A3YE_AUTHORITY_PATH
    elif service == "Mammoth":
        module_name = MAMMOTH_AUTHORITY_MODULE
        source_class_name = MAMMOTH_SOURCE_CLASS
        authority_path = MAMMOTH_AUTHORITY_PATH
    else:
        raise RuntimeHealthTelemetryBindingError(
            "service-specific binding requested for unsupported service"
        )

    observation_module = getattr(observation.__class__, "__module__", "")
    if observation_module != module_name:
        raise RuntimeHealthTelemetryBindingError(
            "observation object is not owned by accepted service authority"
        )

    module = importlib.import_module(module_name)
    source_class = getattr(module, source_class_name, None)
    if source_class is None:
        raise RuntimeHealthTelemetryBindingError(
            "accepted service observation source unavailable"
        )
    source = source_class()
    method = getattr(source, capability, None)
    if method is None or not callable(method):
        raise RuntimeHealthTelemetryBindingError(
            "accepted service observation capability unavailable"
        )
    result = method(observation)
    if not isinstance(result, Mapping):
        raise RuntimeHealthTelemetryBindingError(
            "service observation source returned non-structured result"
        )
    return authority_path, dict(result)


class RuntimeHealthTelemetryInProcessBinding:
    """Fail-closed coordinator for read-only health/telemetry binding."""

    def bind(
        self,
        *,
        service: str,
        capability: str,
        f4g_authorization: F4GAuthorization | Mapping[str, Any],
        activity: str = "idle",
        observation: Any = None,
        producer: Any = None,
        authority: str = "",
        observed_at: str = "",
        observation_source: str = "",
        telemetry_payload_schema: str = "",
    ) -> dict[str, Any]:
        try:
            if service not in SERVICES:
                raise RuntimeHealthTelemetryBindingError("unknown service")
            if capability not in CAPABILITIES:
                raise RuntimeHealthTelemetryBindingError("unknown capability")
            _validate_activity(activity)
            resolved = _resolved_contract(service, capability)
            normalize_f4g_authorization(
                f4g_authorization,
                service=service,
                capability=capability,
            )

            if service == "Platform Services":
                if producer is None:
                    raise RuntimeHealthTelemetryBindingError(
                        "platform producer not supplied"
                    )
                if not authority:
                    raise RuntimeHealthTelemetryBindingError(
                        "platform producer authority not supplied"
                    )
                upstream = _platform_upstream_receipt(
                    capability=capability,
                    producer=producer,
                    authority=authority,
                    observed_at=observed_at,
                    observation_source=observation_source,
                    telemetry_payload_schema=telemetry_payload_schema,
                )
                bound_authority = authority
            else:
                if observation is None:
                    raise RuntimeHealthTelemetryBindingError(
                        "service observation not supplied"
                    )
                bound_authority, upstream = _service_specific_upstream_receipt(
                    service=service,
                    capability=capability,
                    observation=observation,
                )

            return _binding_receipt(
                service=service,
                capability=capability,
                authority=bound_authority,
                upstream=upstream,
                resolved=resolved,
                activity=activity,
            )
        except Exception as exc:
            return _refusal(
                service=service,
                capability=capability,
                reason=str(exc),
                activity=activity if activity in {"idle", "focused", "engaged"} else "idle",
            )


def build_manifest() -> dict[str, Any]:
    return {
        "schema": "aletheus.mission-control-runtime-health-telemetry-in-process-binding.v1",
        "architecture": ARCHITECTURE,
        "tranche": TRANCHE,
        "effect": EFFECT,
        "binding_mode": "IN_PROCESS_ONLY",
        "services": list(SERVICES),
        "capabilities": list(CAPABILITIES),
        "binding_receipt_schema": BINDING_RECEIPT_SCHEMA,
        "f4g_handoff": {
            "schema": F4G_HANDOFF_SCHEMA,
            "source": F4G_HANDOFF_SOURCE,
            "required_before_observation": True,
            "allow_is_not_direct_execution": True,
        },
        "f4h_projection": {
            "required": True,
            "non_healthy_projects_degraded": True,
        },
        "platform_services": {
            "health_authorities": sorted(PLATFORM_HEALTH_AUTHORITIES),
            "telemetry_authorities": sorted(PLATFORM_TELEMETRY_AUTHORITIES),
            "producer_instances_are_caller_supplied": True,
            "runtime_instantiation_performed": False,
        },
        "a3ye": {
            "runtime_producer_authority_path": A3YE_AUTHORITY_PATH,
            "source_class": A3YE_SOURCE_CLASS,
        },
        "mammoth": {
            "runtime_producer_authority_path": MAMMOTH_AUTHORITY_PATH,
            "source_class": MAMMOTH_SOURCE_CLASS,
        },
        "test_files_are_runtime_producer_authority": False,
        "fixture_files_are_runtime_producer_authority": False,
        "documentation_is_runtime_producer_authority": False,
        "backup_files_are_runtime_producer_authority": False,
        "report_files_are_runtime_producer_authority": False,
        "repository_evidence_is_liveness": False,
        "actual_process_liveness_established": False,
        "live_binding_performed": False,
        "process_liveness_probe": False,
        "network_transport": False,
        "http_endpoint": False,
        "websocket": False,
        "rpc": False,
        "socket_transport": False,
        "write_or_mutating_capability": False,
        "autonomous_action": False,
        "generalized_a3ye_command_execution": False,
        "generalized_mammoth_command_execution": False,
        "direct_ungated_subsystem_reach_through": False,
        "opus_runtime_binding": False,
        "protected_mc84f4i_visual_change": False,
    }


def main() -> int:
    import argparse

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
