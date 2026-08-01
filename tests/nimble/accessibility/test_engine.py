from aletheus.nimble.accessibility.engine import AccessibilityProfile, Engine


def test_accessibility_adaptation() -> None:
    report = Engine().adapt(
        AccessibilityProfile(reduced_motion=True), viewport_width=500
    )
    assert report["motion"] == "reduced" and report["density"] == "compact"
