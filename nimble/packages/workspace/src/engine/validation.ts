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

/* ALETHEUSOS_WORKSPACE_STUDIO_BINDING_BEGIN */

/**
 * Workspace Studio compatibility binding.
 *
 * This is deliberately additive. It does not replace Workspace engine
 * validation authority and does not introduce mutation, persistence,
 * transport, command execution, or runtime ownership.
 */
type WorkspaceContractRecord = Record<string, unknown>;

function isWorkspaceContractRecord(
  value: unknown,
): value is WorkspaceContractRecord {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function workspaceContractVersion(
  contract: WorkspaceContractRecord,
): string | undefined {
  const meta = contract["meta"];

  if (!isWorkspaceContractRecord(meta)) {
    return undefined;
  }

  const version = meta["version"];

  return typeof version === "string" && version.length > 0
    ? version
    : undefined;
}

export function validateWorkspaceContractCompatibility(
  contract: unknown,
  expectedVersion?: string,
): WorkspaceValidationResult {
  const failures: string[] = [];

  if (!isWorkspaceContractRecord(contract)) {
    failures.push("Workspace contract must be an object.");

    return {
      valid: false,
      failures,
    };
  }

  const contractVersion = workspaceContractVersion(contract);

  if (contractVersion === undefined) {
    failures.push("Workspace contract meta.version is required.");
  }

  if (
    expectedVersion !== undefined &&
    contractVersion !== undefined &&
    contractVersion !== expectedVersion
  ) {
    failures.push(
      `Workspace contract version "${contractVersion}" is incompatible with expected version "${expectedVersion}".`,
    );
  }

  if (!Object.prototype.hasOwnProperty.call(contract, "workspace")) {
    failures.push("Workspace contract workspace definition is required.");
  }

  if (!Array.isArray(contract["layout_modes"])) {
    failures.push("Workspace contract layout_modes must be an array.");
  }

  return {
    valid: failures.length === 0,
    failures,
  };
}

export function validateWorkspaceAgainstContract(
  workspace: Parameters<typeof validateWorkspace>[0],
  contract: unknown,
  expectedVersion?: string,
): WorkspaceValidationResult {
  const compatibility = validateWorkspaceContractCompatibility(
    contract,
    expectedVersion,
  );

  if (!compatibility.valid) {
    return compatibility;
  }

  return validateWorkspace(workspace);
}

/* ALETHEUSOS_WORKSPACE_STUDIO_BINDING_END */
