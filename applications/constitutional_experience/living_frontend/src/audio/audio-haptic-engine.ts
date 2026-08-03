export type AudioHapticEvent =
  | "NUCLEATION"
  | "CONDENSATION"
  | "STABILIZATION"
  | "DISSOLUTION"
  | "FOCUS";

export class AudioHapticEngine {
  private context: AudioContext | null = null;

  async activate(): Promise<void> {
    if (this.context === null) {
      this.context = new AudioContext({ latencyHint: "interactive" });
    }
    if (this.context.state === "suspended") {
      await this.context.resume();
    }
  }

  trigger(event: AudioHapticEvent, intensity = 0.5): void {
    if (this.context === null) return;

    const now = this.context.currentTime;
    const oscillator = this.context.createOscillator();
    const gain = this.context.createGain();
    const filter = this.context.createBiquadFilter();

    const profile = {
      NUCLEATION: [220, 0.08],
      CONDENSATION: [420, 0.12],
      STABILIZATION: [660, 0.1],
      DISSOLUTION: [180, 0.16],
      FOCUS: [880, 0.045],
    } as const;

    const [frequency, duration] = profile[event];
    oscillator.type = event === "DISSOLUTION" ? "sine" : "triangle";
    oscillator.frequency.setValueAtTime(frequency, now);
    oscillator.frequency.exponentialRampToValueAtTime(
      Math.max(40, frequency * (event === "DISSOLUTION" ? 0.55 : 1.22)),
      now + duration,
    );

    filter.type = "lowpass";
    filter.frequency.setValueAtTime(1800, now);

    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(
      Math.max(0.0002, Math.min(0.06, intensity * 0.035)),
      now + 0.008,
    );
    gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);

    oscillator.connect(filter);
    filter.connect(gain);
    gain.connect(this.context.destination);
    oscillator.start(now);
    oscillator.stop(now + duration + 0.02);
  }
}
