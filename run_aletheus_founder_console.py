import subprocess
import sys

subprocess.run(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "pages/founder_console.py",
    ],
    check=True,
)