from __future__ import annotations

from pathlib import Path


ASSET_DIRECTORY = Path(
    "nimble/apps/platform-shell/dist/assets"
)


def main() -> int:
    if not ASSET_DIRECTORY.exists():
        print(
            "FAIL: Nimble production assets do not exist. "
            "Run npm run build first."
        )
        return 1

    javascript_files = sorted(
        ASSET_DIRECTORY.glob("*.js")
    )

    if len(javascript_files) < 2:
        print(
            "FAIL: Expected at least two JavaScript "
            "chunks after OIDC isolation."
        )
        return 1

    primary_files = [
        path
        for path in javascript_files
        if path.name.startswith("index-")
    ]

    if not primary_files:
        print(
            "FAIL: Could not locate the primary "
            "Nimble JavaScript entry."
        )
        return 1

    primary = max(
        primary_files,
        key=lambda path: path.stat().st_size,
    )

    oidc_signature = (
        "signinRedirectCallback"
    )

    primary_text = primary.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    if oidc_signature in primary_text:
        print(
            "FAIL: OIDC implementation remains "
            "inside the primary shell chunk."
        )
        return 1

    oidc_chunks = [
        path
        for path in javascript_files
        if oidc_signature
        in path.read_text(
            encoding="utf-8",
            errors="ignore",
        )
    ]

    if not oidc_chunks:
        print(
            "FAIL: Could not identify the lazy "
            "OIDC implementation chunk."
        )
        return 1

    print("PASS: Nimble bundle boundary is valid.")
    print(
        "Primary:",
        primary,
        f"({primary.stat().st_size} bytes)",
    )

    for chunk in oidc_chunks:
        print(
            "OIDC lazy chunk:",
            chunk,
            f"({chunk.stat().st_size} bytes)",
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
