from aletheus.tooling.kinekt.boundary.taxonomy import classify_layer


def test_runtime_classification() -> None:
    assert (
        classify_layer(
            "module:aletheus.runtime.core",
            "aletheus.runtime.core",
            "Constitutional Runtime Kernel",
        )
        == "runtime"
    )


def test_product_classification() -> None:
    assert (
        classify_layer(
            "module:aletheus.cardhawk.app",
            "aletheus.cardhawk.app",
            "Card Hawk",
        )
        == "product"
    )
