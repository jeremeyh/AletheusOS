import type {
  LoudnessTelemetry,
  MetrologySnapshot,
  TelemetryState,
} from "../types";
import {
  clamp01,
  constitutionalResonance,
  practicalResonance,
} from "./information-physics";

export interface MetrologyEngineOptions {
  fftBins?: number;
  channelCount?: number;
  smoothing?: number;
  seed?: number;
}

class DeterministicNoise {
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
}

export class QuantumMetrologyEngine {
  private readonly fftBins: number;
  private readonly channelCount: number;
  private readonly smoothing: number;
  private readonly noise: DeterministicNoise;
  private previous: MetrologySnapshot | null = null;

  constructor(options: MetrologyEngineOptions = {}) {
    this.fftBins = options.fftBins ?? 52;
    this.channelCount = options.channelCount ?? 6;
    this.smoothing = clamp01(options.smoothing ?? 0.82);
    this.noise = new DeterministicNoise(options.seed ?? 3921);
  }

  sample(telemetry: TelemetryState, elapsedSeconds: number): MetrologySnapshot {
    const resonance = constitutionalResonance(
      telemetry.veracity,
      telemetry.consensus,
      telemetry.contradiction,
    );

    const signalIntegrity = clamp01(
      telemetry.veracity * 0.56 +
        telemetry.consensus * 0.34 +
        (1 - telemetry.entropy) * 0.10,
    );
    const harmonicStability = clamp01(
      resonance * 0.62 +
        telemetry.elasticity * 0.18 +
        (1 - telemetry.contradiction) * 0.20,
    );
    const practical = practicalResonance(
      signalIntegrity,
      harmonicStability,
      resonance,
      telemetry.contradiction,
    );

    const loudness: LoudnessTelemetry = {
      shortTerm: -15 + Math.sin(elapsedSeconds * 0.71) * 0.34 +
        this.noise.bipolar() * 0.08,
      integrated: -19 + Math.sin(elapsedSeconds * 0.13) * 0.10,
      momentary: -8.5 + Math.sin(elapsedSeconds * 1.31) * 0.92 +
        this.noise.bipolar() * 0.12,
      truePeak: -1.5 + this.noise.bipolar() * 0.04,
      range: 7.4 + Math.sin(elapsedSeconds * 0.19) * 0.3,
    };

    const fft = Array.from({ length: this.fftBins }, (_, index) => {
      const normalized = index / Math.max(1, this.fftBins - 1);
      const envelope = 0.18 + Math.pow(Math.sin(normalized * Math.PI), 1.4) * 0.68;
      const harmonic =
        Math.sin(index * 0.29 + elapsedSeconds * 2.1) * 0.12 +
        Math.sin(index * 0.071 - elapsedSeconds * 0.83) * 0.08;
      return clamp01(envelope + harmonic + this.noise.bipolar() * 0.025);
    });

    const channels = Array.from({ length: this.channelCount }, (_, index) =>
      clamp01(
        0.54 +
          Math.sin(elapsedSeconds * (0.88 + index * 0.07) + index * 0.91) * 0.22 +
          this.noise.bipolar() * 0.035,
      ),
    );

    const raw: MetrologySnapshot = {
      timestamp: Date.now(),
      loudness,
      phaseCorrelation: clamp01(
        0.88 +
          Math.sin(elapsedSeconds * 0.27) * 0.018 -
          telemetry.contradiction * 0.05,
      ),
      stereoWidth: 1.42 + Math.sin(elapsedSeconds * 0.17) * 0.035,
      practicalResonance: practical,
      meantimeQuotient: clamp01(
        telemetry.meantimeQuotient * 0.72 + practical * 0.28,
      ),
      harmonicStability,
      signalIntegrity,
      noiseFloor: clamp01(
        telemetry.entropy * 0.52 +
          telemetry.contradiction * 0.48,
      ),
      fft,
      channels,
    };

    if (!this.previous) {
      this.previous = raw;
      return raw;
    }

    const alpha = 1 - this.smoothing;
    const blend = (previous: number, next: number): number =>
      previous + (next - previous) * alpha;

    const result: MetrologySnapshot = {
      ...raw,
      loudness: {
        shortTerm: blend(this.previous.loudness.shortTerm, raw.loudness.shortTerm),
        integrated: blend(this.previous.loudness.integrated, raw.loudness.integrated),
        momentary: blend(this.previous.loudness.momentary, raw.loudness.momentary),
        truePeak: blend(this.previous.loudness.truePeak, raw.loudness.truePeak),
        range: blend(this.previous.loudness.range, raw.loudness.range),
      },
      phaseCorrelation: blend(
        this.previous.phaseCorrelation,
        raw.phaseCorrelation,
      ),
      stereoWidth: blend(this.previous.stereoWidth, raw.stereoWidth),
      practicalResonance: blend(
        this.previous.practicalResonance,
        raw.practicalResonance,
      ),
      meantimeQuotient: blend(
        this.previous.meantimeQuotient,
        raw.meantimeQuotient,
      ),
      harmonicStability: blend(
        this.previous.harmonicStability,
        raw.harmonicStability,
      ),
      signalIntegrity: blend(
        this.previous.signalIntegrity,
        raw.signalIntegrity,
      ),
      noiseFloor: blend(this.previous.noiseFloor, raw.noiseFloor),
      fft: raw.fft.map((value, index) =>
        blend(this.previous?.fft[index] ?? value, value),
      ),
      channels: raw.channels.map((value, index) =>
        blend(this.previous?.channels[index] ?? value, value),
      ),
    };

    this.previous = result;
    return result;
  }
}
