import {
  useEffect,
  useState,
} from "react";
import {
  useNavigate,
} from "react-router";

import {
  oidcBrowserSession,
} from "../api/oidcSession";

export function OidcCallbackRoute() {
  const navigate = useNavigate();

  const [failure, setFailure] =
    useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function completeCallback() {
      try {
        await oidcBrowserSession
          .handleCallback();

        if (active) {
          navigate("/", {
            replace: true,
          });
        }
      } catch (error) {
        if (active) {
          setFailure(
            error instanceof Error
              ? error.message
              : String(error),
          );
        }
      }
    }

    void completeCallback();

    return () => {
      active = false;
    };
  }, [navigate]);

  if (failure) {
    return (
      <main
        id="nimble-main"
        className="nimble-main"
      >
        <section className="nimble-auth-callback">
          <p className="nimble-panel__eyebrow">
            Authentication failure
          </p>

          <h1>Sign-in could not be completed</h1>

          <p>{failure}</p>

          <button
            className="nimble-button nimble-button--primary"
            type="button"
            onClick={() => {
              void oidcBrowserSession.signIn();
            }}
          >
            Try sign-in again
          </button>
        </section>
      </main>
    );
  }

  return (
    <main
      id="nimble-main"
      className="nimble-main"
    >
      <section className="nimble-auth-callback">
        <span
          className="nimble-auth-callback__spinner"
          aria-hidden="true"
        >
          ✦
        </span>

        <h1>Completing secure sign-in</h1>

        <p>
          Validating the OIDC response and restoring
          the Nimble session.
        </p>
      </section>
    </main>
  );
}
