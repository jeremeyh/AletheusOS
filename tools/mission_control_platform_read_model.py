#!/usr/bin/env python3
"""Generate the bounded Mission Control platform read model.

The caller must supply an explicit baseline commit. Ambient repository HEAD is
never used as the generated model's constitutional baseline.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

SCHEMA = "aletheusos.mission-control-platform-read-model.v1"

SERVICE_DEFINITIONS = {
    "Platform Services": {
        "contract_id": "platform-services.inspect.v1",
        "adapter_id": "platform-services.repository-read-model.v1",
        "evidence_paths": [
            "aletheus/runtime/core.py",
            "aletheus/platform/contracts/service.py",
            "tools/runtime_backbone.py",
        ],
    },
    "A3ye": {
        "contract_id": "a3ye.inspect.v1",
        "adapter_id": "a3ye.repository-read-model.v1",
        "evidence_paths": [
            "aletheus/a3ye/council_bridge/cli.py",
            "aletheus/a3ye/core/cli.py",
        ],
    },
    "Mammoth": {
        "contract_id": "mammoth.inspect.v1",
        "adapter_id": "mammoth.repository-read-model.v1",
        "evidence_paths": [
            "aletheus/institutional_civilization/civilization_catalog.py",
            "aletheus/institutional_civilization/catalog.py",
        ],
    },
}


def run_git(repo: Path, *args: str) -> str:
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


def resolve_exact_commit(repo: Path, baseline_commit: str) -> str:
    candidate = baseline_commit.strip()
    if len(candidate) != 40 or any(ch not in "0123456789abcdefABCDEF" for ch in candidate):
        raise RuntimeError("baseline commit must be an exact 40-character hexadecimal commit id")
    resolved = run_git(repo, "rev-parse", "--verify", f"{candidate}^{{commit}}")
    if resolved.lower() != candidate.lower():
        raise RuntimeError("baseline commit did not resolve to the exact supplied commit id")
    return resolved.lower()


def is_tracked(repo: Path, rel: str) -> bool:
    run = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "--error-unmatch", rel],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return run.returncode == 0


def evidence(repo: Path, rel: str) -> dict:
    path = repo / rel
    if not path.is_file():
        raise RuntimeError(f"missing evidence path: {rel}")
    if not is_tracked(repo, rel):
        raise RuntimeError(f"untracked evidence path: {rel}")
    if run_git(repo, "status", "--porcelain=v1", "--", rel) != "":
        raise RuntimeError(f"dirty evidence path: {rel}")
    data = path.read_bytes()
    return {
        "path": rel,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "tracked": True,
        "clean": True,
    }


def build_model(repo: Path, baseline_commit: str) -> dict:
    repo = repo.resolve()
    pinned_baseline = resolve_exact_commit(repo, baseline_commit)

    services = {}
    for name, definition in SERVICE_DEFINITIONS.items():
        records = [evidence(repo, p) for p in definition["evidence_paths"]]
        services[name] = {
            "contract": {
                "id": definition["contract_id"],
                "version": "1.0.0",
                "surface": name,
                "capability": "inspect",
                "effect": "READ_ONLY",
                "adapter_id": definition["adapter_id"],
            },
            "adapter": {
                "id": definition["adapter_id"],
                "version": "1.0.0",
                "kind": "REPOSITORY_READ_MODEL",
                "direct_subsystem_execution": False,
                "network_transport": False,
            },
            "read_model": {
                "status": "AVAILABLE_FOR_INSPECTION",
                "health_semantics": "TRACKED_IMPLEMENTATION_EVIDENCE_NOT_PROCESS_LIVENESS",
                "implementation_evidence": records,
                "evidence_count": len(records),
            },
        }

    return {
        "schema": SCHEMA,
        "baseline_commit": pinned_baseline,
        "capability": "inspect",
        "effect": "READ_ONLY",
        "f4g_gate_required": True,
        "allow_is_not_direct_execution": True,
        "unknown_contract_adapter_or_service_refuses": True,
        "network_transport_present": False,
        "write_or_mutating_execution_authorized": False,
        "a3ye_general_command_execution_authorized": False,
        "opus_runtime_binding": "DEFERRED_PENDING_CONCRETE_RUNTIME_CONTRACT",
        "services": services,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--baseline-commit", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    payload = json.dumps(
        build_model(Path(args.repo), args.baseline_commit),
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
