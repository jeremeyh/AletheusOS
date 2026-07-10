import { AdaptiveWorkspace } from "./AdaptiveWorkspace";
import { CommandSurface } from "./CommandSurface";
import { GlobalNavigation } from "./GlobalNavigation";
import { MotionEnvironment } from "./MotionEnvironment";
import { ToastRegion } from "./ToastRegion";
import { TopBar } from "./TopBar";
import { TruthInspector } from "./TruthInspector";

export function PlatformShell() {
  return (
    <>
      <a className="skip-link" href="#nimble-main">
        Skip to main workspace
      </a>

      <MotionEnvironment />

      <div className="nimble-shell">
        <GlobalNavigation />

        <section className="nimble-stage">
          <TopBar />
          <AdaptiveWorkspace />
        </section>

        <TruthInspector />
      </div>

      <CommandSurface />
      <ToastRegion />
    </>
  );
}
