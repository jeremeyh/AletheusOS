/* ============================================================================
 * ALETHEUSOS
 * Genesis 39.3.1
 * WebGPU Morphogenesis Runtime
 *
 * Strict-TS compatible
 * Graceful fallback when WebGPU is unavailable
 * ========================================================================= */

export interface WebGPUStatus {
  supported: boolean;
  initialized: boolean;
  backend: "webgpu" | "fallback";
  adapterName?: string;
  error?: string;
}

export interface MorphogenesisSnapshot {
  status: WebGPUStatus;
}

export interface RuntimeOptions {
  powerPreference?: "low-power" | "high-performance";
}

type NavigatorWithGPU = Navigator & {
  gpu?: {
    requestAdapter(options?: {
      powerPreference?: "low-power" | "high-performance";
    }): Promise<GPUAdapter | null>;
  };
};

export class WebGPUMorphogenesisRuntime {
  private snapshot: MorphogenesisSnapshot = {
    status: {
      supported: false,
      initialized: false,
      backend: "fallback",
    },
  };

  constructor(
    private readonly options: RuntimeOptions = {
      powerPreference: "high-performance",
    },
  ) {}

  public getSnapshot(): MorphogenesisSnapshot {
    return this.snapshot;
  }

  public async initialize(): Promise<MorphogenesisSnapshot> {
    try {
      const gpuNavigator = navigator as NavigatorWithGPU;

      if (!gpuNavigator.gpu) {
        this.snapshot.status = {
          supported: false,
          initialized: false,
          backend: "fallback",
          error: "WebGPU unavailable",
        };

        return this.snapshot;
      }

      const adapter = await gpuNavigator.gpu.requestAdapter({
        powerPreference:
          this.options.powerPreference ?? "high-performance",
      });

      if (!adapter) {
        this.snapshot.status = {
          supported: false,
          initialized: false,
          backend: "fallback",
          error: "No GPU adapter",
        };

        return this.snapshot;
      }

      const device = await adapter.requestDevice();

      device.addEventListener(
        "uncapturederror",
        (event: Event) => {
          console.warn(
            "WebGPU uncaptured error",
            event,
          );
        },
      );

      let adapterName = "Unknown GPU";

      try {
        const infoProvider = adapter as GPUAdapter & {
          info?: {
            vendor?: string;
            architecture?: string;
            device?: string;
            description?: string;
          };
        };

        if (infoProvider.info) {
          adapterName =
            infoProvider.info.description ??
            infoProvider.info.device ??
            adapterName;
        }
      } catch {
        // optional metadata only
      }

      this.snapshot.status = {
        supported: true,
        initialized: true,
        backend: "webgpu",
        adapterName,
      };

      return this.snapshot;
    } catch (err) {
      this.snapshot.status = {
        supported: false,
        initialized: false,
        backend: "fallback",
        error:
          err instanceof Error
            ? err.message
            : String(err),
      };

      return this.snapshot;
    }
  }
}
