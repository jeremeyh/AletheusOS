"""
Aletheus Platform Intelligence

Canonical public façade.
"""

#
# Legacy API
#
#
# Canonical subpackages
#
from .constitutional import *
from .constitutional import __all__ as constitutional_all
from .constitutional_dependency_manager import *
from .constitutional_dependency_manager import __all__ as dependency_all
from .constitutional_graph import *
from .constitutional_graph import __all__ as graph_all
from .constitutional_policy_engine import *
from .constitutional_policy_engine import __all__ as policy_all
from .constitutional_runtime_council import *
from .constitutional_runtime_council import __all__ as council_all
from .constitutional_runtime_executive import *
from .constitutional_runtime_executive import __all__ as executive_all
from .constitutional_runtime_governor import *
from .constitutional_runtime_governor import __all__ as governor_all
from .constitutional_runtime_kernel import *
from .constitutional_runtime_kernel import __all__ as kernel_all
from .constitutional_runtime_supervisor import *
from .constitutional_runtime_supervisor import __all__ as supervisor_all
from .digital_twin import *
from .digital_twin import __all__ as twin_all
from .engine import PlatformIntelligenceEngine
from .event_bus import *
from .event_bus import __all__ as event_bus_all
from .events import *
from .events import __all__ as events_all
from .intelligence_engine import *
from .intelligence_engine import __all__ as intelligence_all
from .mission_engine import *
from .mission_engine import __all__ as mission_engine_all
from .mission_scheduler import *
from .mission_scheduler import __all__ as scheduler_all
from .models import ArchitecturalFitnessReport
from .orchestrator import *
from .orchestrator import __all__ as orchestrator_all
from .reporter import PlatformIntelligenceReporter
from .runtime_explorer import *
from .runtime_explorer import __all__ as explorer_all
from .service_registry import *
from .service_registry import __all__ as registry_all

__all__ = [
    "PlatformIntelligenceEngine",
    "PlatformIntelligenceReporter",
    "ArchitecturalFitnessReport",

    *constitutional_all,
    *dependency_all,
    *graph_all,
    *policy_all,
    *council_all,
    *executive_all,
    *governor_all,
    *kernel_all,
    *supervisor_all,
    *twin_all,
    *event_bus_all,
    *events_all,
    *intelligence_all,
    *mission_engine_all,
    *scheduler_all,
    *orchestrator_all,
    *explorer_all,
    *registry_all,
]
