from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)


DOCKERFILE = ROOT / "Dockerfile.nimble"
DOCKERIGNORE = ROOT / ".dockerignore"
COMPOSE = ROOT / "compose.nimble.yml"

CONTRACT = ROOT / "nimble" / "governance" / "deployment" / "container-contract.json"

REPORT = ROOT / "reports" / "nimble" / "container-contract-latest.json"

REQUIRED_DOCKERFILE_MARKERS = (
    "FROM node:24-alpine AS frontend-builder",
    "FROM python:3.14-slim AS runtime",
    "npm ci",
    "npm run build",
    "python -m pip install .",
    "USER aletheus",
    "EXPOSE 8000",
    "HEALTHCHECK",
    "aletheus.experience_gateway.fastapi_app:app",
)

REQUIRED_DOCKERIGNORE_MARKERS = (
    ".git",
    ".venv",
    ".runtime",
    "node_modules",
    "reports",
)

REQUIRED_COMPOSE_MARKERS = (
    "Dockerfile.nimble",
    "read_only: true",
    "no-new-privileges:true",
    "cap_drop:",
    "- ALL",
    "/healthz",
    "/readyz",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def missing_markers(
    text: str,
    markers: tuple[str, ...],
) -> list[str]:
    return [marker for marker in markers if marker not in text]


def main() -> int:
    failures: list[str] = []

    for path in (
        DOCKERFILE,
        DOCKERIGNORE,
        COMPOSE,
        CONTRACT,
    ):
        if not path.exists():
            failures.append(f"Missing container artifact: {path.relative_to(ROOT)}")

    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1

    dockerfile_text = DOCKERFILE.read_text(encoding="utf-8")

    dockerignore_text = DOCKERIGNORE.read_text(encoding="utf-8")

    compose_text = COMPOSE.read_text(encoding="utf-8")

    for marker in missing_markers(
        dockerfile_text,
        REQUIRED_DOCKERFILE_MARKERS,
    ):
        failures.append(f"Dockerfile marker missing: {marker}")

    for marker in missing_markers(
        dockerignore_text,
        REQUIRED_DOCKERIGNORE_MARKERS,
    ):
        failures.append(f".dockerignore marker missing: {marker}")

    for marker in missing_markers(
        compose_text,
        REQUIRED_COMPOSE_MARKERS,
    ):
        failures.append(f"Compose marker missing: {marker}")

    contract = load_json(CONTRACT)

    runtime = contract.get("runtime", {})
    startup = contract.get("startup", {})
    health = contract.get("health", {})

    if runtime.get("user") == "root":
        failures.append("Container runtime user must not be root.")

    if runtime.get("port") != 8000:
        failures.append("Container runtime port must be 8000.")

    if not runtime.get("read_only_root_filesystem"):
        failures.append("Read-only root filesystem is required.")

    if not runtime.get("drop_all_capabilities"):
        failures.append("All Linux capabilities must be dropped.")

    if not runtime.get("no_new_privileges"):
        failures.append("no-new-privileges is required.")

    if startup.get("module") != ("aletheus.experience_gateway.fastapi_app:app"):
        failures.append("Container startup module is incorrect.")

    for key in (
        "liveness_path",
        "readiness_path",
    ):
        value = health.get(key, "")

        if not re.fullmatch(
            r"/[A-Za-z0-9/_-]+",
            value,
        ):
            failures.append(f"Invalid health path: {key}={value}")

    report = {
        "schema_version": "1.0",
        "status": ("PASS" if not failures else "FAIL"),
        "dockerfile": str(DOCKERFILE.relative_to(ROOT)),
        "compose": str(COMPOSE.relative_to(ROOT)),
        "runtime_user": runtime.get("user"),
        "port": runtime.get("port"),
        "failures": failures,
    }

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ CONTAINER CONTRACT")
    print("=" * 72)
    print("Runtime user:", report["runtime_user"])
    print("Port:", report["port"])

    for failure in failures:
        print("FAIL:", failure)

    print("Status:", report["status"])

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
