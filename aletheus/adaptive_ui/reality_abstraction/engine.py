from __future__ import annotations

from types import MappingProxyType
from typing import ClassVar


class Engine:
    ADAPTERS: ClassVar[dict[str, str]] = MappingProxyType(
        {
            "HTML": "DOMProjectionAdapter",
            "WEBGL": "ThreeJSProjectionAdapter",
            "WEBGPU": "WebGPUProjectionAdapter",
            "SWIFTUI": "SwiftUIProjectionAdapter",
            "JETPACK_COMPOSE": "JetpackComposeProjectionAdapter",
            "SPATIAL_XR": "SpatialRealityAdapter",
            "LIGHT_FIELD": "FutureLightFieldAdapter",
            "PROGRAMMABLE_MATTER": "FutureProgrammableMatterAdapter",
        }
    )

    def adapter_for(self, target: str) -> str:
        target = target.upper()

        try:
            return self.ADAPTERS[target]
        except KeyError as exc:
            supported = ", ".join(sorted(self.ADAPTERS))
            raise ValueError(
                f"Unsupported reality adapter '{target}'. "
                f"Supported targets: {supported}"
            ) from exc
