"""Strategic Intelligence Domain for AletheusOS™.

Canonical capabilities:
- SPAN™: Spectrum Platform Analyzer & Navigator™
- SPARTAN™: Spatial Platform Analysis Recursive Transformative Autogenous Network™
"""

from .span import SPANCapability, build_span
from .spartan import SPARTANNetwork, build_spartan

__all__ = [
    "SPANCapability",
    "SPARTANNetwork",
    "build_span",
    "build_spartan",
]
