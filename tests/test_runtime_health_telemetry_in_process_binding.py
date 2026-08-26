#!/usr/bin/env python3
from __future__ import annotations

import importlib
import importlib.util
import inspect
import json
import os
import sys
import types
import unittest
from pathlib import Path

REPO = Path(os.environ["ALETHEUSOS_REPO"]).resolve()
MODULE_PATH = Path(os.environ["ALETHEUSOS_BINDING_MODULE"]).resolve()
EXPECTED_MANIFEST = os.environ.get("ALETHEUSOS_BINDING_EXPECTED_MANIFEST")

if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

spec = importlib.util.spec_from_file_location(
    "runtime_health_telemetry_binding_under_test", MODULE_PATH
)
binding = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = binding
spec.loader.exec_module(binding)


def auth(service: str, capability: str, **overrides):
    base = dict(
        service=service,
        capability=capability,
        effect="READ_ONLY",
        status="ALLOW",
        source=binding.F4G_HANDOFF_SOURCE,
        schema=binding.F4G_HANDOFF_SCHEMA,
        direct_execution_performed=False,
    )
    base.update(overrides)
    return base


def make_platform_class(module_name, class_name, method_name, result):
    def method(self):
        return result

    method.__name__ = method_name
    method.__qualname__ = f"{class_name}.{method_name}"
    method.__module__ = module_name
    cls = type(class_name, (), {method_name: method})
    cls.__module__ = module_name
    cls.__qualname__ = class_name
    return cls


def build_service_observation(module_name: str, healthy=True, telemetry=True):
    module = importlib.import_module(module_name)
    candidates = []
    for name, obj in vars(module).items():
        if (
            inspect.isclass(obj)
            and obj.__module__ == module_name
            and name.endswith("Observation")
            and "Source" not in name
        ):
            candidates.append(obj)
    if not candidates:
        raise AssertionError(f"no observation class found in {module_name}")
    cls = sorted(candidates, key=lambda c: c.__name__)[0]
    sig = inspect.signature(cls)
    values = {
        "observed_at": "2026-08-25T18:30:00-05:00",
        "observation_source": "test.explicit-observation",
        "health_state": "HEALTHY" if healthy else "DEGRADED",
        "failure_reason": "" if healthy else "test degraded",
        "telemetry_payload_schema": (
            "aletheus.binding-test.telemetry.v1" if telemetry else ""
        ),
        "telemetry_payload": {"sample": 1},
    }
    kwargs = {
        name: values[name]
        for name in sig.parameters
        if name in values
    }
    return cls(**kwargs)


class RuntimeHealthTelemetryBindingTests(unittest.TestCase):
    def setUp(self):
        self.coordinator = binding.RuntimeHealthTelemetryInProcessBinding()

    def test_01_manifest_declares_exact_tranche(self):
        m = binding.build_manifest()
        self.assertEqual(
            m["tranche"], "RUNTIME_HEALTH_TELEMETRY_IN_PROCESS_BINDING"
        )
        self.assertEqual(m["binding_mode"], "IN_PROCESS_ONLY")
        self.assertEqual(m["effect"], "READ_ONLY")

    def test_02_only_three_services_are_supported(self):
        self.assertEqual(
            binding.SERVICES, ("Platform Services", "A3ye", "Mammoth")
        )

    def test_03_only_health_and_telemetry_are_supported(self):
        self.assertEqual(binding.CAPABILITIES, ("health", "telemetry"))

    def test_04_unknown_service_refuses(self):
        r = self.coordinator.bind(
            service="Opus",
            capability="health",
            f4g_authorization=auth("Opus", "health"),
        )
        self.assertEqual(r["status"], "REFUSED")
        self.assertEqual(r["health_state"], "UNKNOWN")

    def test_05_unknown_capability_refuses(self):
        r = self.coordinator.bind(
            service="Mammoth",
            capability="write",
            f4g_authorization=auth("Mammoth", "write"),
        )
        self.assertEqual(r["status"], "REFUSED")
        self.assertEqual(r["health_state"], "UNKNOWN")

    def test_06_f4g_refusal_blocks_observation(self):
        r = self.coordinator.bind(
            service="Mammoth",
            capability="health",
            f4g_authorization=auth("Mammoth", "health", status="REFUSE"),
        )
        self.assertEqual(r["status"], "REFUSED")
        self.assertFalse(r["f4g_authorized"])

    def test_07_f4g_service_mismatch_refuses(self):
        r = self.coordinator.bind(
            service="A3ye",
            capability="health",
            f4g_authorization=auth("Mammoth", "health"),
        )
        self.assertEqual(r["status"], "REFUSED")

    def test_08_f4g_capability_mismatch_refuses(self):
        r = self.coordinator.bind(
            service="A3ye",
            capability="health",
            f4g_authorization=auth("A3ye", "telemetry"),
        )
        self.assertEqual(r["status"], "REFUSED")

    def test_09_f4g_unknown_schema_refuses(self):
        r = self.coordinator.bind(
            service="A3ye",
            capability="health",
            f4g_authorization=auth(
                "A3ye", "health", schema="unknown.f4g.v0"
            ),
        )
        self.assertEqual(r["status"], "REFUSED")

    def test_10_f4g_direct_execution_flag_refuses(self):
        r = self.coordinator.bind(
            service="A3ye",
            capability="health",
            f4g_authorization=auth(
                "A3ye", "health", direct_execution_performed=True
            ),
        )
        self.assertEqual(r["status"], "REFUSED")

    def test_11_unknown_f4h_activity_refuses(self):
        r = self.coordinator.bind(
            service="Mammoth",
            capability="health",
            f4g_authorization=auth("Mammoth", "health"),
            activity="executing",
        )
        self.assertEqual(r["status"], "REFUSED")

    def test_12_platform_health_exact_authority_binds(self):
        cls = make_platform_class(
            "aletheus.platform.application_runtime",
            "ApplicationRuntime",
            "health",
            {"health_state": "HEALTHY"},
        )
        r = self.coordinator.bind(
            service="Platform Services",
            capability="health",
            f4g_authorization=auth("Platform Services", "health"),
            producer=cls(),
            authority=(
                "aletheus.platform.application_runtime."
                "ApplicationRuntime.health"
            ),
            observed_at="2026-08-25T18:30:00-05:00",
            observation_source="platform.existing-runtime",
            activity="engaged",
        )
        self.assertEqual(r["status"], "BOUND")
        self.assertEqual(r["service"], "Platform Services")
        self.assertEqual(r["health_state"], "HEALTHY")
        self.assertEqual(r["effect"], "READ_ONLY")
        self.assertTrue(r["f4g_authorized"])

    def test_13_platform_health_unallowlisted_authority_refuses(self):
        cls = make_platform_class(
            "aletheus.platform.application_runtime",
            "ApplicationRuntime",
            "health",
            {"health_state": "HEALTHY"},
        )
        r = self.coordinator.bind(
            service="Platform Services",
            capability="health",
            f4g_authorization=auth("Platform Services", "health"),
            producer=cls(),
            authority="aletheus.fake.Runtime.health",
            observed_at="2026-08-25T18:30:00-05:00",
            observation_source="platform.existing-runtime",
        )
        self.assertEqual(r["status"], "REFUSED")

    def test_14_platform_health_invalid_state_refuses(self):
        cls = make_platform_class(
            "aletheus.platform.application_runtime",
            "ApplicationRuntime",
            "health",
            {"health_state": "BROKEN"},
        )
        r = self.coordinator.bind(
            service="Platform Services",
            capability="health",
            f4g_authorization=auth("Platform Services", "health"),
            producer=cls(),
            authority=(
                "aletheus.platform.application_runtime."
                "ApplicationRuntime.health"
            ),
            observed_at="2026-08-25T18:30:00-05:00",
            observation_source="platform.existing-runtime",
        )
        self.assertEqual(r["status"], "REFUSED")
        self.assertEqual(r["health_state"], "UNKNOWN")

    def test_15_platform_missing_timestamp_refuses(self):
        cls = make_platform_class(
            "aletheus.platform.application_runtime",
            "ApplicationRuntime",
            "health",
            {"health_state": "HEALTHY"},
        )
        r = self.coordinator.bind(
            service="Platform Services",
            capability="health",
            f4g_authorization=auth("Platform Services", "health"),
            producer=cls(),
            authority=(
                "aletheus.platform.application_runtime."
                "ApplicationRuntime.health"
            ),
            observed_at="",
            observation_source="platform.existing-runtime",
        )
        self.assertEqual(r["status"], "REFUSED")

    def test_16_platform_telemetry_exact_authority_binds(self):
        cls = make_platform_class(
            "aletheus.platform.contracts.service",
            "PlatformService",
            "metrics",
            {"requests": 3, "health_state": "HEALTHY"},
        )
        r = self.coordinator.bind(
            service="Platform Services",
            capability="telemetry",
            f4g_authorization=auth("Platform Services", "telemetry"),
            producer=cls(),
            authority=(
                "aletheus.platform.contracts.service."
                "PlatformService.metrics"
            ),
            observed_at="2026-08-25T18:30:00-05:00",
            observation_source="platform.existing-runtime",
            telemetry_payload_schema="aletheus.platform.telemetry.v1",
        )
        self.assertEqual(r["status"], "BOUND")
        self.assertEqual(r["capability"], "telemetry")
        self.assertEqual(r["effect"], "READ_ONLY")

    def test_17_platform_telemetry_missing_schema_refuses(self):
        cls = make_platform_class(
            "aletheus.platform.contracts.service",
            "PlatformService",
            "metrics",
            {"requests": 3},
        )
        r = self.coordinator.bind(
            service="Platform Services",
            capability="telemetry",
            f4g_authorization=auth("Platform Services", "telemetry"),
            producer=cls(),
            authority=(
                "aletheus.platform.contracts.service."
                "PlatformService.metrics"
            ),
            observed_at="2026-08-25T18:30:00-05:00",
            observation_source="platform.existing-runtime",
            telemetry_payload_schema="",
        )
        self.assertEqual(r["status"], "REFUSED")

    def test_18_a3ye_health_exact_authority_binds(self):
        obs = build_service_observation(
            binding.A3YE_AUTHORITY_MODULE, healthy=True, telemetry=True
        )
        r = self.coordinator.bind(
            service="A3ye",
            capability="health",
            f4g_authorization=auth("A3ye", "health"),
            observation=obs,
            activity="focused",
        )
        self.assertEqual(r["status"], "BOUND")
        self.assertEqual(r["authority"], binding.A3YE_AUTHORITY_PATH)
        self.assertEqual(r["service"], "A3ye")
        self.assertEqual(r["health_state"], "HEALTHY")

    def test_19_a3ye_telemetry_exact_authority_binds(self):
        obs = build_service_observation(
            binding.A3YE_AUTHORITY_MODULE, healthy=True, telemetry=True
        )
        r = self.coordinator.bind(
            service="A3ye",
            capability="telemetry",
            f4g_authorization=auth("A3ye", "telemetry"),
            observation=obs,
        )
        self.assertEqual(r["status"], "BOUND")
        self.assertEqual(r["authority"], binding.A3YE_AUTHORITY_PATH)

    def test_20_a3ye_foreign_observation_refuses(self):
        class Fake:
            pass
        r = self.coordinator.bind(
            service="A3ye",
            capability="health",
            f4g_authorization=auth("A3ye", "health"),
            observation=Fake(),
        )
        self.assertEqual(r["status"], "REFUSED")

    def test_21_mammoth_health_exact_authority_binds(self):
        obs = build_service_observation(
            binding.MAMMOTH_AUTHORITY_MODULE, healthy=True, telemetry=True
        )
        r = self.coordinator.bind(
            service="Mammoth",
            capability="health",
            f4g_authorization=auth("Mammoth", "health"),
            observation=obs,
            activity="engaged",
        )
        self.assertEqual(r["status"], "BOUND")
        self.assertEqual(r["authority"], binding.MAMMOTH_AUTHORITY_PATH)
        self.assertEqual(r["service"], "Mammoth")
        self.assertEqual(r["health_state"], "HEALTHY")

    def test_22_mammoth_telemetry_exact_authority_binds(self):
        obs = build_service_observation(
            binding.MAMMOTH_AUTHORITY_MODULE, healthy=True, telemetry=True
        )
        r = self.coordinator.bind(
            service="Mammoth",
            capability="telemetry",
            f4g_authorization=auth("Mammoth", "telemetry"),
            observation=obs,
        )
        self.assertEqual(r["status"], "BOUND")
        self.assertEqual(r["authority"], binding.MAMMOTH_AUTHORITY_PATH)

    def test_23_mammoth_degraded_projects_degraded(self):
        obs = build_service_observation(
            binding.MAMMOTH_AUTHORITY_MODULE, healthy=False, telemetry=True
        )
        r = self.coordinator.bind(
            service="Mammoth",
            capability="health",
            f4g_authorization=auth("Mammoth", "health"),
            observation=obs,
            activity="engaged",
        )
        self.assertEqual(r["status"], "BOUND")
        self.assertEqual(r["health_state"], "DEGRADED")
        self.assertEqual(r["f4h_state"], "degraded")

    def test_24_refusal_never_reports_healthy(self):
        r = self.coordinator.bind(
            service="Mammoth",
            capability="health",
            f4g_authorization=auth("Mammoth", "health"),
            observation=None,
        )
        self.assertEqual(r["status"], "REFUSED")
        self.assertNotEqual(r["health_state"], "HEALTHY")

    def test_25_all_generic_contracts_are_read_only_and_f4g_required(self):
        for service in binding.SERVICES:
            for capability in binding.CAPABILITIES:
                r = binding.foundation.resolve_contract(service, capability)
                self.assertEqual(r["status"], "RESOLVED")
                self.assertEqual(r["effect"], "READ_ONLY")
                self.assertTrue(r["f4g_required"])
                self.assertTrue(r["allow_is_not_direct_execution"])
                self.assertFalse(r["direct_execution_performed"])

    def test_26_platform_allowlist_counts_are_exact(self):
        self.assertEqual(len(binding.PLATFORM_HEALTH_AUTHORITIES), 9)
        self.assertEqual(len(binding.PLATFORM_TELEMETRY_AUTHORITIES), 11)

    def test_27_manifest_pins_exact_service_authority_paths(self):
        m = binding.build_manifest()
        self.assertEqual(
            m["a3ye"]["runtime_producer_authority_path"],
            "aletheus/a3ye/runtime_observation.py",
        )
        self.assertEqual(
            m["mammoth"]["runtime_producer_authority_path"],
            "aletheus/mammoth/runtime_observation.py",
        )

    def test_28_manifest_excludes_nonruntime_authority_categories(self):
        m = binding.build_manifest()
        for key in (
            "test_files_are_runtime_producer_authority",
            "fixture_files_are_runtime_producer_authority",
            "documentation_is_runtime_producer_authority",
            "backup_files_are_runtime_producer_authority",
            "report_files_are_runtime_producer_authority",
        ):
            self.assertFalse(m[key], key)

    def test_29_manifest_forbids_liveness_transport_and_mutation(self):
        m = binding.build_manifest()
        for key in (
            "repository_evidence_is_liveness",
            "actual_process_liveness_established",
            "live_binding_performed",
            "process_liveness_probe",
            "network_transport",
            "http_endpoint",
            "websocket",
            "rpc",
            "socket_transport",
            "write_or_mutating_capability",
            "autonomous_action",
            "generalized_a3ye_command_execution",
            "generalized_mammoth_command_execution",
            "direct_ungated_subsystem_reach_through",
            "opus_runtime_binding",
            "protected_mc84f4i_visual_change",
        ):
            self.assertFalse(m[key], key)

    def test_30_manifest_is_byte_reproducible(self):
        first = json.dumps(
            binding.build_manifest(), indent=2, sort_keys=True
        ) + "\n"
        second = json.dumps(
            binding.build_manifest(), indent=2, sort_keys=True
        ) + "\n"
        self.assertEqual(first, second)
        if EXPECTED_MANIFEST:
            self.assertEqual(
                first,
                Path(EXPECTED_MANIFEST).read_text(encoding="utf-8"),
            )

    def test_31_binding_receipt_explicitly_denies_liveness_claim(self):
        cls = make_platform_class(
            "aletheus.platform.application_runtime",
            "ApplicationRuntime",
            "health",
            {"health_state": "HEALTHY"},
        )
        r = self.coordinator.bind(
            service="Platform Services",
            capability="health",
            f4g_authorization=auth("Platform Services", "health"),
            producer=cls(),
            authority=(
                "aletheus.platform.application_runtime."
                "ApplicationRuntime.health"
            ),
            observed_at="2026-08-25T18:30:00-05:00",
            observation_source="platform.existing-runtime",
        )
        self.assertEqual(r["status"], "BOUND")
        self.assertFalse(r["repository_evidence_is_liveness"])
        self.assertFalse(r["actual_process_liveness_established"])
        self.assertFalse(r["live_binding_performed"])

    def test_32_platform_producer_with_required_args_refuses(self):
        def health(self, required):
            return {"health_state": "HEALTHY"}
        health.__name__ = "health"
        health.__qualname__ = "ApplicationRuntime.health"
        health.__module__ = "aletheus.platform.application_runtime"
        cls = type("ApplicationRuntime", (), {"health": health})
        cls.__module__ = "aletheus.platform.application_runtime"
        cls.__qualname__ = "ApplicationRuntime"
        r = self.coordinator.bind(
            service="Platform Services",
            capability="health",
            f4g_authorization=auth("Platform Services", "health"),
            producer=cls(),
            authority=(
                "aletheus.platform.application_runtime."
                "ApplicationRuntime.health"
            ),
            observed_at="2026-08-25T18:30:00-05:00",
            observation_source="platform.existing-runtime",
        )
        self.assertEqual(r["status"], "REFUSED")

    def test_33_manifest_has_no_runtime_instantiation(self):
        m = binding.build_manifest()
        self.assertFalse(
            m["platform_services"]["runtime_instantiation_performed"]
        )
        self.assertTrue(
            m["platform_services"]["producer_instances_are_caller_supplied"]
        )


if __name__ == "__main__":
    unittest.main()
