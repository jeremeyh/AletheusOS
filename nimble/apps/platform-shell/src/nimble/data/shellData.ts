export interface NavigationItem {
  readonly id: string;
  readonly label: string;
  readonly icon: string;
  readonly count?: number;
  readonly status?: "healthy" | "active";
}

export interface NavigationGroup {
  readonly id: string;
  readonly label: string;
  readonly items: readonly NavigationItem[];
}

export interface Mission {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly progress: number;
}

export const navigationGroups: readonly NavigationGroup[] = [
  {
    id: "platform",
    label: "Platform",
    items: [
      {
        id: "overview",
        label: "Overview",
        icon: "◈",
      },
      {
        id: "intelligence",
        label: "Intelligence",
        icon: "✦",
      },
      {
        id: "missions",
        label: "Missions",
        icon: "◎",
        count: 4,
      },
      {
        id: "workflows",
        label: "Workflows",
        icon: "⌁",
      },
      {
        id: "agents",
        label: "Agents",
        icon: "◇",
        status: "active",
      },
    ],
  },
  {
    id: "knowledge",
    label: "Knowledge",
    items: [
      {
        id: "memory",
        label: "Memory",
        icon: "◌",
      },
      {
        id: "knowledge-graph",
        label: "Knowledge Graph",
        icon: "⌬",
      },
    ],
  },
  {
    id: "governance",
    label: "Governance",
    items: [
      {
        id: "council",
        label: "Council",
        icon: "△",
      },
      {
        id: "runtime",
        label: "Runtime Health",
        icon: "◉",
        status: "healthy",
      },
    ],
  },
];

export const missions: readonly Mission[] = [
  {
    id: "nimble-foundation",
    name: "Nimble Experience Foundation",
    description: "React shell realization",
    progress: 72,
  },
  {
    id: "card-hawk",
    name: "Card Hawk Integration",
    description: "Foundation inheritance ready",
    progress: 42,
  },
  {
    id: "genesis-eight",
    name: "Genesis 8 Stabilization",
    description: "Validated and complete",
    progress: 100,
  },
];
