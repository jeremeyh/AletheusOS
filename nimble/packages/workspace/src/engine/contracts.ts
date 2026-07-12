export type WorkspaceDensity =
  | "consumer"
  | "professional"
  | "enterprise"
  | "founder"
  | "developer";

export type WorkspaceRegion =
  | "header"
  | "navigation"
  | "dock"
  | "canvas"
  | "sidebar"
  | "activity-rail"
  | "status-bar"
  | "inspector"
  | "overlay"
  | "modal";

export type PanelDockState =
  | "left"
  | "right"
  | "bottom"
  | "canvas"
  | "floating"
  | "detached"
  | "hidden";

export type PanelLifecycleState =
  | "created"
  | "registered"
  | "mounted"
  | "visible"
  | "collapsed"
  | "suspended"
  | "destroyed";

export interface WorkspacePanel {
  readonly id: string;
  readonly canonicalName: string;
  readonly displayName?: string;
  readonly region: WorkspaceRegion;
  readonly dockState: PanelDockState;
  readonly lifecycle: PanelLifecycleState;
  readonly priority: number;
  readonly visible: boolean;
  readonly minimumWidth?: number;
  readonly minimumHeight?: number;
  readonly metadata?: Readonly<Record<string, unknown>>;
}

export interface WorkspaceSplit {
  readonly id: string;
  readonly direction: "horizontal" | "vertical";
  readonly first: WorkspaceLayoutNode;
  readonly second: WorkspaceLayoutNode;
  readonly ratio: number;
}

export interface WorkspacePanelNode {
  readonly type: "panel";
  readonly panelId: string;
}

export interface WorkspaceSplitNode {
  readonly type: "split";
  readonly split: WorkspaceSplit;
}

export type WorkspaceLayoutNode =
  | WorkspacePanelNode
  | WorkspaceSplitNode;

export interface WorkspaceLayout {
  readonly id: string;
  readonly version: string;
  readonly root: WorkspaceLayoutNode;
}

export interface WorkspaceDefinition {
  readonly id: string;
  readonly name: string;
  readonly description?: string;
  readonly version: string;
  readonly density: WorkspaceDensity;
  readonly themeId: string;
  readonly panels: readonly WorkspacePanel[];
  readonly layout: WorkspaceLayout;
  readonly metadata?: Readonly<Record<string, unknown>>;
}

export interface WorkspaceSnapshot {
  readonly workspace: WorkspaceDefinition;
  readonly capturedAt: string;
  readonly schemaVersion: "1.0";
}

export interface WorkspaceValidationResult {
  readonly valid: boolean;
  readonly failures: readonly string[];
}
