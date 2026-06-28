import re

class SerialDetector:
    """Detects serial numbering such as 5/10, 19/20, /99."""

    def detect(self, text: str = "") -> dict:
        text = text or ""

        full = re.search(r"\b(\d{1,4})\s*/\s*(\d{1,4})\b", text)
        if full:
            return {
                "serial_number": f"{full.group(1)}/{full.group(2)}",
                "print_run": int(full.group(2)),
                "confidence": 0.9,
            }

        run = re.search(r"(?<!\d)/\s*(\d{1,4})\b", text)
        if run:
            return {
                "serial_number": f"/{run.group(1)}",
                "print_run": int(run.group(1)),
                "confidence": 0.75,
            }

        return {"serial_number": "", "print_run": None, "confidence": 0.0}
