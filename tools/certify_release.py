from aletheus.release_certification import (
    ReleaseCertificationReporter,
    ReleaseCertificationService,
)


def main():
    cert = ReleaseCertificationService().certify()
    print(ReleaseCertificationReporter().render(cert))
    raise SystemExit(0 if cert.approved else 1)


if __name__ == "__main__":
    main()
