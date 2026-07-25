from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
def check(): return (ROOT/'tests/architecture').exists()
