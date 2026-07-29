from __future__ import annotations

from typing import Any

from aletheus.runtime_platform.manifest.runtime_manifest import RuntimeManifest
from aletheus.runtime_platform.manifest.validator import RuntimeManifestValidator
from aletheus.runtime_platform.topology.component import RuntimeComponent
from aletheus.runtime_platform.topology.domain import RuntimeDomain
from aletheus.runtime_platform.topology.service import RuntimeService
from aletheus.runtime_platform.topology.topology_registry import RuntimeTopologyRegistry

from .activation import RuntimeActivationResult
from .boot_context import BootContext
from .boot_phase import BootPhase
from .lifecycle import RuntimeLifecycle


class BootManager:
    """
    Canonical runtime composition engine.

    Responsible for:

        • manifest validation
        • dependency ordering
        • instance composition
        • topology registration
        • activation
        • topology sealing

    Responsible for everything that happens BEFORE
    runtime execution begins.
    """

    VERSION = "1.0.0"

    def __init__(
        self,
        manifest: RuntimeManifest,
    ) -> None:
        self.manifest = manifest
        self.validator = RuntimeManifestValidator()
        self.lifecycle = RuntimeLifecycle()
        self.registry = RuntimeTopologyRegistry()

        self._build_default_pipeline()

    def _build_default_pipeline(self) -> None:

        self.lifecycle.add(
            BootPhase.BOOTSTRAP,
            self._bootstrap,
        )

        self.lifecycle.add(
            BootPhase.COMPOSE,
            self._compose,
        )

        self.lifecycle.add(
            BootPhase.REGISTER,
            self._register,
        )

        self.lifecycle.add(
            BootPhase.RESOLVE_DEPENDENCIES,
            self._resolve,
        )

        self.lifecycle.add(
            BootPhase.VALIDATE,
            self._validate,
        )

        self.lifecycle.add(
            BootPhase.ACTIVATE,
            self._activate,
        )

        self.lifecycle.add(
            BootPhase.CERTIFY,
            self._certify,
        )

        self.lifecycle.add(
            BootPhase.READY,
            self._ready,
        )

    def boot(
        self,
        runtime: Any,
    ) -> RuntimeActivationResult:

        context = BootContext(runtime)

        for step in self.lifecycle.steps:

            context.transition(step.phase)

            try:
                step.action(context)

            except Exception as exc:
                context.fail(exc)
                raise

        snapshot = self.registry.seal()

        return RuntimeActivationResult(
            activated=True,
            certified=True,
            snapshot_version=snapshot.version,
        )

    #
    # phases
    #

    def _bootstrap(
        self,
        context: BootContext,
    ) -> None:
        self.validator.assert_valid(self.manifest)

    def _compose(
        self,
        context: BootContext,
    ) -> None:

        for entry in self.manifest.entries:

            instance = entry.factory(context.runtime)

            context.instances[entry.name] = instance

    def _register(
        self,
        context: BootContext,
    ) -> None:

        for entry in self.manifest.entries:

            instance = context.instances[entry.name]

            if entry.kind == "domain":

                self.registry.register_domain(
                    RuntimeDomain(
                        name=entry.name,
                        instance=instance,
                        version=entry.version,
                        dependencies=entry.dependencies,
                        capabilities=entry.capabilities,
                        required=entry.required,
                    )
                )

            elif entry.kind == "service":

                self.registry.register_service(
                    RuntimeService(
                        name=entry.name,
                        instance=instance,
                        version=entry.version,
                        dependencies=entry.dependencies,
                        capabilities=entry.capabilities,
                        required=entry.required,
                    )
                )

            elif entry.kind == "component":

                self.registry.register_component(
                    RuntimeComponent(
                        name=entry.name,
                        version=entry.version,
                        dependencies=entry.dependencies,
                        capabilities=entry.capabilities,
                        required=entry.required,
                        metadata=entry.metadata,
                    )
                )

            elif entry.kind == "provider":

                self.registry.register_provider(
                    entry.name,
                    instance,
                    dependencies=entry.dependencies,
                )

    def _resolve(
        self,
        context: BootContext,
    ) -> None:
        self.registry.boot_order()

    def _validate(
        self,
        context: BootContext,
    ) -> None:
        self.registry.validate()

    def _activate(
        self,
        context: BootContext,
    ) -> None:
        pass

    def _certify(
        self,
        context: BootContext,
    ) -> None:
        pass

    def _ready(
        self,
        context: BootContext,
    ) -> None:
        pass
