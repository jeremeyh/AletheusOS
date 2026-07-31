from __future__ import annotations

import ast
import difflib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from aletheus.runtime import runtime_core

ROOT = Path(__file__).resolve().parent
TESTS = ROOT / "tests"
ALETHEUS = ROOT / "aletheus"
REPORT_DIR = ROOT / "reports/genesis_8_command_dispatch"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

JSON_REPORT = REPORT_DIR / "command_compatibility_manifest.json"
MD_REPORT = REPORT_DIR / "command_compatibility_manifest.md"


def normalize_command(name: str) -> str:
    replacements = {
        "statistics": "stats",
        "statistic": "stats",
        "prediction": "predict",
        "learning": "learn",
        "role_create": "role.create",
        "role_assign": "role.assign",
    }

    normalized = name.lower().strip()

    for old, new in replacements.items():
        normalized = normalized.replace(old, new)

    normalized = re.sub(r"[^a-z0-9]+", ".", normalized)
    normalized = re.sub(r"\.+", ".", normalized)

    return normalized.strip(".")


def command_tokens(name: str) -> set[str]:
    return {token for token in normalize_command(name).split(".") if token}


def similarity(left: str, right: str) -> float:
    sequence = difflib.SequenceMatcher(
        None,
        normalize_command(left),
        normalize_command(right),
    ).ratio()

    left_tokens = command_tokens(left)
    right_tokens = command_tokens(right)

    union = left_tokens | right_tokens
    token_score = len(left_tokens & right_tokens) / len(union) if union else 0.0

    return round((sequence * 0.65) + (token_score * 0.35), 4)


def extract_dispatch_commands(path: Path) -> list[dict[str, Any]]:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (OSError, SyntaxError, UnicodeDecodeError):
        return []

    commands: list[dict[str, Any]] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        function = node.func
        function_name = None

        if isinstance(function, ast.Attribute):
            function_name = function.attr

        if function_name not in {"dispatch", "execute"}:
            continue

        if not node.args:
            continue

        first = node.args[0]

        if not (isinstance(first, ast.Constant) and isinstance(first.value, str)):
            continue

        commands.append(
            {
                "command": first.value,
                "file": str(path.relative_to(ROOT)),
                "line": node.lineno,
            }
        )

    return commands


def build_source_index() -> dict[str, list[tuple[int, str]]]:
    index: dict[str, list[tuple[int, str]]] = {}

    for source_path in ALETHEUS.rglob("*.py"):
        path_text = str(source_path)

        if any(
            marker in path_text
            for marker in (
                ".backup",
                "before_",
                "restored",
                "__pycache__",
            )
        ):
            continue

        try:
            lines = source_path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue

        index[str(source_path.relative_to(ROOT))] = [
            (line_number, line)
            for line_number, line in enumerate(
                lines,
                start=1,
            )
        ]

    return index


def find_source_references(
    command: str,
    source_index: dict[str, list[tuple[int, str]]],
) -> list[str]:
    references: list[str] = []

    for relative_path, lines in source_index.items():
        for line_number, line in lines:
            if command in line:
                references.append(f"{relative_path}:{line_number}")

                if len(references) >= 20:
                    return references

    return references


def handler_identity(record: Any) -> str | None:
    if record is None:
        return None

    handler = record.handler

    return (
        f"{getattr(handler, '__module__', type(handler).__module__)}."
        f"{getattr(handler, '__qualname__', type(handler).__qualname__)}"
    )


registry = runtime_core.commands.registry
registered = set(registry.list())

print("Indexing Aletheus source files...")
source_index = build_source_index()
print(f"Indexed {len(source_index)} Python files.")

test_occurrences: list[dict[str, Any]] = []

for test_file in sorted(TESTS.rglob("test_*.py")):
    test_occurrences.extend(extract_dispatch_commands(test_file))

requirements: dict[str, list[dict[str, Any]]] = defaultdict(list)

for occurrence in test_occurrences:
    requirements[occurrence["command"]].append(occurrence)

manifest: list[dict[str, Any]] = []

for command in sorted(requirements):
    is_registered = command in registered
    record = registry.get(command) if is_registered else None

    candidates = sorted(
        (
            {
                "command": candidate,
                "score": similarity(command, candidate),
            }
            for candidate in registered
            if candidate != command
        ),
        key=lambda item: item["score"],
        reverse=True,
    )[:5]

    strong_candidates = [item for item in candidates if item["score"] >= 0.55]

    source_references = find_source_references(
        command,
        source_index,
    )

    if is_registered:
        classification = "registered"
    elif strong_candidates:
        classification = "probable_alias"
    elif source_references:
        classification = "defined_but_not_registered"
    else:
        classification = "missing_capability"

    manifest.append(
        {
            "command": command,
            "classification": classification,
            "registered": is_registered,
            "handler": handler_identity(record),
            "category": (record.category if record is not None else None),
            "invocation_mode": (
                registry.dispatcher.invocation_mode(command) if is_registered else None
            ),
            "tests": requirements[command],
            "candidate_aliases": strong_candidates,
            "source_references": source_references,
        }
    )


summary = {
    "test_command_requirements": len(manifest),
    "registered_requirements": sum(1 for item in manifest if item["registered"]),
    "probable_aliases": sum(
        1 for item in manifest if item["classification"] == "probable_alias"
    ),
    "defined_but_not_registered": sum(
        1 for item in manifest if item["classification"] == "defined_but_not_registered"
    ),
    "missing_capabilities": sum(
        1 for item in manifest if item["classification"] == "missing_capability"
    ),
    "live_registry_commands": registry.count(),
    "generation": registry.generation,
    "fingerprint": registry.fingerprint,
}

JSON_REPORT.write_text(
    json.dumps(
        {
            "summary": summary,
            "commands": manifest,
        },
        indent=2,
        sort_keys=True,
    ),
    encoding="utf-8",
)


lines = [
    "# Genesis 8 Command Compatibility Manifest",
    "",
    "## Summary",
    "",
]

for key, value in summary.items():
    lines.append(f"- {key}: **{value}**")

groups = (
    "probable_alias",
    "defined_but_not_registered",
    "missing_capability",
    "registered",
)

for group in groups:
    items = [item for item in manifest if item["classification"] == group]

    lines.extend(
        [
            "",
            f"## {group.replace('_', ' ').title()}",
            "",
        ]
    )

    if not items:
        lines.append("_None._")
        continue

    for item in items:
        lines.extend(
            [
                f"### `{item['command']}`",
                "",
                f"- Registered: `{item['registered']}`",
                f"- Handler: `{item['handler']}`",
                f"- Invocation mode: `{item['invocation_mode']}`",
            ]
        )

        test_locations = ", ".join(
            f"`{entry['file']}:{entry['line']}`" for entry in item["tests"]
        )
        lines.append(f"- Tests: {test_locations}")

        if item["candidate_aliases"]:
            candidates = ", ".join(
                (f"`{candidate['command']}` ({candidate['score']:.2f})")
                for candidate in item["candidate_aliases"]
            )
            lines.append(f"- Alias candidates: {candidates}")

        if item["source_references"]:
            references = ", ".join(
                f"`{reference}`" for reference in item["source_references"]
            )
            lines.append(f"- Source references: {references}")

        lines.append("")

MD_REPORT.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print("Genesis 8 compatibility manifest generated.")
print(f"JSON: {JSON_REPORT.relative_to(ROOT)}")
print(f"Markdown: {MD_REPORT.relative_to(ROOT)}")
print()
for key, value in summary.items():
    print(f"{key}: {value}")
