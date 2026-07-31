"""
Card Hawk Command Console
Powered by AletheusOS™

Internal Runtime Preview
"""

from card_hawk.acquisition_v2.engine import AutonomousAcquisitionEngine
from card_hawk.assistant.engine import IntelligenceAssistantEngine
from card_hawk.community.engine import CommunityIntelligenceEngine
from card_hawk.marketplace_intelligence.engine import MarketplaceIntelligenceEngine
from card_hawk.portfolio_v2.engine import PortfolioIntelligenceEngine
from card_hawk.runtime.engine import CardHawkRuntime


def banner():

    print("""
================================================

              CARD HAWK™

        Powered by AletheusOS™

       Intelligence Command Console

================================================
""")


def main():

    banner()

    runtime = CardHawkRuntime()

    print("BOOTING RUNTIME...")
    print(runtime.initialize())

    print()

    systems = {
        "Community Intelligence": CommunityIntelligenceEngine(),
        "Marketplace Intelligence": MarketplaceIntelligenceEngine(),
        "Autonomous Acquisition": AutonomousAcquisitionEngine(),
        "Portfolio Intelligence": PortfolioIntelligenceEngine(),
        "AI Assistant": IntelligenceAssistantEngine(),
    }

    print("SYSTEM STATUS")
    print("------------------------------")

    for name, engine in systems.items():
        print(f"✓ {name}: ONLINE")

    print("""
        
------------------------------------------------

AVAILABLE COMMANDS:

1. Portfolio Overview
2. Market Scan
3. Acquisition Review
4. Ask Card Hawk
5. Community Intelligence
6. Runtime Status
7. Exit

------------------------------------------------
""")

    while True:
        choice = input("CARD HAWK > ")

        if choice == "1":
            print(
                systems["Portfolio Intelligence"].analyze_portfolio(
                    "Current Collection"
                )
            )

        elif choice == "2":
            print(systems["Marketplace Intelligence"].scan_market())

        elif choice == "3":
            print(
                systems["Autonomous Acquisition"].evaluate_target(
                    "Premium Rookie Auto /25"
                )
            )

        elif choice == "4":
            request = input("Ask Card Hawk: ")

            print(systems["AI Assistant"].process_request(request))

        elif choice == "5":
            print(systems["Community Intelligence"].initialize())

        elif choice == "6":
            print(runtime.health_check())

        elif choice == "7":
            print("Card Hawk shutting down...")

            break

        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
