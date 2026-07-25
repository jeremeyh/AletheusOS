from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
def check(): return all((ROOT/p).exists() for p in ['docs','tools','tests'])
