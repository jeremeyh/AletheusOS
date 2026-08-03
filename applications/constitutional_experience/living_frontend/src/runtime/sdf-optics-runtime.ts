export interface SDFSurfaceState {
  coherence: number;
  thermalPressure: number;
  blendSoftness: number;
  active: boolean;
}

export class SDFOpticsRuntime {
  private state: SDFSurfaceState = {
    coherence: 0.86,
    thermalPressure: 0.12,
    blendSoftness: 0.12,
    active: false,
  };

  activate(): void {
    this.state.active = true;
  }

  deactivate(): void {
    this.state.active = false;
  }

  update(patch: Partial<Omit<SDFSurfaceState, "active">>): void {
    this.state = {
      ...this.state,
      ...patch,
      coherence: Math.max(0, Math.min(1, patch.coherence ?? this.state.coherence)),
      thermalPressure: Math.max(
        0,
        Math.min(1, patch.thermalPressure ?? this.state.thermalPressure),
      ),
      blendSoftness: Math.max(
        0.01,
        Math.min(0.5, patch.blendSoftness ?? this.state.blendSoftness),
      ),
    };
  }

  get snapshot(): SDFSurfaceState {
    return { ...this.state };
  }
}
