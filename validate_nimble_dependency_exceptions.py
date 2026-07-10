from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

REGISTRY = (
    ROOT
    / "nimble"
    / "governance"
    / "supply-chain"
    / "dependency-exceptions.json"
)

REPORT_JSON = (
    ROOT
    / "reports"
    / "nimble"
    / "dependency-exceptions-latest.json"
)

REPORT_MARKDOWN = (
    ROOT
    / "reports"
    / "nimble"
    / "dependency-exceptions-latest.md"
)

SUPPORTED_TYPES = {
    "license_review",
    "vulnerability",
    "scanner_unavailable",
}

SUPPORTED_ECOSYSTEMS = {
    "npm",
    "python",
    "platform",
}

REQUIRED_FIELDS = {
    "id",
    "ecosystem",
    "package",
    "version",
    "exception_type",
    "subject",
    "rationale",
    "approved_by",
    "owner",
    "ticket",
    "created_at",
    "expires_at",
    "status",
}


def parse_datetime(
    value: str,
) -> datetime:
    parsed = datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )

    if parsed.tzinfo is None:
        raise ValueError(
            "Timestamp must include a timezone."
        )

    return parsed.astimezone(timezone.utc)


def load_registry() -> dict[str, Any]:
    if not REGISTRY.exists():
        raise FileNotFoundError(
            "Dependency exception registry is missing."
        )

    return json.loads(
        REGISTRY.read_text(encoding="utf-8")
    )


def validate_exception(
    item: dict[str, Any],
    *,
    now: datetime,
) -> list[str]:
    failures: list[str] = []

    missing = REQUIRED_FIELDS - set(item)

    if missing:
        failures.append(
            "missing fields: "
            + ", ".join(sorted(missing))
        )
        return failures

    identifier = str(item["id"]).strip()

    if not identifier.startswith(
        "NIMBLE-DEP-EX-"
    ):
        failures.append(
            "id must begin with NIMBLE-DEP-EX-"
        )

    if item["ecosystem"] not in SUPPORTED_ECOSYSTEMS:
        failures.append(
            f"unsupported ecosystem: {item['ecosystem']}"
        )

    if item["exception_type"] not in SUPPORTED_TYPES:
        failures.append(
            "unsupported exception type: "
            f"{item['exception_type']}"
        )

    if item["status"] not in {
        "active",
        "revoked",
        "expired",
    }:
        failures.append(
            f"unsupported status: {item['status']}"
        )

    rationale = str(
        item["rationale"]
    ).strip()

    if len(rationale) < 30:
        failures.append(
            "rationale must contain at least "
            "30 characters"
        )

    for field in (
        "approved_by",
        "owner",
        "ticket",
        "package",
        "version",
        "subject",
    ):
        if not str(item[field]).strip():
            failures.append(
                f"{field} must not be empty"
            )

    try:
        created_at = parse_datetime(
            str(item["created_at"])
        )

        expires_at = parse_datetime(
            str(item["expires_at"])
        )
    except ValueError as error:
        failures.append(str(error))
        return failures

    if expires_at <= created_at:
        failures.append(
            "expires_at must be later than created_at"
        )

    if (
        item["status"] == "active"
        and expires_at <= now
    ):
        failures.append(
            "active exception has expired"
        )

    return failures


def write_markdown(
    report: dict[str, Any],
) -> None:
    lines = [
        "# Nimble Dependency Exception Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Status: **{report['status']}**",
        "",
        f"- Active: `{report['counts']['active']}`",
        f"- Revoked: `{report['counts']['revoked']}`",
        f"- Expired: `{report['counts']['expired']}`",
        f"- Invalid: `{report['counts']['invalid']}`",
        "",
        "## Registry",
        "",
        "| ID | Ecosystem | Package | Type | Owner | Expires | Status |",
        "|---|---|---|---|---|---|---|",
    ]

    for item in report["exceptions"]:
        lines.append(
            f"| `{item['id']}` "
            f"| {item.get('ecosystem', '')} "
            f"| `{item.get('package', '')}` "
            f"| {item.get('exception_type', '')} "
            f"| {item.get('owner', '')} "
            f"| `{item.get('expires_at', '')}` "
            f"| **{item['validation_status']}** |"
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
        registry = load_registry()
    except (
        FileNotFoundError,
        json.JSONDecodeError,
    ) as error:
        print("FAIL:", error)
        return 1

    if registry.get("schema_version") != "1.0":
        print(
            "FAIL: Unsupported exception registry schema."
        )
        return 1

    exceptions = registry.get(
        "exceptions"
    )

    if not isinstance(exceptions, list):
        print(
            "FAIL: exceptions must be an array."
        )
        return 1

    now = datetime.now(timezone.utc)
    seen_ids: set[str] = set()
    failures: list[str] = []
    records: list[dict[str, Any]] = []

    counts = {
        "active": 0,
        "revoked": 0,
        "expired": 0,
        "invalid": 0,
    }

    for item in exceptions:
        identifier = str(
            item.get("id", "unknown")
        )

        item_failures = validate_exception(
            item,
            now=now,
        )

        if identifier in seen_ids:
            item_failures.append(
                "duplicate exception id"
            )

        seen_ids.add(identifier)

        if item_failures:
            counts["invalid"] += 1

            for failure in item_failures:
                failures.append(
                    f"{identifier}: {failure}"
                )

            validation_status = "INVALID"
        else:
            status = item["status"]
            counts[status] += 1
            validation_status = status.upper()

        records.append(
            {
                **item,
                "validation_status":
                    validation_status,
                "validation_failures":
                    item_failures,
            }
        )

    report = {
        "schema_version": "1.0",
        "generated_at": now.isoformat(),
        "status": (
            "PASS"
            if not failures
            else "FAIL"
        ),
        "counts": counts,
        "exceptions": records,
        "failures": failures,
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
    print("NIMBLE™ DEPENDENCY EXCEPTION GOVERNANCE")
    print("=" * 72)
    print("Active exceptions:", counts["active"])
    print("Revoked exceptions:", counts["revoked"])
    print("Expired exceptions:", counts["expired"])
    print("Invalid exceptions:", counts["invalid"])

    for failure in failures:
        print("FAIL:", failure)

    print("Status:", report["status"])

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
