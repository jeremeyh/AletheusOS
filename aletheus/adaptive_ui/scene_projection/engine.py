from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, is_dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, ClassVar

from .models import LayoutNode, LayoutScene


class Engine:
    """Compile a render-neutral adaptive scene into a projection contract.

    Genesis 30.10 preserves semantic meaning, layout relationships,
    constitutional topology, adaptive density, and physics state while
    translating a scene into a target-specific projection description.

    The compiler does not perform final rendering. It emits the canonical
    projection contract consumed by renderer and reality adapters.
    """

    VERSION: ClassVar[str] = "30.10.0"

    SUPPORTED: ClassVar[frozenset[str]] = frozenset(
        {
            "API",
            "HTML",
            "JETPACK_COMPOSE",
            "PRESENTATION",
            "REPORT",
            "SPATIAL_XR",
            "SWIFTUI",
            "WEBGL",
            "WEBGPU",
        }
    )

    RENDER_PIPELINES: ClassVar[Mapping[str, str]] = MappingProxyType(
        {
            "API": "STRUCTURED_SEMANTIC_PAYLOAD",
            "HTML": "DOM_ADAPTIVE_PROJECTION",
            "JETPACK_COMPOSE": "ANDROID_NATIVE_COMPOSE",
            "PRESENTATION": "PRESENTATION_SCENE_PROJECTION",
            "REPORT": "DOCUMENT_SCENE_PROJECTION",
            "SPATIAL_XR": "IMMERSIVE_SPATIAL_PROJECTION",
            "SWIFTUI": "APPLE_NATIVE_DECLARATIVE",
            "WEBGL": "THREE_JS_WEBGL",
            "WEBGPU": "NATIVE_WEBGPU",
        }
    )

    TARGET_CAPABILITIES: ClassVar[Mapping[str, tuple[str, ...]]] = MappingProxyType(
        {
            "API": (
                "SEMANTIC_GRAPH",
                "STRUCTURED_DATA",
                "PROVENANCE_METADATA",
            ),
            "HTML": (
                "ACCESSIBLE_DOM",
                "RESPONSIVE_LAYOUT",
                "PROGRESSIVE_ENHANCEMENT",
            ),
            "JETPACK_COMPOSE": (
                "NATIVE_LAYOUT",
                "MATERIAL_ADAPTER",
                "DEVICE_AWARE_COMPOSITION",
            ),
            "PRESENTATION": (
                "SEQUENCED_SCENES",
                "STATIC_SNAPSHOT",
                "SEMANTIC_EQUIVALENCE",
            ),
            "REPORT": (
                "DOCUMENT_FLOW",
                "PRINT_LAYOUT",
                "PROVENANCE_PRESERVATION",
            ),
            "SPATIAL_XR": (
                "THREE_DIMENSIONAL_ANCHORS",
                "DEPTH",
                "IMMERSIVE_OVERLAYS",
            ),
            "SWIFTUI": (
                "NATIVE_LAYOUT",
                "ACCESSIBILITY",
                "DEVICE_AWARE_COMPOSITION",
            ),
            "WEBGL": (
                "THREE_DIMENSIONAL_SCENE",
                "CUSTOM_SHADERS",
                "SPRING_PHYSICS",
            ),
            "WEBGPU": (
                "GPU_COMPUTE",
                "CUSTOM_SHADERS",
                "HIGH_DENSITY_SPATIAL_RENDERING",
                "SPRING_PHYSICS",
            ),
        }
    )

    def compile(
        self,
        scene: LayoutScene,
        target: str,
        *,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
        device_pixel_ratio: float = 1.0,
    ) -> dict[str, Any]:
        """Compile a LayoutScene into a render-neutral projection payload.

        Args:
            scene: Canonical adaptive scene to project.
            target: Requested projection target.
            viewport_width: Physical or logical viewport width.
            viewport_height: Physical or logical viewport height.
            device_pixel_ratio: Projection density multiplier.

        Returns:
            A projection contract preserving semantic equivalence across
            supported display and output technologies.

        Raises:
            TypeError: If scene, target, or viewport inputs are invalid.
            ValueError: If the target or viewport configuration is invalid.
        """

        normalized_target = self._normalize_target(target)

        self._validate_scene(scene)
        self._validate_viewport(
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            device_pixel_ratio=device_pixel_ratio,
        )

        root_node = self._compile_node(scene.root)
        warnings = self._projection_warnings(
            scene=scene,
            target=normalized_target,
        )

        return {
            "compiler": {
                "name": "Scene Projection Compiler",
                "version": self.VERSION,
                "status": "COMPILED",
            },
            "sessionId": scene.session_id,
            "status": "compiled",
            "target": normalized_target,
            "projectionTarget": normalized_target,
            "projectionMode": "ADAPTIVE",
            "semanticEquivalence": "PRESERVED",
            "layoutIntegrity": "VERIFIED",
            "constitutionalIntegrity": "PRESERVED",
            "renderNeutral": True,
            "renderPipeline": self.RENDER_PIPELINES[normalized_target],
            "capabilities": self.TARGET_CAPABILITIES[normalized_target],
            "viewportHydration": {
                "width": viewport_width,
                "height": viewport_height,
                "devicePixelRatio": device_pixel_ratio,
                "logicalAspectRatio": viewport_width / viewport_height,
                "hydrationMode": "DECLARATIVE",
            },
            "adaptiveState": {
                "density": self._enum_value(scene.density),
                "cognitiveState": self._enum_value(scene.cognitive_state),
            },
            "physicsProfile": self._serialize(scene.physics),
            "spatialTopology": {
                "rootNodeId": scene.root.node_id,
                "topologicalState": self._enum_value(scene.root.topological_state),
                "coordinateModel": ("RENDER_NEUTRAL_SPATIAL_BOUNDS"),
                "depthEnabled": self._contains_depth(scene.root),
            },
            "layoutGraph": {
                "rootNode": root_node,
                "nodeCount": self._count_nodes(scene.root),
                "maximumDepth": self._maximum_depth(scene.root),
            },
            "projectionGraph": {
                "sourceRuntime": "ADAPTIVE_UI_WORKSPACE",
                "sourceSceneId": scene.session_id,
                "targetAdapter": normalized_target,
                "semanticEquivalence": "PRESERVED",
                "topologicalContinuity": "PRESERVED",
                "physicsContinuity": self._physics_continuity(normalized_target),
            },
            "metadata": self._serialize(scene.metadata),
            "warnings": warnings,
            "scene": scene,
        }

    def supports(self, target: str) -> bool:
        """Return whether a projection target is supported."""

        if not isinstance(target, str):
            return False

        return target.strip().upper() in self.SUPPORTED

    def describe_target(self, target: str) -> dict[str, Any]:
        """Return the immutable profile for a supported target."""

        normalized_target = self._normalize_target(target)

        return {
            "target": normalized_target,
            "renderPipeline": self.RENDER_PIPELINES[normalized_target],
            "capabilities": self.TARGET_CAPABILITIES[normalized_target],
            "semanticEquivalence": "REQUIRED",
            "renderNeutralInput": True,
        }

    def _compile_node(
        self,
        node: LayoutNode,
    ) -> dict[str, Any]:
        """Recursively compile a canonical layout node."""

        self._validate_node(node)

        return {
            "nodeId": node.node_id,
            "componentType": node.component_type,
            "topologicalState": self._enum_value(node.topological_state),
            "veracity": self._clamp(node.veracity),
            "opacity": self._clamp(node.opacity),
            "priority": self._clamp(node.priority),
            "spatialBounds": {
                "x": node.bounds.x,
                "y": node.bounds.y,
                "z": node.bounds.z,
                "width": node.bounds.width,
                "height": node.bounds.height,
                "depth": node.bounds.depth,
            },
            "adaptiveBehavior": {
                "minDensityVisibility": self._enum_value(
                    node.behavior.min_density_visibility
                ),
                "onCognitiveSpike": (node.behavior.on_cognitive_spike),
                "onHighIntentVelocity": (node.behavior.on_high_intent_velocity),
            },
            "metadata": self._serialize(node.metadata),
            "children": tuple(self._compile_node(child) for child in node.children),
        }

    def _projection_warnings(
        self,
        scene: LayoutScene,
        target: str,
    ) -> tuple[str, ...]:
        """Describe target degradations without changing scene meaning."""

        warnings: list[str] = []

        if target in {
            "HTML",
            "REPORT",
            "PRESENTATION",
            "API",
        } and self._contains_depth(scene.root):
            warnings.append("THREE_DIMENSIONAL_DEPTH_REQUIRES_" "SEMANTIC_FLATTENING")

        if target in {
            "REPORT",
            "PRESENTATION",
            "API",
        }:
            warnings.append("CONTINUOUS_PHYSICS_REPRESENTED_AS_" "STATE_SNAPSHOT")

        if target == "API":
            warnings.append("VISUAL_MATERIALS_REPRESENTED_AS_" "SEMANTIC_METADATA")

        return tuple(warnings)

    def _physics_continuity(
        self,
        target: str,
    ) -> str:
        executable_targets = {
            "WEBGPU",
            "WEBGL",
            "SPATIAL_XR",
            "SWIFTUI",
            "JETPACK_COMPOSE",
            "HTML",
        }

        if target in executable_targets:
            return "EXECUTABLE"

        return "SNAPSHOT_PRESERVED"

    def _contains_depth(
        self,
        node: LayoutNode,
    ) -> bool:
        if node.bounds.depth > 0 or node.bounds.z != 0:
            return True

        return any(self._contains_depth(child) for child in node.children)

    def _count_nodes(
        self,
        node: LayoutNode,
    ) -> int:
        return 1 + sum(self._count_nodes(child) for child in node.children)

    def _maximum_depth(
        self,
        node: LayoutNode,
        current_depth: int = 1,
    ) -> int:
        if not node.children:
            return current_depth

        return max(
            self._maximum_depth(
                child,
                current_depth + 1,
            )
            for child in node.children
        )

    def _normalize_target(
        self,
        target: str,
    ) -> str:
        if not isinstance(target, str):
            raise TypeError("Projection target must be a string.")

        normalized_target = target.strip().upper()

        if not normalized_target:
            raise ValueError("Projection target cannot be empty.")

        if normalized_target not in self.SUPPORTED:
            supported = ", ".join(sorted(self.SUPPORTED))
            raise ValueError(
                f"Unsupported projection target: {target}. "
                f"Supported targets: {supported}"
            )

        return normalized_target

    @staticmethod
    def _validate_scene(
        scene: LayoutScene,
    ) -> None:
        if not isinstance(scene, LayoutScene):
            raise TypeError("scene must be a LayoutScene instance.")

        if not isinstance(scene.session_id, str):
            raise TypeError("scene.session_id must be a string.")

        if not scene.session_id.strip():
            raise ValueError("scene.session_id cannot be empty.")

        if not isinstance(scene.root, LayoutNode):
            raise TypeError("scene.root must be a LayoutNode instance.")

    @staticmethod
    def _validate_node(
        node: LayoutNode,
    ) -> None:
        if not isinstance(node, LayoutNode):
            raise TypeError("Every projected node must be a LayoutNode.")

        if not node.node_id.strip():
            raise ValueError("LayoutNode.node_id cannot be empty.")

        if not node.component_type.strip():
            raise ValueError("LayoutNode.component_type cannot be empty.")

        if node.bounds.width < 0:
            raise ValueError("LayoutNode width cannot be negative.")

        if node.bounds.height < 0:
            raise ValueError("LayoutNode height cannot be negative.")

        if node.bounds.depth < 0:
            raise ValueError("LayoutNode depth cannot be negative.")

    @staticmethod
    def _validate_viewport(
        *,
        viewport_width: int,
        viewport_height: int,
        device_pixel_ratio: float,
    ) -> None:
        if isinstance(viewport_width, bool) or not isinstance(
            viewport_width,
            int,
        ):
            raise TypeError("viewport_width must be an integer.")

        if isinstance(viewport_height, bool) or not isinstance(
            viewport_height,
            int,
        ):
            raise TypeError("viewport_height must be an integer.")

        if isinstance(device_pixel_ratio, bool) or not isinstance(
            device_pixel_ratio,
            (int, float),
        ):
            raise TypeError("device_pixel_ratio must be numeric.")

        if viewport_width <= 0:
            raise ValueError("viewport_width must be greater than zero.")

        if viewport_height <= 0:
            raise ValueError("viewport_height must be greater than zero.")

        if device_pixel_ratio <= 0:
            raise ValueError("device_pixel_ratio must be greater than zero.")

    @staticmethod
    def _clamp(
        value: float,
    ) -> float:
        return max(
            0.0,
            min(
                1.0,
                float(value),
            ),
        )

    @classmethod
    def _serialize(
        cls,
        value: Any,
    ) -> Any:
        if is_dataclass(value) and not isinstance(
            value,
            type,
        ):
            return {key: cls._serialize(item) for key, item in asdict(value).items()}

        if isinstance(value, Enum):
            return value.value

        if isinstance(value, Mapping):
            return {str(key): cls._serialize(item) for key, item in value.items()}

        if isinstance(value, tuple):
            return tuple(cls._serialize(item) for item in value)

        if isinstance(value, list):
            return [cls._serialize(item) for item in value]

        if isinstance(value, set):
            return tuple(
                cls._serialize(item)
                for item in sorted(
                    value,
                    key=str,
                )
            )

        if (
            isinstance(
                value,
                (
                    str,
                    int,
                    float,
                    bool,
                ),
            )
            or value is None
        ):
            return value

        return str(value)

    @staticmethod
    def _enum_value(
        value: Any,
    ) -> str:
        if isinstance(value, Enum):
            return str(value.value)

        return str(value)
