"""Convenience bootstrap for SPAN™ and SPARTAN™.

This file avoids modifying the existing runtime composition root. A later
integration drop can wire this bootstrap into the Constitutional Runtime Kernel
after the repository's exact runtime interfaces are inspected.
"""

from __future__ import annotations

from aletheus.strategic.span import SPANConfig, build_span
from aletheus.strategic.spartan import build_spartan


def build_strategic_intelligence(
    config: SPANConfig | None = None,
):
    resolved_config = config or SPANConfig()
    spartan = build_spartan(resolved_config.enabled_spartan_domains)
    span = build_span(resolved_config, spartan=spartan)
    return span
