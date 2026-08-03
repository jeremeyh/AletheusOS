export interface HardwareCapabilities {
  webgpu: boolean;
  webgl2: boolean;
  sharedArrayBuffer: boolean;
  crossOriginIsolated: boolean;
  hardwareConcurrency: number;
  deviceMemoryGiB: number | null;
  preferredBackend: "webgpu" | "webgl2" | "canvas2d";
}

export async function detectHardwareCapabilities():
  Promise<HardwareCapabilities> {
  const webgpu = "gpu" in navigator;
  const canvas = document.createElement("canvas");
  const webgl2 = canvas.getContext("webgl2") !== null;
  const sharedArrayBuffer =
    typeof SharedArrayBuffer !== "undefined";
  const isolated = globalThis.crossOriginIsolated === true;
  const deviceMemory =
    "deviceMemory" in navigator
      ? Number((navigator as Navigator & { deviceMemory?: number }).deviceMemory)
      : null;

  return {
    webgpu,
    webgl2,
    sharedArrayBuffer,
    crossOriginIsolated: isolated,
    hardwareConcurrency: navigator.hardwareConcurrency || 1,
    deviceMemoryGiB: Number.isFinite(deviceMemory) ? deviceMemory : null,
    preferredBackend: webgpu
      ? "webgpu"
      : webgl2
        ? "webgl2"
        : "canvas2d",
  };
}
