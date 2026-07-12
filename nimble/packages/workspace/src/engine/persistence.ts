import type {
  WorkspaceDefinition,
  WorkspaceSnapshot,
} from "./contracts";

export interface WorkspaceStorage {
  read(
    key: string,
  ): string | undefined;

  write(
    key: string,
    value: string,
  ): void;

  remove(
    key: string,
  ): void;
}

export function createWorkspaceSnapshot(
  workspace: WorkspaceDefinition,
  capturedAt = new Date().toISOString(),
): WorkspaceSnapshot {
  return {
    schemaVersion: "1.0",
    capturedAt,
    workspace,
  };
}

export function serializeWorkspaceSnapshot(
  snapshot: WorkspaceSnapshot,
): string {
  return JSON.stringify(snapshot);
}

export function parseWorkspaceSnapshot(
  serialized: string,
): WorkspaceSnapshot {
  const parsed: unknown =
    JSON.parse(serialized);

  if (
    typeof parsed !== "object" ||
    parsed === null ||
    !("schemaVersion" in parsed) ||
    parsed.schemaVersion !== "1.0" ||
    !("workspace" in parsed)
  ) {
    throw new Error(
      "Invalid workspace snapshot.",
    );
  }

  return parsed as WorkspaceSnapshot;
}

export class MemoryWorkspaceStorage
  implements WorkspaceStorage {
  readonly #values = new Map<
    string,
    string
  >();

  read(key: string): string | undefined {
    return this.#values.get(key);
  }

  write(
    key: string,
    value: string,
  ): void {
    this.#values.set(key, value);
  }

  remove(key: string): void {
    this.#values.delete(key);
  }
}
