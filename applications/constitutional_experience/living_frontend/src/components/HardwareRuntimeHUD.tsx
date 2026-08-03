import type { LivingExperienceHardwareState } from
  "../runtime/living-experience-hardware-runtime";

export function HardwareRuntimeHUD({
  state,
}: {
  state: LivingExperienceHardwareState;
}) {
  return (
    <aside className="hardware-runtime-hud">
      <span>HARDWARE RUNTIME</span>
      <strong>{state.backend.toUpperCase()}</strong>
      <dl>
        <div><dt>Tier</dt><dd>{state.quality?.tier ?? "detecting"}</dd></div>
        <div><dt>Particles</dt><dd>{state.quality?.particleCount ?? "—"}</dd></div>
        <div><dt>Target</dt><dd>{state.quality?.targetHz ?? "—"} Hz</dd></div>
        <div><dt>Worker</dt><dd>{state.workerEnabled ? "SAB" : "fallback"}</dd></div>
      </dl>
    </aside>
  );
}
