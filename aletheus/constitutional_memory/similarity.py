from __future__ import annotations


class ConstitutionalSimilarityEngine:
    GENESIS = "19.5"
    VERSION = "0.1.0"

    def score(self, query_terms: list[str], record: dict):
        haystack = set(
            [
                *record.get("tags", []),
                *record.get("keywords", []),
                *record.get("entities", []),
                record.get("application", ""),
                record.get("relix_profile", ""),
                record.get("recommendation", ""),
            ]
        )

        query = set(query_terms)

        if not query:
            return 0.0

        overlap = query.intersection(haystack)

        return round(len(overlap) / len(query), 4)

    def search(self, query_terms: list[str], records: list[dict], limit: int = 10):
        scored = []

        for record in records:
            score = self.score(query_terms, record)

            if score > 0:
                scored.append(
                    {
                        "similarity": score,
                        "record": record,
                    }
                )

        scored.sort(
            key=lambda item: item["similarity"],
            reverse=True,
        )

        return scored[:limit]


constitutional_similarity_engine = ConstitutionalSimilarityEngine()
