from __future__ import annotations

from .analyzer import Analyzer


class AnalyzerRegistry:
    """Canonical registry for SPAN analyzers."""

    def __init__(self) -> None:
        self._analyzers: dict[str, Analyzer] = {}
        self._enabled: dict[str, bool] = {}

    @classmethod
    def default(cls) -> AnalyzerRegistry:
        """
        Discover and register the built-in SPAN analyzers.
        """
        from .analyzer_loader import AnalyzerLoader

        return AnalyzerLoader().load_registry()

    def register(
        self,
        analyzer: Analyzer,
        *,
        name: str | None = None,
    ) -> None:
        key = name or getattr(
            analyzer,
            "name",
            analyzer.__class__.__name__,
        )

        if key in self._analyzers:
            raise ValueError(f"Analyzer already registered: {key}")

        self._analyzers[key] = analyzer
        self._enabled[key] = True

    def unregister(
        self,
        name: str,
    ) -> None:
        self._analyzers.pop(name, None)
        self._enabled.pop(name, None)

    def enable(
        self,
        name: str,
    ) -> None:
        if name not in self._analyzers:
            raise KeyError(name)

        self._enabled[name] = True

    def disable(
        self,
        name: str,
    ) -> None:
        if name not in self._analyzers:
            raise KeyError(name)

        self._enabled[name] = False

    def get(
        self,
        name: str,
    ) -> Analyzer:
        return self._analyzers[name]

    def list(self) -> tuple[str, ...]:
        return tuple(self._analyzers.keys())

    def enabled(self) -> tuple[Analyzer, ...]:
        return tuple(
            analyzer
            for name, analyzer in self._analyzers.items()
            if self._enabled.get(name, False)
        )

    def analyzers(self) -> tuple[Analyzer, ...]:
        """
        Backwards-compatible alias expected by SpanEngine.
        """
        return self.enabled()
