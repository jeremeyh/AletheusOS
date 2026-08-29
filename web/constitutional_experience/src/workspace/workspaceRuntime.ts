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

/* ALETHEUSOS_WORKSPACE_STUDIO_READ_ONLY_BINDING_BEGIN */

/**
 * Snapshot-only Workspace Studio projection over the existing WorkspaceRuntime.
 *
 * WorkspaceRuntime retains its existing mutable runtime authority. This
 * binding exposes none of register/move/snap/save/load and introduces no
 * command execution, persistence ownership, transport, or autonomy.
 */
export interface WorkspaceStudioReadOnlyRuntime {
  readonly snapshot: () => Readonly<ReturnType<WorkspaceRuntime["snapshot"]>>;
}

export interface WorkspaceStudioValidatedReadModel<TWorkspace> {
  readonly workspace: TWorkspace;
  readonly validation: {
    readonly valid: boolean;
    readonly failures: readonly string[];
  };
  readonly contractVersion?: string;
}

export interface WorkspaceStudioReadOnlyBinding<TWorkspace> {
  readonly runtime: WorkspaceStudioReadOnlyRuntime;
  readonly workspace: TWorkspace;
  readonly validation: {
    readonly valid: true;
    readonly failures: readonly string[];
  };
  readonly contractVersion?: string;
}

export function bindWorkspaceStudioReadOnly<TWorkspace>(
  runtime: WorkspaceRuntime,
  readModel: WorkspaceStudioValidatedReadModel<TWorkspace>,
): WorkspaceStudioReadOnlyBinding<TWorkspace> {
  if (!readModel.validation.valid) {
    throw new Error(
      "Workspace Studio read-only boundary: validated read model required.",
    );
  }

  const runtimeProjection: WorkspaceStudioReadOnlyRuntime = Object.freeze({
    snapshot: () => Object.freeze([...runtime.snapshot()]),
  });

  const validation = Object.freeze({
    valid: true as const,
    failures: Object.freeze([...readModel.validation.failures]),
  });

  const binding = {
    runtime: runtimeProjection,
    workspace: readModel.workspace,
    validation,
    ...(readModel.contractVersion === undefined
      ? {}
      : {
          contractVersion: readModel.contractVersion,
        }),
  };

  return Object.freeze(binding);
}

/* ALETHEUSOS_WORKSPACE_STUDIO_READ_ONLY_BINDING_END */
