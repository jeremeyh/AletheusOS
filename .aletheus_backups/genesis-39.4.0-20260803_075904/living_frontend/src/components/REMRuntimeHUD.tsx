import type { REMRuntimeState } from "../runtime/rem-types";

export function REMRuntimeHUD({
  state,
}: {
  state: REMRuntimeState;
}) {
  return (
    <aside className="rem-runtime-hud" aria-label="REM runtime status">
      <span><i />REM SUBSTRATE</span>
      <strong>{state.phase.replace("-", " ").toUpperCase()}</strong>
      <dl>
        <div><dt>Coherence</dt><dd>{state.coherence.toFixed(3)}</dd></div>
        <div><dt>Particles</dt><dd>{state.particleCount}</dd></div>
        <div><dt>Frame</dt><dd>{state.frameTimeMs.toFixed(2)} ms</dd></div>
        <div><dt>Qm</dt><dd>{(state.meantimeQuotient * 100).toFixed(1)}</dd></div>
      </dl>
    </aside>
  );
}
