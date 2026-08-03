/* ============================================================================
   ALETHEUSOS
   Genesis 39.4
   WebGPU Morphogenesis Runtime
   TypeScript Compatibility Edition
============================================================================ */

export interface MorphogenesisSnapshot {
  enabled: boolean;
  backend: "webgpu" | "fallback";
  adapterName?: string;
  vendor?: string;
  architecture?: string;
}

/* -------------------------------------------------------------------------- */
/* WebGPU compatibility types                                                 */
/* -------------------------------------------------------------------------- */

interface GPUAdapterInfo {
  vendor?: string;
  architecture?: string;
  device?: string;
  description?: string;
}

interface GPUUncapturedErrorEvent extends Event {
  error?: unknown;
}

interface GPUDeviceLike {
  addEventListener(
    type: string,
    listener: (event: GPUUncapturedErrorEvent) => void,
  ): void;
}

interface GPUAdapterLike {
  requestDevice(): Promise<GPUDeviceLike>;
  requestAdapterInfo?(): Promise<GPUAdapterInfo>;
}

interface NavigatorGPU {
  requestAdapter(options?: {
    powerPreference?: "low-power" | "high-performance";
  }): Promise<GPUAdapterLike | null>;
}

interface NavigatorWithGPU extends Navigator {
  gpu?: NavigatorGPU;
}

const gpuNavigator = navigator as NavigatorWithGPU;

/* -------------------------------------------------------------------------- */

export class WebGPUMorphogenesisRuntime {
  private snapshot: MorphogenesisSnapshot = {
    enabled: false,
    backend: "fallback",
  };

  async initialize(): Promise<MorphogenesisSnapshot> {
    if (!gpuNavigator.gpu) {
      console.info("[REM] WebGPU unavailable. Falling back.");

      return this.snapshot;
    }

    try {
      const adapter = await gpuNavigator.gpu.requestAdapter({
        powerPreference: "high-performance",
      });

      if (!adapter) {
        return this.snapshot;
      }

      const device = await adapter.requestDevice();

      device.addEventListener(
        "uncapturederror",
        (event: GPUUncapturedErrorEvent) => {
          console.warn(
            "[REM] WebGPU uncaptured error",
            event.error ?? event,
          );
        },
      );

      let info: GPUAdapterInfo | undefined;

      if (adapter.requestAdapterInfo) {
        info = await adapter.requestAdapterInfo();
      }

      this.snapshot = {
        enabled: true,
        backend: "webgpu",
        adapterName:
          info?.description ??
          info?.device ??
          "Unknown GPU",
        vendor: info?.vendor,
        architecture: info?.architecture,
      };

      return this.snapshot;
    } catch (err) {
      console.warn("[REM] WebGPU initialization failed.", err);

      return this.snapshot;
    }
  }

  getSnapshot(): MorphogenesisSnapshot {
    return this.snapshot;
  }
}

export const webgpuMorphogenesisRuntime =
  new WebGPUMorphogenesisRuntime();
