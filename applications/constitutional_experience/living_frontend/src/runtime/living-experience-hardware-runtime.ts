import {
  detectHardwareCapabilities,
  type HardwareCapabilities,
} from "./hardware-capability-detector";
import {
  selectQualityProfile,
  type QualityProfile,
} from "./adaptive-quality-manager";

export interface LivingExperienceHardwareState {
  initialized: boolean;
  backend: "webgpu" | "webgl2" | "canvas2d";
  capabilities: HardwareCapabilities | null;
  quality: QualityProfile | null;
  workerEnabled: boolean;
  reason: string;
}

export class LivingExperienceHardwareRuntime {
  private state: LivingExperienceHardwareState = {
    initialized: false,
    backend: "canvas2d",
    capabilities: null,
    quality: null,
    workerEnabled: false,
    reason: "Not initialized",
  };

  async initialize(): Promise<LivingExperienceHardwareState> {
    const capabilities = await detectHardwareCapabilities();
    const quality = selectQualityProfile(capabilities);
    const workerEnabled =
      quality.useWorker &&
      capabilities.sharedArrayBuffer &&
      capabilities.crossOriginIsolated;

    this.state = {
      initialized: true,
      backend: quality.useWebGPU
        ? "webgpu"
        : capabilities.webgl2
          ? "webgl2"
          : "canvas2d",
      capabilities,
      quality,
      workerEnabled,
      reason: workerEnabled
        ? "Hardware acceleration and isolated worker transport available"
        : "Fallback path selected according to detected capability",
    };

    return this.snapshot;
  }

  get snapshot(): LivingExperienceHardwareState {
    return {
      ...this.state,
      capabilities: this.state.capabilities
        ? { ...this.state.capabilities }
        : null,
      quality: this.state.quality ? { ...this.state.quality } : null,
    };
  }
}
