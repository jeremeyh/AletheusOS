from __future__ import annotations

from collections import defaultdict


class Engine:
    def find_triangles(
        self, edges: list[tuple[str, str, float]], limits: dict[str, float]
    ) -> tuple[dict[str, object], ...]:
        g = defaultdict(list)
        for a, b, v in edges:
            g[a].append((b, float(v)))
        out = []
        seen = set()
        for a, abes in g.items():
            for b, va in abes:
                for c, vb in g.get(b, []):
                    if c in {a, b}:
                        continue
                    for back, vc in g.get(c, []):
                        if back != a:
                            continue
                        key = tuple(sorted((a, b, c)))
                        if key in seen:
                            continue
                        adj = {
                            a: round(vc - va, 6),
                            b: round(va - vb, 6),
                            c: round(vb - vc, 6),
                        }
                        if any(abs(x) > limits.get(u, 0.0) for u, x in adj.items()):
                            continue
                        seen.add(key)
                        out.append({"participants": (a, b, c), "cashAdjustments": adj})
        return tuple(out)
