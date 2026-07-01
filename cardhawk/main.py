"""
Card Hawk Desktop Application

Version 4.0.0
"""

from cardhawk.app import CardHawkApplication


def main():

    app = CardHawkApplication()

    state = app.startup()

    print("=" * 60)
    print("Card Hawk")
    print("=" * 60)
    print()

    print(f"Version : {state['version']}")
    print(f"Assets  : {state['asset_count']}")
    print()

    print("Portfolio")
    print(state["portfolio"])
    print()

    print("Analytics")
    print(state["analytics"])


if __name__ == "__main__":
    main()
