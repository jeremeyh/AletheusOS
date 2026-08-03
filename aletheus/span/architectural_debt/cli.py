from __future__ import annotations
from argparse import ArgumentParser
from json import dumps
from .engine import Engine
def main()->None:
    p=ArgumentParser(); p.add_argument("repository",nargs="?",default="."); a=p.parse_args(); print(dumps(Engine().analyze(a.repository),indent=2,sort_keys=True))
if __name__=="__main__": main()
