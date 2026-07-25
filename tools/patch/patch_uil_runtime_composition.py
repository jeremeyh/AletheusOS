import re
from pathlib import Path

CORE_PATH = Path("aletheus/runtime/core.py")
UIL_REGISTRATION_PATH = Path(
    "aletheus/runtime/registrations/uil_commands.py"
)


def compose_uil_into_runtime() -> None:
    text = CORE_PATH.read_text(encoding="utf-8")

    import_block = (
        "from aletheus.runtime.adapters."
        "universal_intelligence_adapter import (\n"
        "    UniversalIntelligenceAdapter,\n"
        ")\n"
    )

    if import_block not in text:
        prediction_import = re.search(
            r"^from aletheus\.runtime\.adapters"
            r"\.prediction_adapter import .+$",
            text,
            flags=re.MULTILINE,
        )

        if prediction_import is not None:
            insert_at = prediction_import.start()
            text = (
                text[:insert_at]
                + import_block
                + text[insert_at:]
            )
        else:
            first_runtime_import = re.search(
                r"^from aletheus\.runtime\.",
                text,
                flags=re.MULTILINE,
            )

            if first_runtime_import is None:
                raise RuntimeError(
                    "Could not locate the runtime import section."
                )

            insert_at = first_runtime_import.start()
            text = (
                text[:insert_at]
                + import_block
                + text[insert_at:]
            )

    assignment = (
        "        self.uil = "
        "UniversalIntelligenceAdapter(self)\n"
    )

    if assignment not in text:
        anchors = []

        for pattern in (
            r"^[ \t]+self\.workspace\s*=.*$",
            r"^[ \t]+self\.executive\s*=.*$",
            r"^[ \t]+self\.semantic\s*=.*$",
            r"^[ \t]+self\.reasoning\s*=.*$",
            r"^[ \t]+self\.memory\s*=.*$",
            r"^[ \t]+self\.events\s*=.*$",
        ):
            for match in re.finditer(
                pattern,
                text,
                flags=re.MULTILINE,
            ):
                anchors.append(match)

        if not anchors:
            raise RuntimeError(
                "Could not locate a runtime service "
                "composition anchor."
            )

        anchor = max(
            anchors,
            key=lambda item: item.end(),
        )

        line_end = text.find("\n", anchor.end())

        if line_end == -1:
            line_end = len(text)
            suffix = "\n"
        else:
            line_end += 1
            suffix = ""

        text = (
            text[:line_end]
            + suffix
            + assignment
            + text[line_end:]
        )

    CORE_PATH.write_text(
        text,
        encoding="utf-8",
    )

    print(
        "UIL adapter composed into runtime/core.py."
    )


def simplify_uil_registrar() -> None:
    text = UIL_REGISTRATION_PATH.read_text(
        encoding="utf-8",
    )

    text = re.sub(
        r"\nfrom aletheus\.runtime\.adapters"
        r"\.universal_intelligence_adapter import \(\n"
        r"\s+UniversalIntelligenceAdapter,\n"
        r"\)\n",
        "\n",
        text,
        count=1,
    )

    text = re.sub(
        r"\n\s+if not hasattr\(runtime,\s*[\"']uil[\"']\):\n"
        r"\s+runtime\.uil\s*=\s*"
        r"UniversalIntelligenceAdapter\(runtime\)\n",
        "\n",
        text,
        count=1,
    )

    if "uil = runtime.uil" not in text:
        marker = "    commands = runtime.commands\n"

        if marker not in text:
            raise RuntimeError(
                "Could not locate the UIL registrar "
                "command binding anchor."
            )

        text = text.replace(
            marker,
            marker + "    uil = runtime.uil\n",
            1,
        )

    UIL_REGISTRATION_PATH.write_text(
        text,
        encoding="utf-8",
    )

    print(
        "UIL registrar reduced to command binding only."
    )


def validate() -> None:
    core_text = CORE_PATH.read_text(
        encoding="utf-8",
    )
    registration_text = (
        UIL_REGISTRATION_PATH.read_text(
            encoding="utf-8",
        )
    )

    required_core_fragments = (
        "UniversalIntelligenceAdapter",
        "self.uil = UniversalIntelligenceAdapter(self)",
    )

    for fragment in required_core_fragments:
        if fragment not in core_text:
            raise RuntimeError(
                f"Missing runtime composition fragment: "
                f"{fragment}"
            )

    forbidden_registration_fragments = (
        "if not hasattr(runtime, \"uil\")",
        "if not hasattr(runtime, 'uil')",
        "runtime.uil = UniversalIntelligenceAdapter(runtime)",
    )

    for fragment in forbidden_registration_fragments:
        if fragment in registration_text:
            raise RuntimeError(
                f"UIL registrar still creates the service: "
                f"{fragment}"
            )

    if "uil = runtime.uil" not in registration_text:
        raise RuntimeError(
            "UIL registrar does not bind the composed service."
        )

    print("UIL composition validation passed.")


def main() -> None:
    if not CORE_PATH.exists():
        raise FileNotFoundError(CORE_PATH)

    if not UIL_REGISTRATION_PATH.exists():
        raise FileNotFoundError(
            UIL_REGISTRATION_PATH
        )

    compose_uil_into_runtime()
    simplify_uil_registrar()
    validate()


if __name__ == "__main__":
    main()
