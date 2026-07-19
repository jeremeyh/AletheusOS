from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

REPORT = (
    ROOT
    / "reports"
    / "nimble"
    / "container-smoke-latest.json"
)

DEFAULT_IMAGE = (
    "aletheus/nimble-experience-gateway:local"
)


def run(
    command: list[str],
    *,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def request_json(
    url: str,
) -> tuple[int, dict[str, Any]]:
    with urllib.request.urlopen(
        url,
        timeout=3,
    ) as response:
        return (
            response.status,
            json.loads(
                response.read().decode("utf-8")
            ),
        )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--image",
        default=DEFAULT_IMAGE,
    )

    parser.add_argument(
        "--container-name",
        default="nimble-container-smoke",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=18000,
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=45,
    )

    parser.add_argument(
        "--require-runtime",
        action="store_true",
        help=(
            "Fail instead of skipping when Docker "
            "is unavailable."
        ),
    )

    arguments = parser.parse_args()

    docker_executable = shutil.which("docker")
    if docker_executable is None:
        strict = bool(arguments.require_runtime)

        report = {
            "schema_version": "1.0",
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "image": arguments.image,
            "status": "FAIL" if strict else "SKIP",
            "checks": [],
            "failures": (
                ["Docker runtime is unavailable."]
                if strict
                else []
            ),
            "skip_reason": (
                "Docker runtime is unavailable."
            ),
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
        print("NIMBLE™ CONTAINER SMOKE TEST")
        print("=" * 72)
        print("Docker runtime: unavailable")
        print("Status:", report["status"])

        return 1 if strict else 0

    container_name = arguments.container_name


    run(
        [
            "docker",
            "rm",
            "--force",
            container_name,
        ],
        check=False,
    )

    container_id = ""

    checks: list[dict[str, Any]] = []
    failures: list[str] = []

    try:
        started = run(
            [
                "docker",
                "run",
                "--detach",
                "--name",
                container_name,
                "--read-only",
                "--tmpfs",
                "/tmp:size=64m,mode=1777",
                "--tmpfs",
                "/app/runtime_state:size=64m,mode=0700",
                "--security-opt",
                "no-new-privileges:true",
                "--cap-drop",
                "ALL",
                "--publish",
                f"{arguments.port}:8000",
                "--env",
                "ALETHEUS_AUTH_MODE=local",
                arguments.image,
            ]
        )

        container_id = started.stdout.strip()

        deadline = time.monotonic() + arguments.timeout

        probe_specs = (
            ("/healthz", "alive"),
            ("/readyz", "ready"),
        )

        while time.monotonic() < deadline:
            try:
                collected: list[dict[str, Any]] = []

                for path, expected_state in probe_specs:
                    status, payload = request_json(
                        "http://127.0.0.1:"
                        f"{arguments.port}{path}"
                    )

                    passed = (
                        status == 200
                        and payload.get("status")
                        == expected_state
                    )

                    collected.append(
                        {
                            "path": path,
                            "http_status": status,
                            "reported_status":
                                payload.get("status"),
                            "expected_status":
                                expected_state,
                            "passed": passed,
                        }
                    )

                checks = collected

                if all(
                    check["passed"]
                    for check in checks
                ):
                    break
            except Exception:
                time.sleep(1)
        else:
            failures.append(
                "Container did not become ready "
                f"within {arguments.timeout} seconds."
            )

        for check in checks:
            if not check["passed"]:
                failures.append(
                    f"Probe failed: {check['path']}"
                )

        inspect_result = run(
            [
                "docker",
                "inspect",
                "--format",
                "{{.Config.User}}",
                container_name,
            ]
        )

        runtime_user = inspect_result.stdout.strip()

        if not runtime_user:
            failures.append(
                "Container has no explicit runtime user."
            )

        if runtime_user in {
            "root",
            "0",
            "0:0",
        }:
            failures.append(
                "Container is running as root."
            )

    except Exception as error:
        failures.append(
            f"{type(error).__name__}: {error}"
        )
        runtime_user = "unknown"
    finally:
        logs = run(
            [
                "docker",
                "logs",
                container_name,
            ],
            check=False,
        ).stdout

        run(
            [
                "docker",
                "rm",
                "--force",
                container_name,
            ],
            check=False,
        )

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "image": arguments.image,
        "container_id": container_id,
        "runtime_user": runtime_user,
        "status": (
            "PASS"
            if not failures
            else "FAIL"
        ),
        "checks": checks,
        "failures": failures,
        "logs": logs[-10000:],
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
    print("NIMBLE™ CONTAINER SMOKE TEST")
    print("=" * 72)
    print("Image:", report["image"])
    print("Runtime user:", report["runtime_user"])

    for check in checks:
        print(
            check["path"],
            "PASS"
            if check["passed"]
            else "FAIL",
        )

    for failure in failures:
        print("FAIL:", failure)

    print("Status:", report["status"])

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
