import type { RuntimeTelemetry } from "../types/runtime.js";

export class TelemetryLoop {
  private samples: number[] = [];
  private last = performance.now();

  frame(gpuQueueDepth: number, wasmStepMs: number): RuntimeTelemetry {
    const now = performance.now();
    const frameTimeMs = Math.max(0.001, now - this.last);
    this.last = now;
    this.samples.push(frameTimeMs);
    if (this.samples.length > 240) this.samples.shift();
    const average = this.samples.reduce((a, b) => a + b, 0) / this.samples.length;
    const target = 1000 / 120;
    return {
      timestamp: Date.now(),
      fps: 1000 / frameTimeMs,
      frameTimeMs,
      gpuQueueDepth,
      wasmStepMs,
      meantimeQuotient: Math.max(0, Math.min(1, target / Math.max(target, average))),
    };
  }
}
