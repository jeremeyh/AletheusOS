from __future__ import annotations

from pathlib import Path

from aletheus.constitutional_graph import ConstitutionalKnowledgeGraph
from aletheus.institutional_civilization import (
    CivilizationBootstrap,
    InstitutionRegistry,
    InstitutionWiring,
    canonical_institutions,
)
from aletheus.platform_registry import PlatformRegistry


class FakeWatchTower:
    def verify(self):
        return {
            "status": "ready",
            "findings": [],
        }


class FakeSPA:
    def assess(self, root="."):
        return {
            "status": "healthy",
            "summary": {},
        }


class FakeHomeostasis:
    def __init__(self):
        self.records = []

    def record(self, name, score, message=""):
        self.records.append((name, score, message))
        return {
            "name": name,
            "score": score,
            "message": message,
        }


class FakeCouncil:
    def evaluate(self, proposal):
        return {
            "approved": True,
        }


class FakeLedger:
    def record_event(self, event):
        return event


def build_bootstrap(tmp_path):
    wiring = InstitutionWiring(
        root=Path(tmp_path),
        watch_tower=FakeWatchTower(),
        spa=FakeSPA(),
        homeostasis=FakeHomeostasis(),
        council=FakeCouncil(),
        ledger=FakeLedger(),
    )

    bootstrap = CivilizationBootstrap(
        root=tmp_path,
        institution_registry=InstitutionRegistry(),
        platform_registry=PlatformRegistry(),
        constitutional_graph=ConstitutionalKnowledgeGraph(),
        wiring=wiring,
    )

    return bootstrap, wiring


def test_bootstrap_projects_canonical_civilization(tmp_path):
    bootstrap, _ = build_bootstrap(tmp_path)

    report = bootstrap.bootstrap()

    expected = len(canonical_institutions())

    assert report.status == "ready"
    assert report.institution_count == expected
    assert report.platform_component_count == expected
    assert report.graph_node_count == expected

    # Relationships should exist between institutions.
    assert report.graph_edge_count > 0

    # All checks should complete successfully.
    assert report.failed_count == 0
    assert report.synthetic_harmony == 100.0
