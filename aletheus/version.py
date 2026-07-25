"""Canonical AletheusOS release identity.

All runtime, packaging, UI, and release metadata must derive from this module.
"""

__version__ = "4.2.1"
VERSION = __version__
PRODUCT_NAME = "AletheusOS"
RUNTIME_NAME = "Aletheus Runtime"

__all__ = ["PRODUCT_NAME", "RUNTIME_NAME", "VERSION", "__version__"]
