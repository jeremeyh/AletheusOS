import {
  useAuthentication,
} from "../providers/AuthenticationProvider";

export function AuthenticationPanel() {
  const authentication =
    useAuthentication();

  if (
    authentication.isPending
    || authentication.mode !== "oidc"
  ) {
    return null;
  }

  if (authentication.authenticated) {
    return (
      <button
        className="nimble-button nimble-button--secondary"
        type="button"
        onClick={() => {
          void authentication.signOut();
        }}
      >
        Sign out
      </button>
    );
  }

  return (
    <button
      className="nimble-button nimble-button--primary"
      type="button"
      disabled={
        authentication.session.state
        === "authenticating"
      }
      onClick={() => {
        void authentication.signIn();
      }}
    >
      {authentication.session.state
        === "authenticating"
        ? "Redirecting…"
        : "Sign in"}
    </button>
  );
}
