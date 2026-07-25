from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError(
                "Unable to locate repository root."
            )

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)

MANIFEST = (
    ROOT
    / "nimble"
    / "governance"
    / "supply-chain"
    / "dependency-manifest.json"
)

POLICY = (
    ROOT
    / "nimble"
    / "governance"
    / "supply-chain"
    / "dependency-policy.json"
)

EXCEPTIONS = (
    ROOT
    / "nimble"
    / "governance"
    / "supply-chain"
    / "dependency-exceptions.json"
)

LATEST_JSON = (
    ROOT
    / "reports"
    / "nimble"
    / "dependency-risk-latest.json"
)

LATEST_MARKDOWN = (
    ROOT
    / "reports"
    / "nimble"
    / "dependency-risk-latest.md"
)

NIMBLE_ROOT = ROOT / "nimble"


def load_json(
    path: Path,
) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required file is missing: "
            f"{path.relative_to(ROOT)}"
        )

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def run_json_command(
    command: list[str],
    *,
    cwd: Path = ROOT,
) -> tuple[int, dict[str, Any] | None, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=dict(os.environ),
        )
    except FileNotFoundError as error:
        return 127, None, str(error)

    output = completed.stdout

    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        payload = None

    return completed.returncode, payload, output


def normalize_license(
    value: Any,
) -> str:
    if value is None:
        return "unknown"

    text = str(value).strip()

    if not text:
        return "unknown"

    return text


def classify_licenses(
    manifest: dict[str, Any],
    policy: dict[str, Any],
) -> dict[str, Any]:
    allowed = set(
        policy["licenses"]["allowed"]
    )
    review_required = set(
        policy["licenses"]["review_required"]
    )
    denied = set(
        policy["licenses"]["denied"]
    )

    results: list[dict[str, str]] = []

    inventories = [
        (
            "npm",
            manifest["npm"]["resolved_packages"],
        ),
        (
            "python",
            manifest["python"]["installed_packages"],
        ),
    ]

    for ecosystem, packages in inventories:
        for package in packages:
            license_name = normalize_license(
                package.get("license")
            )

            if license_name in denied:
                classification = "denied"
            elif license_name in allowed:
                classification = "allowed"
            elif license_name in review_required:
                classification = "review_required"
            else:
                classification = "review_required"

            results.append(
                {
                    "ecosystem": ecosystem,
                    "name": package["name"],
                    "version": package["version"],
                    "license": license_name,
                    "classification": classification,
                }
            )

    return {
        "allowed": [
            item
            for item in results
            if item["classification"] == "allowed"
        ],
        "review_required": [
            item
            for item in results
            if item["classification"] == "review_required"
        ],
        "denied": [
            item
            for item in results
            if item["classification"] == "denied"
        ],
        "all": results,
    }


def load_active_exceptions() -> list[dict[str, Any]]:
    if not EXCEPTIONS.exists():
        return []

    registry = load_json(EXCEPTIONS)

    return [
        item
        for item in registry.get(
            "exceptions",
            [],
        )
        if item.get("status") == "active"
    ]


def exception_matches(
    exception: dict[str, Any],
    *,
    ecosystem: str,
    package: str,
    version: str,
    exception_type: str,
    subject: str,
) -> bool:
    return (
        exception.get("ecosystem") == ecosystem
        and exception.get("package") == package
        and exception.get("version") == version
        and exception.get("exception_type")
        == exception_type
        and exception.get("subject") == subject
    )


def collect_npm_audit() -> dict[str, Any]:
    return_code, payload, output = run_json_command(
        [
            "npm",
            "audit",
            "--json",
            "--omit=dev",
        ],
        cwd=NIMBLE_ROOT,
    )

    if payload is None:
        return {
            "available": False,
            "return_code": return_code,
            "error": output.strip(),
            "counts": {},
            "vulnerabilities": [],
        }

    metadata = payload.get(
        "metadata",
        {},
    )

    counts = metadata.get(
        "vulnerabilities",
        {},
    )

    vulnerabilities = []

    for name, record in payload.get(
        "vulnerabilities",
        {},
    ).items():
        vulnerabilities.append(
            {
                "name": name,
                "severity": record.get(
                    "severity",
                    "unknown",
                ),
                "is_direct": bool(
                    record.get("isDirect", False)
                ),
                "via": record.get("via", []),
                "range": record.get("range"),
                "fix_available": record.get(
                    "fixAvailable"
                ),
            }
        )

    return {
        "available": True,
        "return_code": return_code,
        "counts": counts,
        "vulnerabilities": vulnerabilities,
    }


def collect_python_audit() -> dict[str, Any]:
    import tempfile

    with tempfile.TemporaryDirectory(
        prefix="nimble-pip-audit-"
    ) as temporary_directory:
        output_path = (
            Path(temporary_directory)
            / "pip-audit.json"
        )

        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip_audit",
                    "--format",
                    "json",
                    "--output",
                    str(output_path),
                ],
                cwd=ROOT,
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=dict(os.environ),
            )
        except FileNotFoundError as error:
            return {
                "available": False,
                "return_code": 127,
                "error": str(error),
                "dependencies": [],
                "vulnerability_count": 0,
            }

        console_output = completed.stdout.strip()

        if not output_path.exists():
            return {
                "available": False,
                "return_code": completed.returncode,
                "error": (
                    console_output
                    or "pip-audit did not create its JSON output file."
                ),
                "dependencies": [],
                "vulnerability_count": 0,
            }

        try:
            payload = json.loads(
                output_path.read_text(
                    encoding="utf-8"
                )
            )
        except json.JSONDecodeError as error:
            return {
                "available": False,
                "return_code": completed.returncode,
                "error": (
                    "pip-audit produced invalid JSON: "
                    f"{error}. Console output: "
                    f"{console_output}"
                ),
                "dependencies": [],
                "vulnerability_count": 0,
            }

        if isinstance(payload, list):
            dependencies = payload
        elif isinstance(payload, dict):
            dependencies = payload.get(
                "dependencies",
                [],
            )
        else:
            return {
                "available": False,
                "return_code": completed.returncode,
                "error": (
                    "pip-audit returned an unsupported "
                    "JSON payload type."
                ),
                "dependencies": [],
                "vulnerability_count": 0,
            }

        if not isinstance(dependencies, list):
            return {
                "available": False,
                "return_code": completed.returncode,
                "error": (
                    "pip-audit dependencies field "
                    "is not an array."
                ),
                "dependencies": [],
                "vulnerability_count": 0,
            }

        vulnerability_count = sum(
            len(item.get("vulns", []))
            for item in dependencies
            if isinstance(item, dict)
        )

        return {
            "available": True,
            "return_code": completed.returncode,
            "console_output": console_output,
            "dependencies": dependencies,
            "vulnerability_count": vulnerability_count,
        }


def evaluate_npm_vulnerabilities(
    audit: dict[str, Any],
    policy: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if not audit["available"]:
        return failures

    maximum = policy[
        "vulnerabilities"
    ][
        "maximum_accepted"
    ]

    for severity, limit in maximum.items():
        current = int(
            audit["counts"].get(
                severity,
                0,
            )
        )

        if current > int(limit):
            failures.append(
                f"npm {severity} vulnerabilities: "
                f"{current} exceeds {limit}"
            )

    return failures


def write_markdown(
    report: dict[str, Any],
) -> None:
    licenses = report["licenses"]
    npm_audit = report["npm_audit"]
    python_audit = report["python_audit"]

    lines = [
        "# Nimble Dependency Risk Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Status: **{report['status']}**",
        "",
        "## License policy",
        "",
        (
            "- Allowed packages: "
            f"`{len(licenses['allowed'])}`"
        ),
        (
            "- Review required: "
            f"`{len(licenses['review_required'])}`"
        ),
        (
            "- Denied packages: "
            f"`{len(licenses['denied'])}`"
        ),
        "",
        "## Vulnerability scanning",
        "",
        (
            "- npm audit available: "
            f"`{npm_audit['available']}`"
        ),
        (
            "- pip-audit available: "
            f"`{python_audit['available']}`"
        ),
    ]

    if npm_audit["available"]:
        lines.extend(
            [
                (
                    "- npm critical: "
                    f"`{npm_audit['counts'].get('critical', 0)}`"
                ),
                (
                    "- npm high: "
                    f"`{npm_audit['counts'].get('high', 0)}`"
                ),
                (
                    "- npm moderate: "
                    f"`{npm_audit['counts'].get('moderate', 0)}`"
                ),
            ]
        )

    if python_audit["available"]:
        lines.append(
            
                "- Python vulnerabilities: "
                f"`{python_audit['vulnerability_count']}`"
            
        )

    if licenses["denied"]:
        lines.extend(
            [
                "",
                "## Denied licenses",
                "",
                "| Ecosystem | Package | Version | License |",
                "|---|---|---|---|",
            ]
        )

        for item in licenses["denied"]:
            lines.append(
                f"| {item['ecosystem']} "
                f"| `{item['name']}` "
                f"| `{item['version']}` "
                f"| `{item['license']}` |"
            )

    if licenses["review_required"]:
        lines.extend(
            [
                "",
                "## License review queue",
                "",
                "| Ecosystem | Package | Version | License |",
                "|---|---|---|---|",
            ]
        )

        for item in licenses["review_required"]:
            lines.append(
                f"| {item['ecosystem']} "
                f"| `{item['name']}` "
                f"| `{item['version']}` "
                f"| `{item['license']}` |"
            )

    if report["failures"]:
        lines.extend(
            [
                "",
                "## Failures",
                "",
            ]
        )

        for failure in report["failures"]:
            lines.append(f"- {failure}")

    LATEST_MARKDOWN.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    manifest = load_json(MANIFEST)
    policy = load_json(POLICY)

    licenses = classify_licenses(
        manifest,
        policy,
    )

    npm_audit = collect_npm_audit()
    python_audit = collect_python_audit()

    failures: list[str] = []
    active_exceptions = load_active_exceptions()
    applied_exceptions: list[dict[str, Any]] = []

    for item in licenses["denied"]:
        matching = next(
            (
                exception
                for exception in active_exceptions
                if exception_matches(
                    exception,
                    ecosystem=item["ecosystem"],
                    package=item["name"],
                    version=item["version"],
                    exception_type="license_review",
                    subject=item["license"],
                )
            ),
            None,
        )

        if matching is not None:
            applied_exceptions.append(matching)
            continue

        failures.append(
            "Denied license: "
            f"{item['ecosystem']} "
            f"{item['name']}@{item['version']} "
            f"uses {item['license']}"
        )

    failures.extend(
        evaluate_npm_vulnerabilities(
            npm_audit,
            policy,
        )
    )

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            UTC
        ).isoformat(),
        "status": (
            "PASS"
            if not failures
            else "FAIL"
        ),
        "policy": {
            "path": str(
                POLICY.relative_to(ROOT)
            ),
        },
        "manifest": {
            "path": str(
                MANIFEST.relative_to(ROOT)
            ),
        },
        "licenses": licenses,
        "npm_audit": npm_audit,
        "python_audit": python_audit,
        "exceptions": {
            "active_count": len(active_exceptions),
            "applied": applied_exceptions,
        },
        "failures": failures,
    }

    LATEST_JSON.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    write_markdown(report)

    print("=" * 72)
    print("NIMBLE™ DEPENDENCY RISK GOVERNANCE")
    print("=" * 72)
    print(
        "Allowed licenses:",
        len(licenses["allowed"]),
    )
    print(
        "Review required:",
        len(licenses["review_required"]),
    )
    print(
        "Denied licenses:",
        len(licenses["denied"]),
    )
    print(
        "npm audit:",
        (
            "available"
            if npm_audit["available"]
            else "unavailable"
        ),
    )
    print(
        "pip-audit:",
        (
            "available"
            if python_audit["available"]
            else "unavailable"
        ),
    )

    for failure in failures:
        print("FAIL:", failure)

    print("Status:", report["status"])

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
