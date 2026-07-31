"""Read-only Runtime Explorer façade."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from types import MappingProxyType

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalAddress,
    ConstitutionalHealth,
    ConstitutionalKind,
    ConstitutionalObject,
    ConstitutionalState,
    RelationshipKind,
)
from aletheus.platform_intelligence.constitutional_graph import (
    ConstitutionalGraph,
)
from aletheus.platform_intelligence.digital_twin import (
    PlatformDigitalTwin,
    TwinSnapshot,
    TwinSnapshotDiff,
)
from aletheus.platform_intelligence.service_registry import (
    PlatformServiceRegistry,
)

from .exceptions import ExplorerObjectNotFoundError
from .query import ExplorerQuery
from .results import (
    ExplorerImpactResult,
    ExplorerSearchResult,
    RuntimeExplorerStatistics,
)

_UNHEALTHY = frozenset(
    {
        ConstitutionalHealth.WARNING,
        ConstitutionalHealth.DEGRADED,
        ConstitutionalHealth.CRITICAL,
        ConstitutionalHealth.OFFLINE,
    }
)


class RuntimeExplorer:
    """
    Canonical read interface over Platform Intelligence.

    The Explorer performs discovery, search, traversal, impact analysis,
    snapshot inspection, and structural queries. It never mutates the Twin,
    Graph, Registry, or runtime.
    """

    def __init__(
        self,
        *,
        twin: PlatformDigitalTwin,
        graph: ConstitutionalGraph,
        service_registry: PlatformServiceRegistry,
    ) -> None:
        self._twin = twin
        self._graph = graph
        self._service_registry = service_registry

    @property
    def twin(self) -> PlatformDigitalTwin:
        return self._twin

    def object(
        self,
        address: str | ConstitutionalAddress,
    ) -> ConstitutionalObject:
        try:
            return self._twin.object(address)
        except Exception as error:
            raise ExplorerObjectNotFoundError(
                f"Explorer object not found: {address}"
            ) from error

    def objects(self) -> tuple[ConstitutionalObject, ...]:
        """Return every known object, deduplicated by address."""

        indexed: dict[
            str,
            ConstitutionalObject,
        ] = {}

        for item in self._service_registry.all():
            indexed[item.address] = item

        for item in self._graph.nodes():
            indexed[item.address] = item

        return tuple(indexed[address] for address in sorted(indexed))

    def services(
        self,
    ) -> tuple[ConstitutionalObject, ...]:
        return self._service_registry.all()

    def find_by_kind(
        self,
        kind: ConstitutionalKind,
    ) -> tuple[ConstitutionalObject, ...]:
        return self._filter(
            self.objects(),
            lambda item: item.kind is kind,
        )

    def find_by_state(
        self,
        state: ConstitutionalState,
    ) -> tuple[ConstitutionalObject, ...]:
        return self._filter(
            self.objects(),
            lambda item: item.state is state,
        )

    def find_by_health(
        self,
        health: ConstitutionalHealth,
    ) -> tuple[ConstitutionalObject, ...]:
        return self._filter(
            self.objects(),
            lambda item: item.health is health,
        )

    def find_by_owner(
        self,
        owner: str,
    ) -> tuple[ConstitutionalObject, ...]:
        needle = owner.strip().casefold()

        return self._filter(
            self.objects(),
            lambda item: needle in item.owner.casefold(),
        )

    def find_by_authority(
        self,
        authority: str,
    ) -> tuple[ConstitutionalObject, ...]:
        needle = authority.strip().casefold()

        return self._filter(
            self.objects(),
            lambda item: needle in item.authority.casefold(),
        )

    def unhealthy(
        self,
    ) -> tuple[ConstitutionalObject, ...]:
        return self._filter(
            self.objects(),
            lambda item: item.health in _UNHEALTHY,
        )

    def search(
        self,
        text: str,
    ) -> tuple[ExplorerSearchResult, ...]:
        needle = text.strip().casefold()

        if not needle:
            return ()

        results: list[ExplorerSearchResult] = []

        for item in self.objects():
            fields = {
                "address": item.address,
                "canonical_name": item.canonical_name,
                "description": item.description,
                "owner": item.owner,
                "authority": item.authority,
                "kind": item.kind.value,
                "state": item.state.value,
                "health": item.health.value,
            }

            matched: list[str] = []
            score = 0

            for field, value in fields.items():
                normalized = str(value).casefold()

                if normalized == needle:
                    matched.append(field)
                    score += 100
                elif needle in normalized:
                    matched.append(field)
                    score += (
                        40
                        if field
                        in {
                            "address",
                            "canonical_name",
                        }
                        else 10
                    )

            if matched:
                results.append(
                    ExplorerSearchResult(
                        object=item,
                        score=score,
                        matched_fields=tuple(sorted(matched)),
                    )
                )

        return tuple(
            sorted(
                results,
                key=lambda result: (
                    -result.score,
                    result.object.address,
                ),
            )
        )

    def query(
        self,
        expression: str,
    ) -> tuple[ConstitutionalObject, ...]:
        query = ExplorerQuery.parse(expression)
        candidates = self.objects()

        for field, value in query.terms:
            candidates = tuple(
                item
                for item in candidates
                if self._matches(
                    item,
                    field,
                    value,
                )
            )

        return tuple(
            sorted(
                candidates,
                key=lambda item: item.address,
            )
        )

    def dependencies(
        self,
        address: str | ConstitutionalAddress,
        *,
        transitive: bool = False,
    ) -> tuple[ConstitutionalObject, ...]:
        self.object(address)

        if transitive:
            return self._graph.downstream(
                address,
                kinds={RelationshipKind.DEPENDS_ON},
            )

        return self._twin.dependencies(address)

    def dependents(
        self,
        address: str | ConstitutionalAddress,
        *,
        transitive: bool = False,
    ) -> tuple[ConstitutionalObject, ...]:
        self.object(address)

        if transitive:
            return self._graph.upstream(
                address,
                kinds={RelationshipKind.DEPENDS_ON},
            )

        return self._twin.dependents(address)

    def path(
        self,
        source: str | ConstitutionalAddress,
        target: str | ConstitutionalAddress,
    ) -> tuple[ConstitutionalObject, ...]:
        self.object(source)
        self.object(target)

        return self._graph.shortest_path(
            source,
            target,
        )

    def impact(
        self,
        address: str | ConstitutionalAddress,
    ) -> ExplorerImpactResult:
        subject = self.object(address)
        direct = self.dependents(address)
        transitive = self.dependents(
            address,
            transitive=True,
        )

        return ExplorerImpactResult(
            subject=subject,
            direct_dependents=direct,
            transitive_dependents=transitive,
            affected_count=len(transitive),
        )

    def orphans(
        self,
    ) -> tuple[ConstitutionalObject, ...]:
        return self._graph.orphans()

    def cycles(
        self,
    ) -> tuple[
        tuple[ConstitutionalAddress, ...],
        ...,
    ]:
        return self._graph.cycles()

    def roots(
        self,
    ) -> tuple[ConstitutionalObject, ...]:
        return self._graph.roots()

    def leaves(
        self,
    ) -> tuple[ConstitutionalObject, ...]:
        return self._graph.leaves()

    def graph_snapshot(
        self,
    ) -> dict[str, object]:
        return self._graph.snapshot()

    def twin_state(
        self,
    ) -> dict[str, object]:
        return self._twin.current_state()

    def snapshot(
        self,
        *,
        retain: bool = True,
    ) -> TwinSnapshot:
        return self._twin.snapshot(retain=retain)

    def snapshots(
        self,
    ) -> tuple[TwinSnapshot, ...]:
        return self._twin.retained_snapshots()

    def diff(
        self,
        previous: TwinSnapshot,
        current: TwinSnapshot,
    ) -> TwinSnapshotDiff:
        return self._twin.diff(
            previous,
            current,
        )

    def statistics(
        self,
    ) -> RuntimeExplorerStatistics:
        objects = self.objects()
        graph_stats = self._graph.statistics()
        twin_stats = self._twin.statistics()

        kind_counts = Counter(item.kind.value for item in objects)
        state_counts = Counter(item.state.value for item in objects)
        health_counts = Counter(item.health.value for item in objects)

        return RuntimeExplorerStatistics(
            objects=len(objects),
            services=len(self._service_registry.all()),
            relationships=(graph_stats.relationships),
            unhealthy=sum(item.health in _UNHEALTHY for item in objects),
            orphans=graph_stats.orphans,
            cycles=graph_stats.cycles,
            retained_snapshots=(twin_stats.snapshots_retained),
            twin_revision=twin_stats.revision,
            objects_by_kind=MappingProxyType(dict(kind_counts)),
            objects_by_state=MappingProxyType(dict(state_counts)),
            objects_by_health=MappingProxyType(dict(health_counts)),
        )

    @staticmethod
    def _filter(
        values: Iterable[ConstitutionalObject],
        predicate: object,
    ) -> tuple[ConstitutionalObject, ...]:
        return tuple(
            sorted(
                (
                    item
                    for item in values
                    if predicate(item)  # type: ignore[operator]
                ),
                key=lambda item: item.address,
            )
        )

    @staticmethod
    def _matches(
        item: ConstitutionalObject,
        field: str,
        value: str,
    ) -> bool:
        if field == "text":
            searchable = " ".join(
                (
                    item.address,
                    item.canonical_name,
                    item.description,
                    item.owner,
                    item.authority,
                )
            ).casefold()
            return value in searchable

        values = {
            "kind": item.kind.value,
            "state": item.state.value,
            "health": item.health.value,
            "owner": item.owner,
            "authority": item.authority,
            "address": item.address,
        }

        return value in values[field].casefold()
