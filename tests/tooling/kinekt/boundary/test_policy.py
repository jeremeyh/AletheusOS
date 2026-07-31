from aletheus.tooling.kinekt.boundary.policy import evaluate


def test_runtime_product_boundary_violation() -> None:
    finding = evaluate(
        "aletheus.runtime.core",
        "aletheus.cardhawk.app",
        "runtime",
        "product",
        ("aletheus/runtime/core.py", "aletheus/cardhawk/app.py"),
    )

    assert finding is not None
    assert finding.severity == "high"
