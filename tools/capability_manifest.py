from aletheus.capability_manifest import (
    CapabilityManifest,
    CapabilityManifestRegistry,
    CapabilityManifestReporter,
)


def main():

    registry = CapabilityManifestRegistry()

    registry.register(
        CapabilityManifest(
            id="runtime.health",
            name="Runtime Health",
            provider="Platform Intelligence",
            capability_type="service",
            interfaces=["PlatformService"],
            provides=["runtime.health"],
        )
    )

    registry.register(
        CapabilityManifest(
            id="runtime.snapshot",
            name="Runtime Snapshot",
            provider="Platform Intelligence",
            capability_type="service",
            interfaces=["PlatformService"],
            requires=["runtime.health"],
            provides=["runtime.snapshot"],
        )
    )

    print(
        CapabilityManifestReporter().render(
            registry
        )
    )


if __name__ == "__main__":
    main()
