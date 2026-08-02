from __future__ import annotations

from dataclasses import replace
from typing import ClassVar

from .models import NavigationContext, NavigationMode


class Engine:
    VERSION: ClassVar[str] = "29.0.0"
    SUPPORTED_MODES: ClassVar[frozenset[NavigationMode]] = frozenset(NavigationMode)

    def navigate(
        self,
        context: NavigationContext,
        destination: str,
        *,
        mode: NavigationMode = NavigationMode.CONTEXTUAL,
    ) -> NavigationContext:
        if mode not in self.SUPPORTED_MODES:
            raise ValueError(f"Unsupported navigation mode: {mode}")
        return replace(
            context,
            current_node=destination,
            history=context.history + (context.current_node,),
        )

    def back(self, context: NavigationContext) -> NavigationContext:
        if not context.history:
            return context
        return replace(
            context, current_node=context.history[-1], history=context.history[:-1]
        )
