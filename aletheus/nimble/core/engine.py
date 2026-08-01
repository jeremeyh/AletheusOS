from __future__ import annotations

import json
from pathlib import Path

from .models import PrimitiveDefinition, ValidationResult


class Engine:
    CONSTITUTIONAL_LAYERS = (
        "structure",
        "typography",
        "interaction",
        "visualization",
        "constitutional",
        "engine_instruments",
    )

    def validate(self, primitives: tuple[PrimitiveDefinition, ...]) -> ValidationResult:
        findings = []
        names = set()
        for primitive in primitives:
            if primitive.name in names:
                findings.append(f"duplicate primitive: {primitive.name}")
            names.add(primitive.name)
            if primitive.layer not in self.CONSTITUTIONAL_LAYERS:
                findings.append(
                    f"invalid layer for {primitive.name}: {primitive.layer}"
                )
            if primitive.reserved and primitive.layer != "constitutional":
                findings.append(
                    f"reserved primitive outside constitutional layer: {primitive.name}"
                )
        return ValidationResult(not findings, tuple(findings))

    def write_catalog(
        self, primitives: tuple[PrimitiveDefinition, ...], output: Path
    ) -> Path:
        result = self.validate(primitives)
        payload = {
            "runtime": "Nimble",
            "library": "Primitive Experience Library",
            "valid": result.valid,
            "findings": list(result.findings),
            "primitives": [item.to_dict() for item in primitives],
        }
        output.mkdir(parents=True, exist_ok=True)
        target = output / "primitive-experience-library.json"
        target.write_text(
            json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
        )
        return target
