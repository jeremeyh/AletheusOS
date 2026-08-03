export interface PointerSample {
  x: number;
  y: number;
  timestamp: number;
}

export interface IntentPrediction {
  x: number;
  y: number;
  horizonMs: number;
  speed: number;
  confidence: number;
}

export class PredictiveIntentEngine {
  private readonly samples: PointerSample[] = [];

  constructor(
    private readonly maximumSamples = 8,
    private readonly horizonMs = 42,
  ) {}

  add(sample: PointerSample): IntentPrediction {
    this.samples.push(sample);
    if (this.samples.length > this.maximumSamples) {
      this.samples.shift();
    }
    return this.predict();
  }

  predict(): IntentPrediction {
    if (this.samples.length < 2) {
      const latest = this.samples.at(-1) ?? { x: 0, y: 0, timestamp: 0 };
      return {
        x: latest.x,
        y: latest.y,
        horizonMs: this.horizonMs,
        speed: 0,
        confidence: 0,
      };
    }

    const current = this.samples.at(-1)!;
    const previous = this.samples.at(-2)!;
    const deltaMs = Math.max(1, current.timestamp - previous.timestamp);
    const velocityX = (current.x - previous.x) / deltaMs;
    const velocityY = (current.y - previous.y) / deltaMs;
    const speed = Math.hypot(velocityX, velocityY) * 1000;

    const consistency = this.samples.length < 3
      ? 0.55
      : this.directionConsistency();

    return {
      x: current.x + velocityX * this.horizonMs,
      y: current.y + velocityY * this.horizonMs,
      horizonMs: this.horizonMs,
      speed,
      confidence: Math.max(0, Math.min(1, consistency)),
    };
  }

  private directionConsistency(): number {
    let similarity = 0;
    let comparisons = 0;

    for (let index = 2; index < this.samples.length; index += 1) {
      const a = this.samples[index - 2];
      const b = this.samples[index - 1];
      const c = this.samples[index];

      const v1x = b.x - a.x;
      const v1y = b.y - a.y;
      const v2x = c.x - b.x;
      const v2y = c.y - b.y;

      const denominator =
        Math.max(0.001, Math.hypot(v1x, v1y) * Math.hypot(v2x, v2y));
      similarity += (v1x * v2x + v1y * v2y) / denominator;
      comparisons += 1;
    }

    return comparisons === 0
      ? 0.55
      : Math.max(0, Math.min(1, (similarity / comparisons + 1) / 2));
  }
}
