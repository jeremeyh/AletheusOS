export interface ThermalNode {
  id: string;
  processingLoad: number;
  memoryLoad: number;
  interactionRate: number;
  heat: number;
}

export class ThermalFieldEngine {
  private readonly nodes = new Map<string, ThermalNode>();

  update(input: Omit<ThermalNode, "heat">): ThermalNode {
    const previous = this.nodes.get(input.id);
    const targetHeat = Math.max(
      0,
      Math.min(
        1,
        input.processingLoad * 0.48 +
          input.memoryLoad * 0.32 +
          input.interactionRate * 0.2,
      ),
    );

    const heat = previous
      ? previous.heat + (targetHeat - previous.heat) * 0.18
      : targetHeat;

    const node = { ...input, heat };
    this.nodes.set(input.id, node);
    return node;
  }

  cool(deltaSeconds: number): void {
    const cooling = Math.exp(-Math.max(0, deltaSeconds) * 0.42);
    for (const [id, node] of this.nodes) {
      this.nodes.set(id, { ...node, heat: node.heat * cooling });
    }
  }

  snapshot(): ThermalNode[] {
    return Array.from(this.nodes.values()).map((node) => ({ ...node }));
  }
}
