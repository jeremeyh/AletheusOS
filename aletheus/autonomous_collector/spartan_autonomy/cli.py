from .engine import Engine
from .models import Mission, Opportunity


def main() -> None:
    result = Engine().evaluate(
        Mission("mission-demo", "Find a scarce asset", 250.0),
        Opportunity("opp-demo", "asset-demo", "CARD_HAWK", 175.0, 225.0, 0.91),
    )
    print(result)


if __name__ == "__main__":
    main()
