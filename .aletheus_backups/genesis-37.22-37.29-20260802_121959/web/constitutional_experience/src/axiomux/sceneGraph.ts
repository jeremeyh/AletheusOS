import type { SceneNode } from "../types/runtime.js";

export class SceneGraph {
  private readonly nodes = new Map<string, SceneNode>();
  private readonly edges = new Map<string, Set<string>>();

  upsert(node: SceneNode): void {
    this.nodes.set(node.id, structuredClone(node));
    if (!this.edges.has(node.id)) this.edges.set(node.id, new Set());
  }

  connect(a: string, b: string): void {
    if (!this.nodes.has(a) || !this.nodes.has(b)) throw new Error("unknown scene node");
    this.edges.get(a)?.add(b);
    this.edges.get(b)?.add(a);
  }

  snapshot(): { nodes: SceneNode[]; edges: Array<[string, string]> } {
    const edges: Array<[string, string]> = [];
    for (const [a, targets] of this.edges) {
      for (const b of targets) if (a < b) edges.push([a, b]);
    }
    return { nodes: [...this.nodes.values()].map(structuredClone), edges };
  }
}
