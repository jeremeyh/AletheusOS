export type NimblePanelState =
  | "open"
  | "collapsed"
  | "focused"
  | "hidden";

export interface NimblePanelDefinition {
  readonly id: string;
  readonly title: string;
  readonly role: string;
  readonly state: NimblePanelState;
  readonly minimumWidth: number;
  readonly minimumHeight: number;
}

export interface NimbleWorkspaceLayout {
  readonly id: string;
  readonly applicationId: string;
  readonly panels: readonly NimblePanelDefinition[];
  readonly updatedAt: string;
  readonly version: number;
}

export * from "./engine";
