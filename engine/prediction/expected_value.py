def expected_value(outcomes: list[dict]) -> float:
    return round(
        sum(
            float(o.get("value", 0)) * float(o.get("probability", 0)) for o in outcomes
        ),
        2,
    )
