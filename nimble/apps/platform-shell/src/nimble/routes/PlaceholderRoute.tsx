import { useLocation } from "react-router";

export function PlaceholderRoute() {
  const location = useLocation();

  const name = location.pathname
    .replace(/^\/+/, "")
    .replaceAll("-", " ")
    || "overview";

  return (
    <main id="nimble-main" className="nimble-main">
      <section className="nimble-placeholder-route">
        <p className="nimble-panel__eyebrow">
          Registered Nimble route
        </p>

        <h1>{name}</h1>

        <p>
          This bounded route exists in the production router but its
          domain surface has not yet been implemented.
        </p>

        <section>
          <h2>Current truth</h2>
          <p>
            Navigation is active. Domain behavior and live data remain
            intentionally unavailable rather than being simulated.
          </p>
        </section>
      </section>
    </main>
  );
}
