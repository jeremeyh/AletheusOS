from __future__ import annotations

from pprint import pprint

from aletheus.execution_engine import execution_engine


def main():
    record = execution_engine.execute(
        identity="identity.founder.master_lord_6ixth",
        application="CardHawk",
        query="What is my Caleb Williams Bowman worth?",
    )

    print("CARDHAWK PROOF WORKFLOW 001")
    print("=" * 50)
    print()
    pprint(record.to_dict())


if __name__ == "__main__":
    main()
