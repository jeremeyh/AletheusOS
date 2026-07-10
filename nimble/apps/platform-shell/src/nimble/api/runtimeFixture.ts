import type {
  RuntimeHealthSnapshot,
  RuntimeMission,
  RuntimeOverview,
} from "./runtimeTypes";

const now = new Date().toISOString();

export const runtimeHealthFixture: RuntimeHealthSnapshot = {
  state: "healthy",
  summary:
    "Development fixture based on the most recent verified regression baseline.",
  passingChecks: 246,
  totalChecks: 246,
  warningCount: 0,
  checks: [
    {
      id: "runtime-regression",
      name: "Runtime regression",
      state: "healthy",
      detail: "246 tests passing with zero warnings.",
      latencyMs: 2500,
      checkedAt: now,
    },
    {
      id: "nimble-foundation",
      name: "Nimble foundation",
      state: "healthy",
      detail: "Architecture and inheritance contracts validated.",
      checkedAt: now,
    },
    {
      id: "nimble-typescript",
      name: "Nimble TypeScript boundary",
      state: "healthy",
      detail: "All bounded packages typecheck successfully.",
      checkedAt: now,
    },
  ],
  truth: {
    state: "development_fixture",
    explanation:
      "The browser is displaying a verified local fixture because no live AletheusOS API response has been received.",
    confidence: {
      value: 0.99,
      label: "verified",
      basis:
        "Most recent local regression and Nimble validation results.",
    },
    provenance: [
      {
        sourceId: "local-regression-baseline",
        sourceType: "development_fixture",
        label: "AletheusOS 246-test clean baseline",
        observedAt: now,
      },
    ],
    uncertainty: [
      {
        known: true,
        material: true,
        description:
          "This fixture does not prove the current live runtime state.",
      },
    ],
    reversibility: {
      reversible: true,
      undoLabel: "Reconnect to live runtime",
      consequence:
        "Fixture data will be replaced when the live API becomes available.",
    },
  },
};

export const runtimeMissionFixture: readonly RuntimeMission[] = [
  {
    id: "nimble-production-shell",
    name: "Nimble Production Shell",
    description:
      "Convert the visual reference into a typed operational platform shell.",
    state: "active",
    progress: 82,
    confidence: {
      value: 0.97,
      label: "high",
      basis:
        "TypeScript, Vite, package, and validator boundaries are passing.",
    },
  },
  {
    id: "runtime-api-integration",
    name: "Runtime API Integration",
    description:
      "Connect Nimble surfaces to live AletheusOS runtime adapters.",
    state: "active",
    progress: 46,
    confidence: {
      value: 0.88,
      label: "high",
      basis:
        "Client boundary is defined; live endpoint verification remains.",
    },
  },
  {
    id: "card-hawk-inheritance",
    name: "Card Hawk Inheritance",
    description:
      "Adopt Nimble without duplicating the experience framework.",
    state: "planned",
    progress: 20,
    confidence: {
      value: 0.94,
      label: "high",
      basis:
        "Application inheritance contracts are established.",
    },
  },
];

export const runtimeOverviewFixture: RuntimeOverview = {
  health: runtimeHealthFixture,
  missions: runtimeMissionFixture,
  generatedAt: now,
};
