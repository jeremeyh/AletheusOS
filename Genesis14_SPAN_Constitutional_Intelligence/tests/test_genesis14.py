from pathlib import Path

from aletheus.span.api import SPAN
from aletheus.span.profiles import load_profile
from aletheus.span.rule_loader import RuleLoader
from aletheus.span.rule_registry import RuleRegistry


def test_rule_discovery():
    registry = RuleRegistry()
    report = RuleLoader(registry).load_all(strict=True)
    assert not report.errors
    assert len(registry) >= 20


def test_profile_loading():
    profile_path = Path("aletheus/span/profiles/constitutional.yaml")
    profile = load_profile(profile_path)
    assert profile.name == "constitutional"
    assert "security" in profile.enabled_categories


def test_end_to_end_analysis():
    report = SPAN("aletheus/span/profiles/constitutional.yaml").analyze(".")
    assert report.metadata["rules_executed"] >= 20
    assert report.metadata["genesis"] == "14.0"
    assert isinstance(report.to_json(), str)
    assert "# SPAN Constitutional Intelligence Report" in report.to_markdown()
