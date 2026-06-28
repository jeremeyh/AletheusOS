def detect_market_signals(metrics: dict) -> list[str]:
    signals = []
    if metrics.get("price_drop_pct", 0) >= 15:
        signals.append("PRICE_DROP")
    if metrics.get("sold_velocity", 0) >= 5:
        signals.append("HIGH_VELOCITY")
    return signals
