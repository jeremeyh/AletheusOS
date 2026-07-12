import type {
  WorkspaceDefinition,
} from "./contracts";

export const founderWorkspace: WorkspaceDefinition = {
  id: "aletheus.workspace.founder",
  name: "Founder Console™",
  description:
    "Canonical reference workspace for AletheusOS.",
  version: "0.1.0",
  density: "founder",
  themeId: "aletheus.instrumentation",
  panels: [
    {
      id: "aletheus.panel.navigation",
      canonicalName: "Navigation",
      region: "navigation",
      dockState: "left",
      lifecycle: "created",
      priority: 10,
      visible: true,
      minimumWidth: 220,
    },
    {
      id: "aletheus.panel.instrumentation",
      canonicalName:
        "Intelligence Instrumentation™",
      region: "canvas",
      dockState: "canvas",
      lifecycle: "created",
      priority: 100,
      visible: true,
      minimumWidth: 560,
    },
    {
      id: "aletheus.panel.activity",
      canonicalName: "Activity Rail",
      region: "activity-rail",
      dockState: "right",
      lifecycle: "created",
      priority: 30,
      visible: true,
      minimumWidth: 260,
    },
    {
      id: "aletheus.panel.status",
      canonicalName: "Status Bar",
      region: "status-bar",
      dockState: "bottom",
      lifecycle: "created",
      priority: 20,
      visible: true,
      minimumHeight: 32,
    },
  ],
  layout: {
    id: "aletheus.layout.founder.default",
    version: "0.1.0",
    root: {
      type: "split",
      split: {
        id: "aletheus.split.founder.primary",
        direction: "horizontal",
        ratio: 0.2,
        first: {
          type: "panel",
          panelId:
            "aletheus.panel.navigation",
        },
        second: {
          type: "split",
          split: {
            id: "aletheus.split.founder.content",
            direction: "horizontal",
            ratio: 0.76,
            first: {
              type: "panel",
              panelId:
                "aletheus.panel.instrumentation",
            },
            second: {
              type: "panel",
              panelId:
                "aletheus.panel.activity",
            },
          },
        },
      },
    },
  },
};
