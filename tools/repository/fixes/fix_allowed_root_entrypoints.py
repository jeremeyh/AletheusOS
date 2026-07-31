#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
POLICY = ROOT / "config" / "repository_policy.json"

if not POLICY.exists():
    raise SystemExit(f"Policy file not found: {POLICY}")

backup = POLICY.with_suffix(".json.bak")
shutil.copy2(POLICY, backup)

with POLICY.open("r", encoding="utf-8") as f:
    policy = json.load(f)

policy["allowed_root_entrypoints"] = [
    "app.py",
    "run.py",
    "manage.py",
    "conftest.py",
    "run_aletheus_founder_console.py",
    "run_aletheus_system_test.sh",
    "run_repository_self_repair.sh",
    "append_nimble_audit_event.py",
    "collect_nimble_production_telemetry.py",
    "generate_nimble_dependency_manifest.py",
    "generate_nimble_release_attestation.py",
    "plan_nimble_audit_recovery.py",
    "promote_nimble_performance_baseline.py",
    "reconcile_nimble_dependency_exceptions.py",
    "scan_nimble_dependency_risk.py",
    "test_nimble_audit_ledger_tamper.py",
    "validate_nimble_baseline_governance.py",
    "validate_nimble_container_contract.py",
    "validate_nimble_credential_isolation.py",
    "validate_nimble_credential_rotation.py",
    "validate_nimble_dependency_exceptions.py",
    "validate_nimble_dependency_manifest.py",
    "validate_nimble_dependency_risk.py",
    "validate_nimble_experience_core.py",
    "validate_nimble_instrumentation_preview.py",
    "validate_nimble_performance_regression.py",
    "validate_nimble_primitive_experience.py",
    "validate_nimble_provider_preflight.py",
    "validate_nimble_release_attestation.py",
    "validate_nimble_workspace_engine.py",
]

with POLICY.open("w", encoding="utf-8") as f:
    json.dump(policy, f, indent=2)
    f.write("\n")

print("✓ Updated allowed_root_entrypoints")
print(f"✓ Backup written to: {backup}")
