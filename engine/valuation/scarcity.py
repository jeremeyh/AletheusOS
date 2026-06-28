def scarcity_score(serial_number: str = "", population: int | None = None) -> float:
    score = 50.0
    if "/" in str(serial_number):
        try:
            denom = int(str(serial_number).split("/")[-1])
            if denom <= 10:
                score += 35
            elif denom <= 25:
                score += 25
            elif denom <= 99:
                score += 12
        except Exception:
            pass
    if population is not None:
        if population <= 5:
            score += 15
        elif population <= 25:
            score += 8
    return min(score, 100.0)
