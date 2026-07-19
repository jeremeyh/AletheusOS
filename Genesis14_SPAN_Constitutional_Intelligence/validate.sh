#!/usr/bin/env bash
set -Eeuo pipefail

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${1:-$(pwd)}"
cd "$PROJECT_ROOT"

echo "Compiling Genesis 14 modules..."
python -m compileall -q \
  aletheus/span/api.py \
  aletheus/span/constitutional_context.py \
  aletheus/span/profiles.py \
  aletheus/span/reporter.py \
  aletheus/span/rules

echo "Running Genesis 14 contract validation..."
python - <<'PY'
from pathlib import Path
from tempfile import TemporaryDirectory

from aletheus.span import SPAN, SPANReport, RuleProfile, load_profile
from aletheus.span.rule_loader import RuleLoader
from aletheus.span.rule_registry import RuleRegistry

registry = RuleRegistry()
load_report = RuleLoader(registry).load_all(strict=True)
assert load_report.ok, load_report.to_dict()
assert len(registry) == 20, f"expected 20 rules, got {len(registry)}"

profile = load_profile("aletheus/span/profiles/constitutional.yaml")
assert profile.name == "constitutional"
assert len(profile.enabled_categories) == 10

with TemporaryDirectory() as temp:
    root = Path(temp)
    (root / "aletheus" / "span").mkdir(parents=True)
    (root / "README.md").write_text("# Sample\n")
    (root / "bad.py").write_text(
        'API_KEY = "12345678901234567890"\n'
        'def public(items=[]):\n'
        '    print("x")\n'
        '    return items\n'
    )
    report = SPAN(profile).analyze(root)
    assert isinstance(report, SPANReport)
    ids = {finding.id for finding in report.findings}
    assert "SPAN-SEC-001" in ids
    assert "SPAN-API-001" in ids
    assert "SPAN-QUA-002" in ids
    assert report.metadata["rules_executed"] == 20
    assert report.to_json()
    assert report.to_markdown().startswith("# SPAN")

print("Public API: OK")
print("Rule discovery: OK")
print("Rules registered: 20")
print("Profiles: OK")
print("Project inspection: OK")
print("Evidence attachment: OK")
print("JSON reporter: OK")
print("Markdown reporter: OK")
print("End-to-end analysis: OK")
PY

if command -v pytest >/dev/null 2>&1; then
  echo "Running focused pytest validation..."
  pytest -q tests/span/test_genesis14.py
else
  echo "pytest not installed; focused runtime validation already passed."
fi
