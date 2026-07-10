from __future__ import annotations

from pathlib import Path


ASSET_DIRECTORY = Path(
    "nimble/apps/platform-shell/dist/assets"
)

FORBIDDEN_PRIMARY_SIGNATURES = {
    "command surface": (
        "Governed command gateway",
    ),
    "command history": (
        "Command audit history",
    ),
    "OIDC callback": (
        "Completing secure sign-in",
    ),
    "OIDC protocol": (
        "signinRedirectCallback",
    ),
}


def main() -> int:
    assets = sorted(
        ASSET_DIRECTORY.glob("*.js")
    )

    if not assets:
        print(
            "FAIL: No production JavaScript assets found. "
            "Run the Nimble build first."
        )
        return 1

    primary_candidates = [
        path
        for path in assets
        if path.name.startswith("index-")
    ]

    if not primary_candidates:
        print(
            "FAIL: No primary index chunk found."
        )
        return 1

    primary = max(
        primary_candidates,
        key=lambda path: path.stat().st_size,
    )

    primary_text = primary.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    failures: list[str] = []

    for label, signatures in (
        FORBIDDEN_PRIMARY_SIGNATURES.items()
    ):
        if any(
            signature in primary_text
            for signature in signatures
        ):
            failures.append(
                f"{label} remains in the primary chunk"
            )

    secondary = [
        path
        for path in assets
        if path != primary
    ]

    if len(secondary) < 3:
        failures.append(
            "fewer than three secondary chunks were emitted"
        )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print(
        "PASS: Nimble route splitting is valid."
    )
    print(
        "Primary:",
        primary,
        f"({primary.stat().st_size} bytes)",
    )
    print(
        "Secondary chunks:",
        len(secondary),
    )

    for path in secondary:
        print(
            "-",
            path,
            f"({path.stat().st_size} bytes)",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
