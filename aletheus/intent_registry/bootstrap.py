from .models import IntentRecord
from .registry import IntentRegistry


def bootstrap_intents() -> IntentRegistry:
    registry = IntentRegistry()

    registry.register(IntentRecord(
        id="aletheus_os",
        name="AletheusOS",
        purpose="Provide a universal intelligence platform for hosted applications.",
        owner_layer="platform",
        capabilities=["runtime", "memory", "reasoning", "workflow", "governance"],
        outputs=["platform_services", "application_runtime"],
    ))

    registry.register(IntentRecord(
        id="card_hawk",
        name="Card Hawk",
        purpose="Provide collectibles intelligence, asset management, and portfolio decision support.",
        owner_layer="application",
        capabilities=["asset_vault", "portfolio", "marketplace", "vision", "analytics"],
        dependencies=["aletheus_os"],
        outputs=["collectibles_insight", "portfolio_intelligence"],
    ))

    registry.register(IntentRecord(
        id="platform_intelligence",
        name="Platform Intelligence",
        purpose="Measure architectural fitness and help AletheusOS understand its own structure.",
        owner_layer="platform",
        capabilities=["architecture_analysis", "repository_inspection"],
        outputs=["fitness_report", "architectural_risk"],
    ))

    return registry
