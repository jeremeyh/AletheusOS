export interface ReactionDiffusionState {
  activator: number;
  inhibitor: number;
  coherence: number;
  wave: number;
}

export class BiologicalRhythmEngine {
  private state: ReactionDiffusionState = {
    activator: 0.54,
    inhibitor: 0.46,
    coherence: 0.88,
    wave: 0,
  };

  step(
    deltaSeconds: number,
    systemLoad: number,
    networkLatency: number,
  ): ReactionDiffusionState {
    const dt = Math.min(Math.max(deltaSeconds, 0), 0.05);
    const load = Math.max(0, Math.min(1, systemLoad));
    const latency = Math.max(0, Math.min(1, networkLatency));

    const feed = 0.031 + load * 0.014;
    const kill = 0.058 + latency * 0.012;
    const reaction =
      this.state.activator *
      this.state.inhibitor *
      this.state.inhibitor;

    this.state.activator +=
      (0.18 * (1 - this.state.activator) -
        reaction +
        feed * (1 - this.state.activator)) *
      dt;

    this.state.inhibitor +=
      (0.09 * (0.5 - this.state.inhibitor) +
        reaction -
        (kill + feed) * this.state.inhibitor) *
      dt;

    this.state.activator = Math.max(0, Math.min(1, this.state.activator));
    this.state.inhibitor = Math.max(0, Math.min(1, this.state.inhibitor));
    this.state.wave =
      Math.sin((this.state.activator - this.state.inhibitor) * Math.PI * 4);
    this.state.coherence = Math.max(
      0,
      Math.min(
        1,
        1 - Math.abs(this.state.activator - this.state.inhibitor) * 0.72,
      ),
    );

    return { ...this.state };
  }

  get snapshot(): ReactionDiffusionState {
    return { ...this.state };
  }
}
