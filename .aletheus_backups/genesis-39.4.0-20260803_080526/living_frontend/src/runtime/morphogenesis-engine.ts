import type { REMPhase } from "./rem-types";

export interface MorphogenesisState {
  phase: REMPhase;
  coherence: number;
  target: number;
  velocity: number;
}

export interface MorphogenesisCommand {
  type:
    | "CRYSTALLIZE"
    | "DISSOLVE"
    | "TRANSFORM"
    | "STABILIZE";
  intensity?: number;
}

const clamp01 = (value: number): number =>
  Math.max(0, Math.min(1, value));

export class MorphogenesisEngine {
  private state: MorphogenesisState = {
    phase: "ambient",
    coherence: 0.06,
    target: 0.06,
    velocity: 0,
  };

  get snapshot(): MorphogenesisState {
    return { ...this.state };
  }

  dispatch(command: MorphogenesisCommand): MorphogenesisState {
    const intensity = clamp01(command.intensity ?? 1);

    switch (command.type) {
      case "CRYSTALLIZE":
        this.state.target = 0.9 * intensity;
        this.state.phase = "nucleating";
        break;
      case "DISSOLVE":
        this.state.target = 0.04;
        this.state.phase = "dissolving";
        break;
      case "TRANSFORM":
        this.state.target = clamp01(0.45 + 0.45 * intensity);
        this.state.phase = "transforming";
        break;
      case "STABILIZE":
        this.state.target = clamp01(this.state.coherence);
        this.state.phase = "stabilized";
        break;
    }

    return this.snapshot;
  }

  step(deltaSeconds: number): MorphogenesisState {
    const dt = Math.max(0, Math.min(deltaSeconds, 1 / 20));
    const stiffness = 8.4;
    const damping = 4.6;
    const displacement = this.state.target - this.state.coherence;
    const acceleration =
      stiffness * displacement - damping * this.state.velocity;

    this.state.velocity += acceleration * dt;
    this.state.coherence = clamp01(
      this.state.coherence + this.state.velocity * dt,
    );

    const error = Math.abs(this.state.target - this.state.coherence);
    if (this.state.phase === "nucleating" && this.state.coherence > 0.28) {
      this.state.phase = "condensing";
    }
    if (
      (this.state.phase === "condensing" ||
        this.state.phase === "transforming") &&
      error < 0.025
    ) {
      this.state.phase = "stabilized";
    }
    if (this.state.phase === "dissolving" && this.state.coherence < 0.09) {
      this.state.phase = "ambient";
    }

    return this.snapshot;
  }
}
