import type { LivingEngineMeshSnapshot } from
  "../runtime/living-engine-mesh-types";

export function LivingEngineMeshHUD({
  snapshot,
}: {
  snapshot: LivingEngineMeshSnapshot;
}) {
  return (
    <aside className="living-engine-mesh-hud">
      <span>LIVING ENGINE MESH</span>
      <strong>{snapshot.engines.filter((engine) => engine.active).length} ACTIVE</strong>
      <dl>
        <div><dt>Load</dt><dd>{(snapshot.totalLoad * 100).toFixed(1)}%</dd></div>
        <div><dt>Resonance</dt><dd>{(snapshot.practicalResonance * 100).toFixed(1)}</dd></div>
        <div><dt>Intent</dt><dd>{(snapshot.preHydrationConfidence * 100).toFixed(1)}</dd></div>
        <div><dt>Bio</dt><dd>{(snapshot.biologicalCoherence * 100).toFixed(1)}</dd></div>
      </dl>
    </aside>
  );
}
