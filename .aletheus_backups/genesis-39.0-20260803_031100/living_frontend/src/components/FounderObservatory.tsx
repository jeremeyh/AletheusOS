export function FounderObservatory({ authorized }: { authorized: boolean }) {
  return (
    <section
      className={`founder-observatory ${
        authorized ? "founder-observatory--authorized" : "founder-observatory--sealed"
      }`}
    >
      <div className="founder-observatory__logo-shell">
        <img
          className="founder-observatory__logo"
          src="/aletheusos-canonical-logo.jpeg"
          alt="AletheusOS canonical gold logo"
        />
        <span className="founder-observatory__orbit founder-observatory__orbit--one" />
        <span className="founder-observatory__orbit founder-observatory__orbit--two" />
      </div>

      <div className="founder-observatory__copy">
        <span className="eyebrow">Founder Observatory</span>
        <h2>
          {authorized
            ? "Eye-in-the-Sky Authority Plane"
            : "Constitutionally Isolated"}
        </h2>
        <p>
          {authorized
            ? "Global telemetry, developer contribution, runtime posture, security state, marketplace behavior, mission health, constitutional compliance, and platform evolution are visible from this highest-order observability plane."
            : "No application role, developer entitlement, workspace permission, client-side route, or internal service tunnel can grant access to this trust plane."}
        </p>
      </div>

      <div className="founder-observatory__seal">
        <span>{authorized ? "ROOT ATTESTED" : "SEALED"}</span>
        <strong>{authorized ? "FOUNDER ONLY" : "NO ACCESS PATH"}</strong>
      </div>
    </section>
  );
}
