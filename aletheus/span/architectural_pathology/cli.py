from __future__ import annotations

from argparse import ArgumentParser
from json import dumps

from .engine import Engine


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("repository", nargs="?", default=".")
    args = parser.parse_args()
    print(dumps(Engine().analyze(args.repository), indent=2, sort_keys=True))
