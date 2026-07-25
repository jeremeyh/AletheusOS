import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
def check():
 p=subprocess.run(['git','status','--porcelain'],cwd=ROOT,capture_output=True,text=True);return p.returncode==0
