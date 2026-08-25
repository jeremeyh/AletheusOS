import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


class RuntimeHealthTelemetryContractFoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = Path(os.environ.get("ALETHEUSOS_REPO", Path(__file__).resolve().parents[1]))
        module_path = Path(
            os.environ.get(
                "ALETHEUSOS_RUNTIME_OBSERVATION_MODULE",
                cls.repo / "aletheus/platform/contracts/runtime_observation.py",
            )
        )
        spec = importlib.util.spec_from_file_location("runtime_observation_foundation", module_path)
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        cls.m = module

    def resolution(self, service="Platform Services", capability="health"):
        return self.m.resolve_contract(service, capability)

    def test_exact_service_and_capability_registry(self):
        self.assertEqual(set(self.m.SERVICE_REGISTRY), {"Platform Services", "A3ye", "Mammoth"})
        for service in self.m.SERVICE_REGISTRY:
            self.assertEqual(set(self.m.SERVICE_REGISTRY[service]["contracts"]), {"health", "telemetry"})

    def test_unknown_service_refuses(self):
        self.assertEqual(self.resolution("Opus")["status"], "REFUSED")
        self.assertEqual(self.resolution("Unknown")["failure_reason"], "UNKNOWN_SERVICE")

    def test_unknown_capability_refuses(self):
        result = self.resolution("Platform Services", "execute")
        self.assertEqual(result["status"], "REFUSED")
        self.assertEqual(result["failure_reason"], "UNKNOWN_CAPABILITY")

    def test_unknown_contract_refuses_health_receipt(self):
        r = self.m.build_health_receipt(
            service="Platform Services",
            contract_id="wrong.contract",
            adapter_id="platform-services.runtime-observation.v1",
            observed_at="2026-08-24T22:00:00-05:00",
            observation_source="unit-test",
            health_state="HEALTHY",
        )
        self.assertEqual(r["status"], "REFUSED")
        self.assertEqual(r["health_state"], "UNKNOWN")

    def test_unknown_adapter_refuses_health_receipt(self):
        r = self.m.build_health_receipt(
            service="Platform Services",
            contract_id="platform-services.health.v1",
            adapter_id="wrong.adapter",
            observed_at="2026-08-24T22:00:00-05:00",
            observation_source="unit-test",
            health_state="HEALTHY",
        )
        self.assertEqual(r["status"], "REFUSED")
        self.assertEqual(r["health_state"], "UNKNOWN")

    def test_valid_health_receipt_is_read_only(self):
        r = self.m.build_health_receipt(
            service="Platform Services",
            contract_id="platform-services.health.v1",
            adapter_id="platform-services.runtime-observation.v1",
            observed_at="2026-08-24T22:00:00-05:00",
            observation_source="unit-test",
            health_state="HEALTHY",
        )
        self.assertEqual(r["status"], "ACCEPTED")
        self.assertEqual(r["health_state"], "HEALTHY")
        self.assertEqual(r["effect"], "READ_ONLY")
        self.assertFalse(r["network_transport_performed"])
        self.assertFalse(r["mutation_performed"])
        self.assertFalse(r["direct_execution_performed"])

    def test_missing_timestamp_can_never_report_healthy(self):
        r = self.m.build_health_receipt(
            service="Platform Services",
            contract_id="platform-services.health.v1",
            adapter_id="platform-services.runtime-observation.v1",
            observed_at="",
            observation_source="unit-test",
            health_state="HEALTHY",
        )
        self.assertEqual(r["status"], "REFUSED")
        self.assertEqual(r["health_state"], "UNKNOWN")

    def test_invalid_health_state_refuses(self):
        r = self.m.build_health_receipt(
            service="A3ye",
            contract_id="a3ye.health.v1",
            adapter_id="a3ye.runtime-observation.v1",
            observed_at="2026-08-24T22:00:00-05:00",
            observation_source="unit-test",
            health_state="PERFECT",
        )
        self.assertEqual(r["status"], "REFUSED")
        self.assertEqual(r["health_state"], "UNKNOWN")

    def test_valid_telemetry_receipt_requires_schema(self):
        r = self.m.build_telemetry_receipt(
            service="Mammoth",
            contract_id="mammoth.telemetry.v1",
            adapter_id="mammoth.runtime-observation.v1",
            observed_at="2026-08-24T22:00:00-05:00",
            observation_source="unit-test",
            health_state="HEALTHY",
            telemetry_payload_schema="aletheus.mammoth.telemetry.test.v1",
            telemetry_payload={"objects": 12},
        )
        self.assertEqual(r["status"], "ACCEPTED")
        self.assertEqual(r["telemetry_payload"]["objects"], 12)
        self.assertEqual(r["effect"], "READ_ONLY")

    def test_missing_telemetry_schema_refuses(self):
        r = self.m.build_telemetry_receipt(
            service="Mammoth",
            contract_id="mammoth.telemetry.v1",
            adapter_id="mammoth.runtime-observation.v1",
            observed_at="2026-08-24T22:00:00-05:00",
            observation_source="unit-test",
            health_state="HEALTHY",
            telemetry_payload_schema="",
            telemetry_payload={"objects": 12},
        )
        self.assertEqual(r["status"], "REFUSED")
        self.assertEqual(r["health_state"], "UNKNOWN")

    def test_non_healthy_always_projects_degraded(self):
        for state in ("DEGRADED", "UNAVAILABLE", "UNKNOWN"):
            for activity in ("idle", "focused", "engaged"):
                self.assertEqual(self.m.project_f4h_state(state, activity), "degraded")

    def test_healthy_preserves_valid_activity_state(self):
        for activity in ("idle", "focused", "engaged"):
            self.assertEqual(self.m.project_f4h_state("HEALTHY", activity), activity)
        self.assertEqual(self.m.project_f4h_state("HEALTHY", "invalid"), "degraded")

    def test_manifest_is_pinned_and_contains_no_live_binding(self):
        accepted = os.environ.get("ALETHEUSOS_ACCEPTED_BASELINE")
        inherited = os.environ.get("ALETHEUSOS_INHERITED_READ_MODEL_BASELINE")
        self.assertTrue(accepted)
        self.assertTrue(inherited)
        manifest = self.m.build_foundation_manifest(self.repo, accepted, inherited)
        self.assertEqual(manifest["accepted_platform_integration_baseline"], accepted)
        self.assertEqual(manifest["inherited_read_model_baseline"], inherited)
        self.assertFalse(manifest["network_transport_implementation_authorized"])
        self.assertFalse(manifest["live_probe_binding_authorized"])
        self.assertFalse(manifest["write_or_mutating_capabilities_authorized"])
        self.assertEqual(
            manifest["opus_runtime_binding"],
            "DEFERRED_PENDING_CONCRETE_RUNTIME_CONTRACT",
        )


if __name__ == "__main__":
    unittest.main()
