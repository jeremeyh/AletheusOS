import subprocess, sys
subprocess.run([sys.executable, "-m", "streamlit", "run", "ui/pages/aletheus_founder_console.py"], check=True)
