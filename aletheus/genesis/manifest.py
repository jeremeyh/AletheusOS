from __future__ import annotations

from .models import GenesisPackageSpec


def build_manifest(spec: GenesisPackageSpec) -> dict:
    return {
        "genesis_package": spec.gp_id,
        "title": spec.title,
        "classification": spec.classification.value,
        "authority": spec.authority,
        "family": spec.family,
        "risk": spec.risk.value,
        "depends_on": spec.depends_on,
        "adds": spec.files_to_add,
        "modifies": spec.files_to_modify,
        "deletes": spec.files_to_delete,
        "adr": spec.adr,
        "collision_check": "REQUIRED",
        "watch_tower": "REQUIRED",
        "repository_dna": "READY_TO_RECORD",
        "ontology": "READY_TO_REGISTER",
    }
