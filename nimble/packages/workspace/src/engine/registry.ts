import type {
  WorkspaceDefinition,
} from "./contracts";
import {
  validateWorkspace,
} from "./validation";

export class WorkspaceRegistry {
  readonly #workspaces = new Map<
    string,
    WorkspaceDefinition
  >();

  #activeWorkspaceId: string | undefined;

  register(
    workspace: WorkspaceDefinition,
  ): void {
    const validation =
      validateWorkspace(workspace);

    if (!validation.valid) {
      throw new Error(
        [
          "Workspace validation failed:",
          ...validation.failures,
        ].join("\n"),
      );
    }

    if (
      this.#workspaces.has(workspace.id)
    ) {
      throw new Error(
        `Duplicate workspace: ${workspace.id}`,
      );
    }

    this.#workspaces.set(
      workspace.id,
      workspace,
    );
  }

  unregister(id: string): void {
    if (!this.#workspaces.delete(id)) {
      throw new Error(
        `Unknown workspace: ${id}`,
      );
    }

    if (this.#activeWorkspaceId === id) {
      this.#activeWorkspaceId = undefined;
    }
  }

  resolve(id: string): WorkspaceDefinition {
    const workspace =
      this.#workspaces.get(id);

    if (!workspace) {
      throw new Error(
        `Unknown workspace: ${id}`,
      );
    }

    return workspace;
  }

  activate(id: string): WorkspaceDefinition {
    const workspace = this.resolve(id);

    this.#activeWorkspaceId = id;

    return workspace;
  }

  active(): WorkspaceDefinition | undefined {
    return this.#activeWorkspaceId
      ? this.resolve(this.#activeWorkspaceId)
      : undefined;
  }

  list(): readonly WorkspaceDefinition[] {
    return [...this.#workspaces.values()];
  }

  has(id: string): boolean {
    return this.#workspaces.has(id);
  }
}
