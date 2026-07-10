import {
  isRouteErrorResponse,
  useRouteError,
} from "react-router";

export function RouteError() {
  const error = useRouteError();

  let title = "The workspace could not be opened.";
  let cause = "An unknown route failure occurred.";
  let status: number | undefined;

  if (isRouteErrorResponse(error)) {
    status = error.status;
    title = error.statusText || title;
    cause = typeof error.data === "string"
      ? error.data
      : JSON.stringify(error.data);
  } else if (error instanceof Error) {
    cause = error.message;
  }

  return (
    <main className="nimble-route-error">
      <p className="nimble-panel__eyebrow">
        Principle X · Failure disclosed
      </p>

      <h1>{title}</h1>

      {status && (
        <strong className="nimble-route-error__status">
          HTTP {status}
        </strong>
      )}

      <section>
        <h2>What failed</h2>
        <p>{cause}</p>
      </section>

      <section>
        <h2>Impact</h2>
        <p>
          The selected route is unavailable. Existing runtime and
          workspace state have not been modified.
        </p>
      </section>

      <section>
        <h2>Recovery</h2>
        <p>
          Return to the overview or retry after the underlying route
          dependency is restored.
        </p>
      </section>

      <a
        className="nimble-button nimble-button--primary"
        href="/"
      >
        Return to overview
      </a>
    </main>
  );
}
