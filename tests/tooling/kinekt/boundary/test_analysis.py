from aletheus.tooling.kinekt.boundary.analysis import analyze_boundaries


def test_boundary_analysis_detects_violation() -> None:
    dependency = {
        "nodes": [
            {
                "node_id": "module:aletheus.runtime.core",
                "name": "aletheus.runtime.core",
                "capability": "Constitutional Runtime Kernel",
            },
            {
                "node_id": "module:aletheus.cardhawk.app",
                "name": "aletheus.cardhawk.app",
                "capability": "Card Hawk",
            },
        ],
        "relationships": [
            {
                "source": "module:aletheus.runtime.core",
                "target": "module:aletheus.cardhawk.app",
                "relationship": "imports",
                "evidence": [
                    "aletheus/runtime/core.py",
                    "aletheus/cardhawk/app.py",
                ],
            }
        ],
    }
    cohesion = {"packages": []}

    findings, pressure, unresolved = analyze_boundaries(
        dependency,
        cohesion,
    )

    assert len(findings) == 1
    assert pressure
    assert unresolved == 0
