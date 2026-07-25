from __future__ import annotations

import json
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

REGISTRY = (
    ROOT
    / "nimble"
    / "governance"
    / "supply-chain"
    / "dependency-exceptions.json"
)

RISK_REPORT = (
    ROOT
    / "reports"
    / "nimble"
    / "dependency-risk-latest.json"
)

REPORT_JSON = (
    ROOT
    / "reports"
    / "nimble"
    / "dependency-exception-reconciliation-latest.json"
)

REPORT_MARKDOWN = (
    ROOT
    / "reports"
    / "nimble"
    / "dependency-exception-reconciliation-latest.md"
)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required file is missing: {path.relative_to(ROOT)}"
        )

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def normalize_subject(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()

    if value is None:
        return ""

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    )


def exception_key(
    item: dict[str, Any],
) -> tuple[str, str, str, str, str]:
    return (
        str(item.get("ecosystem", "")).strip(),
        str(item.get("package", "")).strip(),
        str(item.get("version", "")).strip(),
        str(item.get("exception_type", "")).strip(),
        normalize_subject(item.get("subject")),
    )


def risk_key(
    *,
    ecosystem: str,
    package: str,
    version: str,
    exception_type: str,
    subject: Any,
) -> tuple[str, str, str, str, str]:
    return (
        ecosystem.strip(),
        package.strip(),
        version.strip(),
        exception_type.strip(),
        normalize_subject(subject),
    )


def collect_current_risks(
    report: dict[str, Any],
) -> list[dict[str, Any]]:
    risks: list[dict[str, Any]] = []

    licenses = report.get("licenses", {})

    for item in licenses.get("review_required", []):
        risks.append(
            {
                "ecosystem": item["ecosystem"],
                "package": item["name"],
                "version": item["version"],
                "exception_type": "license_review",
                "subject": item["license"],
                "severity": "review",
                "source": "license_review_required",
            }
        )

    for item in licenses.get("denied", []):
        risks.append(
            {
                "ecosystem": item["ecosystem"],
                "package": item["name"],
                "version": item["version"],
                "exception_type": "license_review",
                "subject": item["license"],
                "severity": "denied",
                "source": "license_denied",
            }
        )

    npm_audit = report.get("npm_audit", {})

    if not npm_audit.get("available", False):
        risks.append(
            {
                "ecosystem": "platform",
                "package": "npm-audit",
                "version": "current",
                "exception_type": "scanner_unavailable",
                "subject": "npm",
                "severity": "unknown",
                "source": "npm_audit",
            }
        )
    else:
        for item in npm_audit.get("vulnerabilities", []):
            severity = str(
                item.get("severity", "unknown")
            ).lower()

            if severity not in {"critical", "high"}:
                continue

            risks.append(
                {
                    "ecosystem": "npm",
                    "package": item["name"],
                    "version": str(
                        item.get("range") or "unknown"
                    ),
                    "exception_type": "vulnerability",
                    "subject": severity,
                    "severity": severity,
                    "source": "npm_audit",
                }
            )

    python_audit = report.get("python_audit", {})

    if not python_audit.get("available", False):
        risks.append(
            {
                "ecosystem": "platform",
                "package": "pip-audit",
                "version": "current",
                "exception_type": "scanner_unavailable",
                "subject": "python",
                "severity": "unknown",
                "source": "pip_audit",
            }
        )
    else:
        for dependency in python_audit.get(
            "dependencies",
            [],
        ):
            package = str(
                dependency.get("name", "unknown")
            )
            version = str(
                dependency.get("version", "unknown")
            )

            for vulnerability in dependency.get(
                "vulns",
                [],
            ):
                vulnerability_id = str(
                    vulnerability.get("id", "unknown")
                )

                risks.append(
                    {
                        "ecosystem": "python",
                        "package": package,
                        "version": version,
                        "exception_type": "vulnerability",
                        "subject": vulnerability_id,
                        "severity": "high",
                        "source": "pip_audit",
                    }
                )

    return risks


def reconcile(
    registry: dict[str, Any],
    risk_report: dict[str, Any],
) -> dict[str, Any]:
    active = [
        item
        for item in registry.get("exceptions", [])
        if item.get("status") == "active"
    ]

    current_risks = collect_current_risks(
        risk_report
    )

    exception_map: dict[
        tuple[str, str, str, str, str],
        list[dict[str, Any]],
    ] = {}

    for item in active:
        exception_map.setdefault(
            exception_key(item),
            [],
        ).append(item)

    risk_map: dict[
        tuple[str, str, str, str, str],
        list[dict[str, Any]],
    ] = {}

    for item in current_risks:
        key = risk_key(
            ecosystem=item["ecosystem"],
            package=item["package"],
            version=item["version"],
            exception_type=item["exception_type"],
            subject=item["subject"],
        )

        risk_map.setdefault(key, []).append(item)

    failures: list[str] = []
    matched: list[dict[str, Any]] = []
    orphaned: list[dict[str, Any]] = []
    duplicate_exceptions: list[dict[str, Any]] = []

    for key, exceptions in exception_map.items():
        risks = risk_map.get(key, [])

        if len(exceptions) > 1:
            duplicate_exceptions.extend(exceptions)

            identifiers = ", ".join(
                sorted(
                    str(item.get("id"))
                    for item in exceptions
                )
            )

            failures.append(
                f"Duplicate active exceptions for {key}: "
                f"{identifiers}"
            )

        if not risks:
            orphaned.extend(exceptions)

            for item in exceptions:
                failures.append(
                    "Orphaned active exception "
                    f"{item.get('id')}: no matching current risk"
                )
        else:
            for item in exceptions:
                matched.append(
                    {
                        "exception": item,
                        "risks": risks,
                    }
                )

    unwaived: list[dict[str, Any]] = []

    for key, risks in risk_map.items():
        exceptions = exception_map.get(key, [])

        if exceptions:
            continue

        for risk in risks:
            if risk["source"] == "license_review_required":
                continue

            unwaived.append(risk)

    for risk in unwaived:
        failures.append(
            "Unwaived enforceable risk: "
            f"{risk['ecosystem']} "
            f"{risk['package']}@{risk['version']} "
            f"{risk['exception_type']} "
            f"{risk['subject']}"
        )

    return {
        "active_exception_count": len(active),
        "current_risk_count": len(current_risks),
        "matched": matched,
        "orphaned": orphaned,
        "duplicate_exceptions": duplicate_exceptions,
        "unwaived_enforceable_risks": unwaived,
        "failures": failures,
    }


def write_markdown(
    report: dict[str, Any],
) -> None:
    lines = [
        "# Nimble Dependency Exception Reconciliation",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Status: **{report['status']}**",
        "",
        f"- Active exceptions: `{report['active_exception_count']}`",
        f"- Current risks: `{report['current_risk_count']}`",
        f"- Matched exceptions: `{len(report['matched'])}`",
        f"- Orphaned exceptions: `{len(report['orphaned'])}`",
        (
            "- Duplicate exceptions: "
            f"`{len(report['duplicate_exceptions'])}`"
        ),
        (
            "- Unwaived enforceable risks: "
            f"`{len(report['unwaived_enforceable_risks'])}`"
        ),
    ]

    if report["matched"]:
        lines.extend(
            [
                "",
                "## Matched exceptions",
                "",
                "| Exception | Ecosystem | Package | Version | Type | Subject |",
                "|---|---|---|---|---|---|",
            ]
        )

        for match in report["matched"]:
            item = match["exception"]

            lines.append(
                f"| `{item['id']}` "
                f"| {item['ecosystem']} "
                f"| `{item['package']}` "
                f"| `{item['version']}` "
                f"| {item['exception_type']} "
                f"| `{item['subject']}` |"
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

    REPORT_MARKDOWN.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    try:
        registry = load_json(REGISTRY)
        risk_report = load_json(RISK_REPORT)
    except (
        FileNotFoundError,
        json.JSONDecodeError,
    ) as error:
        print("FAIL:", error)
        return 1

    result = reconcile(
        registry,
        risk_report,
    )

    now = datetime.now(UTC)

    report = {
        "schema_version": "1.0",
        "generated_at": now.isoformat(),
        "status": (
            "PASS"
            if not result["failures"]
            else "FAIL"
        ),
        **result,
    }

    REPORT_JSON.write_text(
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
    print("NIMBLE™ DEPENDENCY EXCEPTION RECONCILIATION")
    print("=" * 72)
    print(
        "Active exceptions:",
        report["active_exception_count"],
    )
    print(
        "Current risks:",
        report["current_risk_count"],
    )
    print(
        "Matched exceptions:",
        len(report["matched"]),
    )
    print(
        "Orphaned exceptions:",
        len(report["orphaned"]),
    )
    print(
        "Unwaived enforceable risks:",
        len(report["unwaived_enforceable_risks"]),
    )

    for failure in report["failures"]:
        print("FAIL:", failure)

    print("Status:", report["status"])

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
