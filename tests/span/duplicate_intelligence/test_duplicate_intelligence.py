from pathlib import Path
from aletheus.span.duplicate_intelligence.engine import Engine
def test_duplicate_intelligence(tmp_path:Path)->None:
    p=tmp_path/"pkg"; p.mkdir(); (p/"__init__.py").write_text(""); (p/"engine.py").write_text("VALUE = 1\n")
    a=Engine().analyze(tmp_path); b=Engine().analyze(tmp_path)
    assert a==b and a["humanAuthority"]=="PRESERVED" and a["executionAuthorized"] is False and a["digest"]
