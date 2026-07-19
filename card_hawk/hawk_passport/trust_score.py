def calculate_trust_score(*, has_identity: bool, has_owner: bool, authenticity: str, provenance_count: int, transfer_count: int) -> int:
    score = (20 if has_identity else 0) + (20 if has_owner else 0)
    score += {"verified": 35, "review": 15, "unverified": 0, "rejected": -35}[authenticity]
    score += min(provenance_count * 5, 15) + min(transfer_count * 2, 10)
    return max(0, min(score, 100))
