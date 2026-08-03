export interface FrameSample {
  frameTimeMs: number;
  timestamp: number;
}

export interface TemporalDeterminismSnapshot {
  meanFrameTimeMs: number;
  varianceMs: number;
  droppedFrameRatio: number;
  meantimeQuotient: number;
  samples: number;
}

const clamp01 = (value: number): number =>
  Math.max(0, Math.min(1, value));

export class TemporalDeterminismMonitor {
  private readonly samples: FrameSample[] = [];

  constructor(
    private readonly targetFrameMs = 1000 / 120,
    private readonly windowSize = 180,
  ) {}

  add(frameTimeMs: number, timestamp = performance.now()):
    TemporalDeterminismSnapshot {
    this.samples.push({ frameTimeMs, timestamp });
    if (this.samples.length > this.windowSize) {
      this.samples.shift();
    }
    return this.snapshot();
  }

  snapshot(): TemporalDeterminismSnapshot {
    if (this.samples.length === 0) {
      return {
        meanFrameTimeMs: this.targetFrameMs,
        varianceMs: 0,
        droppedFrameRatio: 0,
        meantimeQuotient: 0.913,
        samples: 0,
      };
    }

    const values = this.samples.map((sample) => sample.frameTimeMs);
    const mean =
      values.reduce((sum, value) => sum + value, 0) / values.length;
    const variance =
      values.reduce(
        (sum, value) => sum + Math.pow(value - mean, 2),
        0,
      ) / values.length;
    const dropped =
      values.filter((value) => value > this.targetFrameMs * 1.5).length /
      values.length;

    const budgetScore = clamp01(this.targetFrameMs / Math.max(mean, 0.001));
    const jitterScore = clamp01(1 - Math.sqrt(variance) / this.targetFrameMs);
    const deliveryScore = clamp01(1 - dropped);
    const quotient =
      budgetScore * 0.48 +
      jitterScore * 0.34 +
      deliveryScore * 0.18;

    return {
      meanFrameTimeMs: mean,
      varianceMs: variance,
      droppedFrameRatio: dropped,
      meantimeQuotient: quotient,
      samples: values.length,
    };
  }
}
