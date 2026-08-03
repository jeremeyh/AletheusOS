export class DeterministicNoise {
  private state: number;

  constructor(seed: number) {
    this.state = seed >>> 0;
  }

  next(): number {
    this.state = (1664525 * this.state + 1013904223) >>> 0;
    return this.state / 0xffffffff;
  }

  bipolar(): number {
    return this.next() * 2 - 1;
  }

  sample2D(x: number, y: number, time: number): number {
    const a = Math.sin(x * 12.9898 + y * 78.233 + time * 0.37 + this.state);
    const b = Math.sin(x * 4.173 + y * 19.91 - time * 0.21 + this.state * 0.5);
    return Math.max(-1, Math.min(1, a * 0.68 + b * 0.32));
  }
}
