import {
  isRouteErrorResponse,
  useRouteError,
} from "react-router";

export function RouteError() {
  const error =
    useRouteError();

  let title =
    "The route could not be rendered";

  let detail =
    "An unexpected route failure occurred.";

  if (isRouteErrorResponse(error)) {
    title =
      `${error.status} ${error.statusText}`;

    detail =
      typeof error.data === "string"
        ? error.data
        : JSON.stringify(
            error.data,
            null,
            2,
          );
  } else if (error instanceof Error) {
    detail = error.message;
  }

  return (
    <main
      id="nimble-main"
      className="nimble-main"
    >
      <section
        className="nimble-boundary-failure"
        role="alert"
      >
        <p className="nimble-panel__eyebrow">
          Principle X · Route failure
        </p>

        <h1>{title}</h1>
        <p>{detail}</p>

        <div className="nimble-command-actions">
          <button
            className="nimble-button nimble-button--secondary"
            type="button"
            onClick={() => {
              window.history.back();
            }}
          >
            Go back
          </button>

          <button
            className="nimble-button nimble-button--primary"
            type="button"
            onClick={() => {
              window.location.assign("/");
            }}
          >
            Return to overview
          </button>
        </div>
      </section>
    </main>
  );
}
