import type { InstrumentDefinition } from "../types/runtime.js";

export interface LayoutItem {
  instrumentId: string;
  x: number; y: number; width: number; height: number;
  displayId?: string;
}

export class WorkspaceRuntime {
  private readonly instruments = new Map<string, InstrumentDefinition>();
  private layout: LayoutItem[] = [];

  register(definition: InstrumentDefinition): void {
    if (definition.founderOnly) throw new Error("Founder instruments cannot enter Workspace Composer");
    this.instruments.set(definition.id, structuredClone(definition));
  }

  move(instrumentId: string, x: number, y: number, displayId?: string): void {
    if (!this.instruments.has(instrumentId)) throw new Error("instrument not registered");
    const current = this.layout.find(item => item.instrumentId === instrumentId);
    if (current) Object.assign(current, { x, y, displayId });
    else this.layout.push({ instrumentId, x, y, width: 4, height: 3, displayId });
  }

  snap(grid = 8): void {
    this.layout = this.layout.map(item => ({
      ...item,
      x: Math.round(item.x / grid) * grid,
      y: Math.round(item.y / grid) * grid,
    }));
  }

  save(storage: Storage, key: string): void {
    storage.setItem(key, JSON.stringify(this.layout));
  }

  load(storage: Storage, key: string): void {
    const raw = storage.getItem(key);
    this.layout = raw ? JSON.parse(raw) as LayoutItem[] : [];
  }

  snapshot(): LayoutItem[] { return structuredClone(this.layout); }
}
