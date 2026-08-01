from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path


class AuthorityLedgerEngine:
    def __init__(
        self,
        catalog: Path,
        authority: Path,
        registry: Path,
        twin: Path,
        graph: Path,
        governance: Path,
        repo: Path,
        output: Path,
    ):
        self.paths = {
            "catalog": catalog,
            "authority": authority,
            "registry": registry,
            "twin": twin,
            "graph": graph,
            "governance": governance,
        }
        self.repo = repo
        self.output = output

    def build(self):
        data = {
            k: json.loads(v.read_text(encoding="utf-8")) for k, v in self.paths.items()
        }
        source = "\n".join(
            str(p.relative_to(self.repo)).lower() for p in self.repo.rglob("*.py")
        )
        modeled_text = (
            str(data["authority"])
            + str(data["registry"])
            + str(data["twin"])
            + str(data["graph"])
        ).lower()
        governed_text = str(data["governance"]).lower()
        rows = []
        claims = defaultdict(list)
        findings = []
        for item in data["catalog"].get("entries", []):
            tokens = [item["name"], *item.get("aliases", [])]
            norm = lambda x: "".join(c for c in x.lower() if c.isalnum())
            modeled = any(norm(t) in norm(modeled_text) for t in tokens if norm(t))
            implemented = any(norm(t) in norm(source) for t in tokens if norm(t))
            integrated = bool(item.get("mesh_connections")) and (implemented or modeled)
            governed = any(
                norm(t) in norm(governed_text) for t in tokens if norm(t)
            ) or bool(item.get("must_not_own"))
            realized = modeled and implemented and integrated and governed
            row = {
                **item,
                "defined": True,
                "modeled": modeled,
                "implemented": implemented,
                "integrated": integrated,
                "governed": governed,
                "realized": realized,
            }
            rows.append(row)
            claims[item["authority"].strip().lower()].append(item["name"])
            if implemented and not modeled:
                findings.append(
                    {
                        "code": "IMPLEMENTED_NOT_MODELED",
                        "severity": "high",
                        "subject": item["name"],
                    }
                )
            if modeled and not implemented:
                findings.append(
                    {
                        "code": "MODELED_NOT_IMPLEMENTED",
                        "severity": "medium",
                        "subject": item["name"],
                    }
                )
            if implemented and not integrated:
                findings.append(
                    {
                        "code": "IMPLEMENTED_NOT_INTEGRATED",
                        "severity": "high",
                        "subject": item["name"],
                    }
                )
        for claim, owners in claims.items():
            if claim and len(owners) > 1:
                findings.append(
                    {
                        "code": "DUPLICATE_AUTHORITY_STATEMENT",
                        "severity": "critical",
                        "subject": claim,
                        "evidence": owners,
                    }
                )
        counts = {
            k: sum(bool(r[k]) for r in rows)
            for k in (
                "defined",
                "modeled",
                "implemented",
                "integrated",
                "governed",
                "realized",
            )
        }
        report = {
            "generated_at": datetime.now(UTC).isoformat(),
            "entries": rows,
            "findings": findings,
            "maturity_counts": counts,
            "provenance": {k: str(v) for k, v in self.paths.items()},
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "constitutional-authority-ledger.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        (self.output / "realization-gaps.json").write_text(
            json.dumps(
                {"gaps": [r for r in rows if not r["realized"]]},
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        (self.output / "mesh-connection-matrix.json").write_text(
            json.dumps(
                {r["name"]: r["mesh_connections"] for r in rows},
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        (self.output / "authority-overlap-findings.json").write_text(
            json.dumps(
                {"findings": [f for f in findings if "DUPLICATE" in f["code"]]},
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        lines = [
            "# Constitutional Authority Ledger™",
            "",
            f"- Entries: **{len(rows)}**",
            f"- Realized: **{counts['realized']}**",
            f"- Findings: **{len(findings)}**",
            "",
        ]
        for r in rows:
            lines += [
                f"## {r['name']}",
                f"- Category: `{r['category']}`",
                f"- Parent: `{r['parent']}`",
                f"- Authority: {r['authority']}",
                f"- Modeled: **{r['modeled']}**",
                f"- Implemented: **{r['implemented']}**",
                f"- Integrated: **{r['integrated']}**",
                f"- Governed: **{r['governed']}**",
                f"- Realized: **{r['realized']}**",
                "",
            ]
        (self.output / "constitutional-authority-ledger.md").write_text(
            "\n".join(lines), encoding="utf-8"
        )
        return report
