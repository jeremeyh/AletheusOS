import type {
  PanelLifecycleState,
} from "./contracts";

const TRANSITIONS: Readonly<
  Record<
    PanelLifecycleState,
    readonly PanelLifecycleState[]
  >
> = {
  created: ["registered", "destroyed"],
  registered: ["mounted", "destroyed"],
  mounted: [
    "visible",
    "collapsed",
    "suspended",
    "destroyed",
  ],
  visible: [
    "collapsed",
    "suspended",
    "destroyed",
  ],
  collapsed: [
    "visible",
    "suspended",
    "destroyed",
  ],
  suspended: [
    "mounted",
    "visible",
    "destroyed",
  ],
  destroyed: [],
};

export function canTransitionPanel(
  from: PanelLifecycleState,
  to: PanelLifecycleState,
): boolean {
  return TRANSITIONS[from].includes(to);
}

export function assertPanelTransition(
  from: PanelLifecycleState,
  to: PanelLifecycleState,
): void {
  if (!canTransitionPanel(from, to)) {
    throw new Error(
      `Invalid panel lifecycle transition: ${from} -> ${to}`,
    );
  }
}
