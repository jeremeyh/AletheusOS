from __future__ import annotations

from .models import Experience


class Engine:
    def chunks(
        self, experience: Experience, *, chunk_size: int = 2
    ) -> tuple[dict[str, object], ...]:
        nodes = list(experience.root.children)
        total = max(1, (len(nodes) + chunk_size - 1) // chunk_size)
        out = []
        for i in range(total):
            out.append(
                {
                    "experienceId": experience.experience_id,
                    "stream": {
                        "chunk": i + 1,
                        "totalChunks": total,
                        "complete": i + 1 == total,
                    },
                    "nodes": [
                        n.to_dict()
                        for n in nodes[i * chunk_size : (i + 1) * chunk_size]
                    ],
                }
            )
        return tuple(out)
