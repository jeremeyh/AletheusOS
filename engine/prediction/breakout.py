def breakout_probability(signals: dict) -> float:
    base = 0.25
    base += 0.20 if signals.get("playing_time") == "rising" else 0
    base += 0.20 if signals.get("market_velocity") == "rising" else 0
    base += 0.15 if signals.get("team_context") == "strong" else 0
    return round(min(base, 0.95), 3)
