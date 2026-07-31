from aletheus.tooling.kinekt.dependency.policy import evaluate_dependency


def test_runtime_product_dependency_is_rejected() -> None:
    finding = evaluate_dependency(
        "aletheus.runtime.core",
        "Constitutional Runtime Kernel",
        "aletheus.cardhawk.app",
        "Card Hawk",
        ("aletheus/runtime/core.py", "aletheus/cardhawk/app.py"),
    )

    assert finding is not None
    assert finding.severity == "high"
