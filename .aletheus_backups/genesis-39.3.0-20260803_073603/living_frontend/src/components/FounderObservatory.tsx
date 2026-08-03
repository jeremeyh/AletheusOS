export function FounderObservatory({
  authorized,
}: {
  authorized: boolean;
}) {
  return (
    <section
      className={`founder-observatory ${
        authorized ? "authorized" : "sealed"
      }`}
    >
      <div className="founder-observatory__mark">
        <img
          src="/aletheusos-canonical-mark.jpeg"
          alt="AletheusOS canonical gold mark"
        />
        <span className="founder-observatory__ring founder-observatory__ring--a" />
        <span className="founder-observatory__ring founder-observatory__ring--b" />
      </div>

      <div>
        <span className="eyebrow">
          Founder Observatory
        </span>
        <h2>
          {authorized
            ? "Underlying Tensor Mechanics Revealed"
            : "Constitutionally Isolated"}
        </h2>
        <p>
          {authorized
            ? "The twelve-dimensional intelligence tensor, gravitational curvature, harmonic contraction, contradiction shear, phase order, runtime topology, mission mass, and constitutional compliance are observable from this root-attested plane."
            : "No application role, developer entitlement, workspace permission, client-side route, or internal service tunnel can grant access to this trust plane."}
        </p>
      </div>

      <div className="founder-observatory__seal">
        <span>
          {authorized ? "ROOT ATTESTED" : "SEALED"}
        </span>
        <strong>
          {authorized
            ? "FOUNDER ONLY"
            : "NO ACCESS PATH"}
        </strong>
      </div>
    </section>
  );
}
