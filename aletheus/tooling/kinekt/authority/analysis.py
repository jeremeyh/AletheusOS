from __future__ import annotations

from collections import defaultdict
from typing import Any

from .models import AuthorityFinding, CapabilityAuthority


def parse_authorities(registry: dict[str, Any]) -> list[CapabilityAuthority]:
    raw = registry.get("capabilities", [])
    if not isinstance(raw, list):
        raise TypeError("Authority registry capabilities must be a list.")
    return [
        CapabilityAuthority(
            name=str(i["name"]),
            runtime_role=str(i["runtime_role"]),
            module_prefixes=tuple(map(str, i.get("module_prefixes", []))),
            owns=tuple(map(str, i.get("owns", []))),
            consumes=tuple(map(str, i.get("consumes", []))),
            produces=tuple(map(str, i.get("produces", []))),
            delegates_to=tuple(map(str, i.get("delegates_to", []))),
            must_not_own=tuple(map(str, i.get("must_not_own", []))),
        )
        for i in raw
        if isinstance(i, dict)
    ]


def assign_modules(twin: dict[str, Any], authorities: list[CapabilityAuthority]):
    assignments = {}
    unresolved = []
    findings = []
    for node in twin.get("nodes", []):
        if not isinstance(node, dict) or node.get("node_type") != "module":
            continue
        name = str(node.get("name", ""))
        matches = [
            a.name
            for a in authorities
            if any(name == p or name.startswith(p + ".") for p in a.module_prefixes)
        ]
        if len(matches) == 1:
            assignments[name] = matches[0]
        elif len(matches) > 1:
            findings.append(
                AuthorityFinding(
                    "MULTIPLE_MODULE_AUTHORITIES",
                    "high",
                    name,
                    "Module matches multiple declared capability authorities.",
                    tuple(matches),
                )
            )
        else:
            unresolved.append(name)
    return assignments, sorted(unresolved), findings


def detect_claim_overlaps(
    authorities: list[CapabilityAuthority],
) -> list[AuthorityFinding]:
    claims = defaultdict(list)
    for a in authorities:
        for c in a.owns:
            claims[c.casefold()].append(a.name)
    findings = []
    for claim, owners in sorted(claims.items()):
        if len(owners) > 1:
            findings.append(
                AuthorityFinding(
                    "SOVEREIGN_AUTHORITY_OVERLAP",
                    "critical",
                    claim,
                    "Multiple capabilities claim the same sovereign responsibility.",
                    tuple(sorted(owners)),
                )
            )
    return findings
