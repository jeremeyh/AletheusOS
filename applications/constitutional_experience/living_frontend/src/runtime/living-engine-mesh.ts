import type {
  EngineTelemetry,
  LivingEngineId,
  LivingEngineMeshSnapshot,
} from "./living-engine-mesh-types";

const clamp01 = (value: number): number =>
  Math.max(0, Math.min(1, value));

export class LivingEngineMesh {
  private readonly engines = new Map<LivingEngineId, EngineTelemetry>();

  register(engine: EngineTelemetry): void {
    this.engines.set(engine.id, { ...engine });
  }

  update(
    id: LivingEngineId,
    patch: Partial<Omit<EngineTelemetry, "id">>,
  ): void {
    const current = this.engines.get(id);
    if (!current) {
      throw new Error(`Living engine not registered: ${id}`);
    }
    this.engines.set(id, { ...current, ...patch });
  }

  snapshot(): LivingEngineMeshSnapshot {
    const engines = Array.from(this.engines.values());
    const totalLoad = engines.length === 0
      ? 0
      : engines.reduce((sum, engine) => sum + engine.load, 0) / engines.length;

    const practicalResonance = engines.length === 0
      ? 0
      : engines.reduce(
          (sum, engine) =>
            sum +
            engine.confidence *
              (engine.health === "nominal" ? 1 : engine.health === "degraded" ? 0.72 : 0.2),
          0,
        ) / engines.length;

    return {
      timestamp: Date.now(),
      engines,
      totalLoad: clamp01(totalLoad),
      practicalResonance: clamp01(practicalResonance),
      preHydrationConfidence:
        this.engines.get("predictive-intent")?.confidence ?? 0,
      thermalPressure:
        this.engines.get("thermal-field")?.load ?? 0,
      biologicalCoherence:
        this.engines.get("biological-rhythm")?.confidence ?? 0,
    };
  }
}

export function createDefaultLivingEngineMesh(): LivingEngineMesh {
  const mesh = new LivingEngineMesh();
  const defaults: EngineTelemetry[] = [
    {
      id: "sdf-optics",
      health: "inactive",
      active: false,
      latencyMs: 0,
      load: 0,
      confidence: 0.9,
      detail: "SDF optics awaiting hardware activation",
    },
    {
      id: "predictive-intent",
      health: "nominal",
      active: true,
      latencyMs: 0.18,
      load: 0.08,
      confidence: 0.82,
      detail: "Pointer-vector pre-hydration active",
    },
    {
      id: "thermal-field",
      health: "nominal",
      active: true,
      latencyMs: 0.12,
      load: 0.16,
      confidence: 0.91,
      detail: "Virtual heat field calibrated",
    },
    {
      id: "biological-rhythm",
      health: "nominal",
      active: true,
      latencyMs: 0.28,
      load: 0.11,
      confidence: 0.88,
      detail: "Reaction-diffusion metrology active",
    },
    {
      id: "spatial-layout",
      health: "inactive",
      active: false,
      latencyMs: 0,
      load: 0,
      confidence: 0.78,
      detail: "Off-DOM layout solver boundary established",
    },
    {
      id: "constraint-physics",
      health: "inactive",
      active: false,
      latencyMs: 0,
      load: 0,
      confidence: 0.74,
      detail: "Constraint physics boundary established",
    },
    {
      id: "audio-haptics",
      health: "nominal",
      active: true,
      latencyMs: 0.7,
      load: 0.05,
      confidence: 0.86,
      detail: "Audio haptic synthesis available",
    },
    {
      id: "reactive-graph",
      health: "nominal",
      active: true,
      latencyMs: 0.09,
      load: 0.06,
      confidence: 0.93,
      detail: "Fine-grained signal graph active",
    },
  ];

  defaults.forEach((engine) => mesh.register(engine));
  return mesh;
}
