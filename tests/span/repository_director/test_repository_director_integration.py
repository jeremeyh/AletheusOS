from pathlib import Path
from aletheus.span.repository_director.engine import Engine
def test_director(tmp_path:Path)->None:
    p=tmp_path/"aletheus"; p.mkdir(); (p/"__init__.py").write_text(""); (p/"runtime.py").write_text("ACTIVE=True\n")
    r=Engine().analyze(tmp_path); assert r["analysisCount"]==11 and r["constitutionalStatus"]=="VERIFIED" and r["spartanStatus"]=="ACTIVE" and r["humanAuthority"]=="PRESERVED" and r["executionAuthorized"] is False
