"""AletheusOS Constitutional Scenario Engine™."""

from .comparison import (
    compare_assumptions,
    compare_scenario_outcomes,
)
from .engine import (
    ConstitutionalScenarioEngine,
    MetricProjector,
)
from .factory import create_scenario
from .instrumentation import (
    SCENARIO_ACTIVITY_ID,
    SCENARIO_CONFIDENCE_ID,
    SCENARIO_VIRTUE_ID,
    ScenarioInstrumentPublisher,
    register_scenario_instruments,
)
from .models import (
    AssumptionKind,
    ScenarioAssumption,
    ScenarioComparison,
    ScenarioDefinition,
    ScenarioMetricDelta,
    ScenarioOutcome,
    ScenarioStatus,
    new_scenario_id,
    new_scenario_run_id,
)
from .registry import (
    ConstitutionalScenarioRegistry,
    DuplicateScenarioError,
)

__all__ = [
    "AssumptionKind",
    "ConstitutionalScenarioEngine",
    "ConstitutionalScenarioRegistry",
    "DuplicateScenarioError",
    "MetricProjector",
    "SCENARIO_ACTIVITY_ID",
    "SCENARIO_CONFIDENCE_ID",
    "SCENARIO_VIRTUE_ID",
    "ScenarioAssumption",
    "ScenarioComparison",
    "ScenarioDefinition",
    "ScenarioInstrumentPublisher",
    "ScenarioMetricDelta",
    "ScenarioOutcome",
    "ScenarioStatus",
    "compare_assumptions",
    "compare_scenario_outcomes",
    "create_scenario",
    "new_scenario_id",
    "new_scenario_run_id",
    "register_scenario_instruments",
]
