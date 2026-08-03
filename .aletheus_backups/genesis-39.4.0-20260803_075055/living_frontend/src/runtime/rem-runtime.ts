import { DeterministicNoise } from "./deterministic-noise";
import { MorphogenesisEngine } from "./morphogenesis-engine";
import { TemporalDeterminismMonitor } from "./temporal-determinism-monitor";
import type {
  REMParticle,
  REMPointer,
  REMRuntimeConfiguration,
  REMRuntimeState,
} from "./rem-types";

export const defaultREMConfiguration: REMRuntimeConfiguration = {
  particleCount: 320,
  latticeStiffness: 340,
  damping: 28,
  brownianStrength: 0.085,
  magneticStrength: 780,
  magneticRadius: 180,
  connectionRadius: 84,
  targetFrameMs: 1000 / 120,
  seed: 3923,
};

export class REMRuntime {
  readonly particles: REMParticle[] = [];
  readonly morphogenesis = new MorphogenesisEngine();
  readonly timing: TemporalDeterminismMonitor;

  private readonly noise: DeterministicNoise;
  private width = 1;
  private height = 1;
  private lastTimestamp = 0;
  private pointer: REMPointer = { x: -1000, y: -1000, active: false };
  private state: REMRuntimeState;

  constructor(
    private readonly configuration: REMRuntimeConfiguration =
      defaultREMConfiguration,
  ) {
    this.noise = new DeterministicNoise(configuration.seed);
    this.timing = new TemporalDeterminismMonitor(
      configuration.targetFrameMs,
    );
    this.state = {
      phase: "ambient",
      coherence: 0.06,
      targetCoherence: 0.06,
      crystallized: false,
      particleCount: configuration.particleCount,
      frameTimeMs: configuration.targetFrameMs,
      frameVarianceMs: 0,
      meantimeQuotient: 0.913,
      droppedFrameRatio: 0,
    };
  }

  initialize(width: number, height: number): void {
    this.width = Math.max(1, width);
    this.height = Math.max(1, height);
    this.particles.length = 0;

    for (let index = 0; index < this.configuration.particleCount; index += 1) {
      const x = this.noise.next() * this.width;
      const y = this.noise.next() * this.height;
      this.particles.push({
        x,
        y,
        velocityX: this.noise.bipolar() * 0.32,
        velocityY: this.noise.bipolar() * 0.32,
        anchorX: x,
        anchorY: y,
        coherence: 0.06,
        size: 0.55 + this.noise.next() * 1.55,
        charge: 0.55 + this.noise.next() * 0.9,
        seed: this.noise.next(),
      });
    }
  }

  resize(width: number, height: number): void {
    const previousWidth = this.width;
    const previousHeight = this.height;
    this.width = Math.max(1, width);
    this.height = Math.max(1, height);

    for (const particle of this.particles) {
      particle.x = particle.x / previousWidth * this.width;
      particle.y = particle.y / previousHeight * this.height;
      particle.anchorX = particle.anchorX / previousWidth * this.width;
      particle.anchorY = particle.anchorY / previousHeight * this.height;
    }
  }

  setPointer(pointer: REMPointer): void {
    this.pointer = pointer;
  }

  crystallize(intensity = 1): void {
    this.morphogenesis.dispatch({ type: "CRYSTALLIZE", intensity });
  }

  dissolve(): void {
    this.morphogenesis.dispatch({ type: "DISSOLVE" });
  }

  update(timestamp: number): REMRuntimeState {
    const frameTime =
      this.lastTimestamp === 0
        ? this.configuration.targetFrameMs
        : Math.min(50, Math.max(0.1, timestamp - this.lastTimestamp));
    this.lastTimestamp = timestamp;
    const deltaSeconds = frameTime / 1000;

    const morph = this.morphogenesis.step(deltaSeconds);
    const temporal = this.timing.add(frameTime, timestamp);

    for (let index = 0; index < this.particles.length; index += 1) {
      const particle = this.particles[index];
      particle.coherence +=
        (morph.coherence - particle.coherence) *
        Math.min(1, deltaSeconds * 4.6);

      const ambient =
        this.noise.sample2D(
          particle.x * 0.004,
          particle.y * 0.004,
          timestamp * 0.001 + particle.seed,
        ) * this.configuration.brownianStrength;

      let forceX = ambient;
      let forceY = this.noise.sample2D(
        particle.y * 0.004,
        particle.x * 0.004,
        timestamp * 0.0013 - particle.seed,
      ) * this.configuration.brownianStrength;

      const anchorWeight = particle.coherence;
      forceX +=
        (particle.anchorX - particle.x) *
        this.configuration.latticeStiffness *
        anchorWeight *
        0.00008;
      forceY +=
        (particle.anchorY - particle.y) *
        this.configuration.latticeStiffness *
        anchorWeight *
        0.00008;

      if (this.pointer.active) {
        const dx = particle.x - this.pointer.x;
        const dy = particle.y - this.pointer.y;
        const distanceSquared = dx * dx + dy * dy;
        const radiusSquared =
          this.configuration.magneticRadius *
          this.configuration.magneticRadius;

        if (distanceSquared > 0.01 && distanceSquared < radiusSquared) {
          const distance = Math.sqrt(distanceSquared);
          const attenuation =
            1 - distance / this.configuration.magneticRadius;
          const force =
            this.configuration.magneticStrength *
            particle.charge *
            attenuation *
            attenuation /
            Math.max(distanceSquared, 36);
          forceX += dx / distance * force;
          forceY += dy / distance * force;
        }
      }

      particle.velocityX += forceX;
      particle.velocityY += forceY;

      const damping =
        Math.exp(-this.configuration.damping * deltaSeconds * 0.045);
      particle.velocityX *= damping;
      particle.velocityY *= damping;

      particle.x += particle.velocityX;
      particle.y += particle.velocityY;

      if (particle.x < 0) particle.x += this.width;
      if (particle.x > this.width) particle.x -= this.width;
      if (particle.y < 0) particle.y += this.height;
      if (particle.y > this.height) particle.y -= this.height;
    }

    this.state = {
      phase: morph.phase,
      coherence: morph.coherence,
      targetCoherence: morph.target,
      crystallized: morph.coherence > 0.5,
      particleCount: this.particles.length,
      frameTimeMs: temporal.meanFrameTimeMs,
      frameVarianceMs: temporal.varianceMs,
      meantimeQuotient: temporal.meantimeQuotient,
      droppedFrameRatio: temporal.droppedFrameRatio,
    };
    return { ...this.state };
  }

  get snapshot(): REMRuntimeState {
    return { ...this.state };
  }

  get connectionRadius(): number {
    return this.configuration.connectionRadius;
  }
}
