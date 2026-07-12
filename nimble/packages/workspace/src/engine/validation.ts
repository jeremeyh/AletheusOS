import type {
  WorkspaceDefinition,
  WorkspaceValidationResult,
} from "./contracts";
import {
  validateWorkspaceLayout,
} from "./layout";

const ID_PATTERN =
  /^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$/;

export function validateWorkspace(
  workspace: WorkspaceDefinition,
): WorkspaceValidationResult {
  const failures: string[] = [];

  if (!ID_PATTERN.test(workspace.id)) {
    failures.push(
      `Invalid workspace id: ${workspace.id}`,
    );
  }

  if (!workspace.name.trim()) {
    failures.push(
      `Workspace has no name: ${workspace.id}`,
    );
  }

  if (!workspace.version.trim()) {
    failures.push(
      `Workspace has no version: ${workspace.id}`,
    );
  }

  const panelIds = new Set<string>();

  for (const panel of workspace.panels) {
    if (!ID_PATTERN.test(panel.id)) {
      failures.push(
        `Invalid workspace panel id: ${panel.id}`,
      );
    }

    if (panelIds.has(panel.id)) {
      failures.push(
        `Duplicate workspace panel: ${panel.id}`,
      );
    }

    panelIds.add(panel.id);

    if (panel.priority < 0) {
      failures.push(
        `Workspace panel priority cannot be negative: ${panel.id}`,
      );
    }
  }

  const layoutValidation =
    validateWorkspaceLayout(
      workspace.layout,
      workspace.panels,
    );

  failures.push(
    ...layoutValidation.failures,
  );

  return {
    valid: failures.length === 0,
    failures,
  };
}
