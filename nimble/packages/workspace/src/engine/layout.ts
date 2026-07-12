import type {
  WorkspaceLayout,
  WorkspaceLayoutNode,
  WorkspacePanel,
  WorkspaceValidationResult,
} from "./contracts";

function collectPanelIds(
  node: WorkspaceLayoutNode,
  collected: string[],
): void {
  if (node.type === "panel") {
    collected.push(node.panelId);
    return;
  }

  collectPanelIds(
    node.split.first,
    collected,
  );

  collectPanelIds(
    node.split.second,
    collected,
  );
}

function validateNode(
  node: WorkspaceLayoutNode,
  failures: string[],
): void {
  if (node.type === "panel") {
    if (!node.panelId.trim()) {
      failures.push(
        "Workspace panel node has an empty panel id.",
      );
    }

    return;
  }

  const ratio = node.split.ratio;

  if (
    !Number.isFinite(ratio) ||
    ratio <= 0 ||
    ratio >= 1
  ) {
    failures.push(
      `Workspace split ratio must be between 0 and 1: ${node.split.id}`,
    );
  }

  validateNode(
    node.split.first,
    failures,
  );

  validateNode(
    node.split.second,
    failures,
  );
}

export function workspacePanelIds(
  layout: WorkspaceLayout,
): readonly string[] {
  const panelIds: string[] = [];

  collectPanelIds(
    layout.root,
    panelIds,
  );

  return panelIds;
}

export function validateWorkspaceLayout(
  layout: WorkspaceLayout,
  panels: readonly WorkspacePanel[],
): WorkspaceValidationResult {
  const failures: string[] = [];

  validateNode(
    layout.root,
    failures,
  );

  const layoutPanelIds =
    workspacePanelIds(layout);

  const panelIds = new Set(
    panels.map((panel) => panel.id),
  );

  const encountered = new Set<string>();

  for (const panelId of layoutPanelIds) {
    if (encountered.has(panelId)) {
      failures.push(
        `Workspace layout contains duplicate panel: ${panelId}`,
      );
    }

    encountered.add(panelId);

    if (!panelIds.has(panelId)) {
      failures.push(
        `Workspace layout references unknown panel: ${panelId}`,
      );
    }
  }

  return {
    valid: failures.length === 0,
    failures,
  };
}
