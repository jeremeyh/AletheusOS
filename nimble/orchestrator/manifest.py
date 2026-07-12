from __future__ import annotations

from .models import CapabilityDefinition


CAPABILITIES: tuple[CapabilityDefinition, ...] = (
    CapabilityDefinition(
        capability_id="experience-constitution",
        display_name="Experience Constitution™",
        required_paths=(
            "aletheus/constitution/ARCHITECTURAL_CONSTITUTION.md",
            "aletheus/constitution/EXPERIENCE_EVOLUTION.md",
            "aletheus/constitution/FOUNDERS_VISION.md",
        ),
        constitutional=True,
    ),
    CapabilityDefinition(
        capability_id="experience-core",
        display_name="Experience Core™",
        required_paths=(
            "nimble/packages/core/src/experience/contracts.ts",
            "nimble/packages/core/src/experience/index.ts",
            "nimble/packages/core/src/experience/tokens/index.ts",
            "nimble/packages/core/src/experience/theme/index.ts",
            "validate_nimble_experience_core.py",
            "tests/nimble/test_experience_core.py",
        ),
        dependencies=("experience-constitution",),
        constitutional=True,
    ),
    CapabilityDefinition(
        capability_id="react-primitives",
        display_name="Primitive Experience Library™",
        required_paths=(
            "nimble/packages/react/src/primitives/Surface.tsx",
            "nimble/packages/react/src/primitives/Stack.tsx",
            "nimble/packages/react/src/primitives/Grid.tsx",
            "nimble/packages/react/src/primitives/Text.tsx",
            "nimble/packages/react/src/primitives/Instrument.tsx",
            "nimble/packages/react/src/primitives/reserved.tsx",
            "validate_nimble_primitive_experience.py",
            "tests/nimble/test_primitive_experience.py",
        ),
        dependencies=("experience-core",),
    ),
    CapabilityDefinition(
        capability_id="workspace-engine",
        display_name="Workspace Engine™",
        required_paths=(
            "nimble/packages/workspace/src/engine/contracts.ts",
            "nimble/packages/workspace/src/engine/founder.ts",
            "nimble/packages/workspace/src/engine/layout.ts",
            "nimble/packages/workspace/src/engine/registry.ts",
            "nimble/packages/workspace/src/engine/persistence.ts",
            "validate_nimble_workspace_engine.py",
            "tests/nimble/test_workspace_engine.py",
        ),
        dependencies=("experience-core",),
    ),
    CapabilityDefinition(
        capability_id="instrumentation-preview",
        display_name="Intelligence Instrumentation™ Preview",
        required_paths=(
            "nimble/apps/platform-shell/instrumentation.html",
            "nimble/apps/platform-shell/src/instrumentation-preview.tsx",
            "nimble/apps/platform-shell/src/nimble/showcase/IntelligenceInstrumentationShowcase.tsx",
            "validate_nimble_instrumentation_preview.py",
            "tests/nimble/test_instrumentation_preview.py",
        ),
        dependencies=("react-primitives",),
    ),
    CapabilityDefinition(
        capability_id="founder-console",
        display_name="Founder Console™",
        required_paths=(
            "nimble/apps/platform-shell/founder-console.html",
            "nimble/apps/platform-shell/src/founder-console.tsx",
            "nimble/apps/platform-shell/src/nimble/founder-console/FounderConsoleShell.tsx",
            "validate_nimble_founder_console_shell.py",
            "tests/nimble/test_founder_console_shell.py",
        ),
        dependencies=(
            "react-primitives",
            "workspace-engine",
        ),
    ),
)
