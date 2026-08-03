export type QualityTier = "conservative" | "balanced" | "high" | "ultra";

export interface QualityProfile {
  tier: QualityTier;
  particleCount: number;
  targetHz: number;
  connectionRadius: number;
  bloomPasses: number;
  useWorker: boolean;
  useWebGPU: boolean;
}

export function selectQualityProfile(input: {
  webgpu: boolean;
  sharedArrayBuffer: boolean;
  crossOriginIsolated: boolean;
  hardwareConcurrency: number;
  deviceMemoryGiB: number | null;
}): QualityProfile {
  const memory = input.deviceMemoryGiB ?? 4;
  const workers = input.sharedArrayBuffer && input.crossOriginIsolated;

  if (input.webgpu && input.hardwareConcurrency >= 12 && memory >= 8) {
    return {
      tier: "ultra",
      particleCount: 4096,
      targetHz: 120,
      connectionRadius: 72,
      bloomPasses: 3,
      useWorker: workers,
      useWebGPU: true,
    };
  }

  if (input.webgpu && input.hardwareConcurrency >= 8) {
    return {
      tier: "high",
      particleCount: 2048,
      targetHz: 120,
      connectionRadius: 76,
      bloomPasses: 2,
      useWorker: workers,
      useWebGPU: true,
    };
  }

  if (input.hardwareConcurrency >= 4) {
    return {
      tier: "balanced",
      particleCount: 768,
      targetHz: 60,
      connectionRadius: 82,
      bloomPasses: 1,
      useWorker: false,
      useWebGPU: false,
    };
  }

  return {
    tier: "conservative",
    particleCount: 320,
    targetHz: 60,
    connectionRadius: 84,
    bloomPasses: 0,
    useWorker: false,
    useWebGPU: false,
  };
}
