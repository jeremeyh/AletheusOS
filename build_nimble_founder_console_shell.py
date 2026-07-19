#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SHELL = ROOT / "nimble/apps/platform-shell"
SRC = SHELL / "src"
CONSOLE = SRC / "nimble/founder-console"

VALIDATOR = ROOT / "validate_nimble_founder_console_shell.py"
TEST_FILE = ROOT / "tests/nimble/test_founder_console_shell.py"

REQUIRED = [
    ROOT / "nimble/packages/react/src/primitives/Surface.tsx",
    ROOT / "nimble/packages/react/src/primitives/Instrument.tsx",
    ROOT / "nimble/packages/workspace/src/engine/founder.ts",
]

FILES: dict[str, str] = {
    "src/nimble/founder-console/FounderConsoleShell.tsx": r'''import {
  AletheusIndexInstrument,
  Grid,
  Instrument,
  Stack,
  Surface,
  Text,
  ThorxInstrument,
} from "@aletheus/nimble-react";

import {
  founderWorkspace,
  type WorkspacePanel,
} from "@aletheus/nimble-workspace-engine";

import "./founder-console.css";


const ENGINE_GRADES = [
  {
    id: "engine:evidence",
    label: "Evidence Engine™",
    value: 95.4,
    accent:
      "instrumentation.engine.evidence",
  },
  {
    id: "engine:knowledge",
    label: "Knowledge Engine™",
    value: 97.8,
    accent:
      "instrumentation.engine.knowledge",
  },
  {
    id: "engine:reason",
    label: "Reason Engine™",
    value: 94.9,
    accent:
      "instrumentation.engine.reason",
  },
  {
    id: "engine:memory",
    label: "Memory Engine™",
    value: 98.2,
    accent:
      "instrumentation.engine.memory",
  },
  {
    id: "engine:bias",
    label: "Bias Engine™",
    value: 93.5,
    accent:
      "instrumentation.engine.bias",
  },
  {
    id: "engine:risk",
    label: "Risk Engine™",
    value: 91.2,
    accent:
      "instrumentation.engine.risk",
  },
  {
    id: "engine:predictive",
    label: "Predictive Engine™",
    value: 94.8,
    accent:
      "instrumentation.engine.predictive",
  },
] as const;


const ACTIVITY = [
  {
    time: "11:42",
    message: "Evidence model synchronized",
  },
  {
    time: "11:43",
    message: "Knowledge graph validated",
  },
  {
    time: "11:44",
    message: "Bias analysis refreshed",
  },
  {
    time: "11:45",
    message: "THORᵡ constitutional check passed",
  },
  {
    time: "11:46",
    message: "Workspace state preserved",
  },
] as const;


function NavigationPanel({
  panel,
}: {
  readonly panel: WorkspacePanel;
}) {
  const navigationItems = [
    "Overview",
    "Intelligence",
    "Runtime",
    "Governance",
    "Experience",
    "Telemetry",
    "Developer",
  ];

  return (
    <Surface
      variant="panel"
      className="founder-navigation"
      data-panel-id={panel.id}
    >
      <Stack spacing="lg">
        <div>
          <Text
            as="div"
            variant="caption"
            muted
            className="founder-eyebrow"
          >
            ALETHEUSOS™
          </Text>

          <Text
            as="div"
            variant="heading"
          >
            Founder Console™
          </Text>
        </div>

        <nav
          aria-label="Founder Console navigation"
          className="founder-navigation__items"
        >
          {navigationItems.map(
            (item, index) => (
              <button
                key={item}
                type="button"
                className={
                  index === 0
                    ? "founder-nav-button founder-nav-button--active"
                    : "founder-nav-button"
                }
              >
                <span
                  className="founder-nav-button__indicator"
                />
                {item}
              </button>
            ),
          )}
        </nav>

        <div className="founder-navigation__footer">
          <Text variant="telemetry" muted>
            GENESIS 8
          </Text>

          <Text variant="telemetry" muted>
            WORKSPACE v{founderWorkspace.version}
          </Text>
        </div>
      </Stack>
    </Surface>
  );
}


function Meter({
  value,
}: {
  readonly value: number;
}) {
  return (
    <div
      className="founder-meter"
      role="meter"
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={value}
    >
      <span
        className="founder-meter__fill"
        style={{
          width: `${value}%`,
        }}
      />
    </div>
  );
}


function InstrumentationCanvas({
  panel,
}: {
  readonly panel: WorkspacePanel;
}) {
  return (
    <section
      className="founder-canvas"
      data-panel-id={panel.id}
    >
      <Stack spacing="lg">
        <header className="founder-canvas__header">
          <div>
            <Text
              as="div"
              variant="caption"
              muted
              className="founder-eyebrow"
            >
              UNIVERSAL INTELLIGENCE RUNTIME
            </Text>

            <Text
              as="h1"
              variant="display"
              className="founder-title"
            >
              Intelligence Instrumentation™
            </Text>

            <Text
              as="p"
              muted
              className="founder-subtitle"
            >
              Live constitutional, epistemic, and
              engine-level instrumentation.
            </Text>
          </div>

          <div className="founder-runtime">
            <span className="founder-runtime__light" />

            <div>
              <Text
                as="div"
                variant="telemetry"
              >
                RUNTIME HEALTHY
              </Text>

              <Text
                as="div"
                variant="telemetry"
                muted
              >
                16 ms · 0 faults
              </Text>
            </div>
          </div>
        </header>

        <Grid
          columns="minmax(0, 1.35fr) minmax(280px, 0.65fr)"
          gap="lg"
          className="founder-primary-instruments"
        >
          <AletheusIndexInstrument
            value="94.6"
            status="healthy"
            density="founder"
            kind="gauge"
            detail={
              <div className="founder-detail-row">
                <span>Trajectory +2.7</span>
                <span>Stability 96.8</span>
                <span>Horizon 12 mo</span>
              </div>
            }
            footer={<Meter value={94.6} />}
          />

          <ThorxInstrument
            value="AUTHORIZED"
            status="healthy"
            density="founder"
            detail={
              <div className="founder-thorx-checks">
                <span>PRINCIPLE X · PASS</span>
                <span>CONSTITUTION · PASS</span>
                <span>GOVERNANCE · PASS</span>
              </div>
            }
            footer={
              <div className="founder-thorx-seal">
                CONSTITUTIONAL RELEASE VALID
              </div>
            }
          />
        </Grid>

        <Surface
          variant="panel"
          className="founder-engine-cluster"
        >
          <Stack spacing="lg">
            <div className="founder-section-heading">
              <div>
                <Text
                  as="h2"
                  variant="heading"
                >
                  Individual Engine Grades
                </Text>

                <Text as="p" muted>
                  Independent engine instruments.
                </Text>
              </div>

              <Text variant="telemetry" muted>
                7 ACTIVE · 0 FAULTS
              </Text>
            </div>

            <Grid
              minColumnWidth={240}
              gap="md"
            >
              {ENGINE_GRADES.map((engine) => (
                <Instrument
                  key={engine.id}
                  id={engine.id}
                  label={engine.label}
                  value={engine.value.toFixed(1)}
                  kind="meter"
                  density="enterprise"
                  status={
                    engine.value >= 95
                      ? "healthy"
                      : "attention"
                  }
                  accentToken={engine.accent}
                  detail={
                    `Independent grade · ${
                      engine.value >= 95
                        ? "stable"
                        : "under review"
                    }`
                  }
                  footer={
                    <Meter value={engine.value} />
                  }
                />
              ))}
            </Grid>
          </Stack>
        </Surface>
      </Stack>
    </section>
  );
}


function ActivityRail({
  panel,
}: {
  readonly panel: WorkspacePanel;
}) {
  return (
    <Surface
      variant="panel"
      className="founder-activity"
      data-panel-id={panel.id}
    >
      <Stack spacing="lg">
        <div>
          <Text
            as="div"
            variant="caption"
            muted
            className="founder-eyebrow"
          >
            ACTIVITY RAIL
          </Text>

          <Text
            as="h2"
            variant="heading"
          >
            Operational Intelligence
          </Text>
        </div>

        <ol className="founder-activity__list">
          {ACTIVITY.map((event) => (
            <li
              key={`${event.time}-${event.message}`}
              className="founder-activity__item"
            >
              <Text
                as="time"
                variant="telemetry"
                muted
              >
                {event.time}
              </Text>

              <Text
                as="div"
                variant="body"
              >
                {event.message}
              </Text>
            </li>
          ))}
        </ol>

        <div className="founder-activity__health">
          <Text variant="telemetry" muted>
            TELEMETRY CONNECTED
          </Text>

          <span className="founder-activity__health-light" />
        </div>
      </Stack>
    </Surface>
  );
}


function StatusBar({
  panel,
}: {
  readonly panel: WorkspacePanel;
}) {
  const statuses = [
    "Runtime Healthy",
    "16 ms",
    "7 Engines",
    "Telemetry Live",
    "THORᵡ Authorized",
    "Genesis 8",
  ];

  return (
    <footer
      className="founder-status-bar"
      data-panel-id={panel.id}
    >
      {statuses.map((status) => (
        <span
          key={status}
          className="founder-status-bar__item"
        >
          <span className="founder-status-bar__dot" />
          {status}
        </span>
      ))}
    </footer>
  );
}


function resolvePanel(
  id: string,
): WorkspacePanel {
  const panel = founderWorkspace.panels.find(
    (candidate) => candidate.id === id,
  );

  if (!panel) {
    throw new Error(
      `Founder Console panel is missing: ${id}`,
    );
  }

  return panel;
}


export function FounderConsoleShell() {
  const navigation = resolvePanel(
    "aletheus.panel.navigation",
  );

  const instrumentation = resolvePanel(
    "aletheus.panel.instrumentation",
  );

  const activity = resolvePanel(
    "aletheus.panel.activity",
  );

  const status = resolvePanel(
    "aletheus.panel.status",
  );

  return (
    <main
      className="founder-console"
      data-workspace-id={founderWorkspace.id}
      data-workspace-density={
        founderWorkspace.density
      }
      data-workspace-theme={
        founderWorkspace.themeId
      }
    >
      <NavigationPanel panel={navigation} />

      <InstrumentationCanvas
        panel={instrumentation}
      />

      <ActivityRail panel={activity} />

      <StatusBar panel={status} />
    </main>
  );
}
''',

    "src/nimble/founder-console/founder-console.css": r''':root {
  color-scheme: dark;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
}

* {
  box-sizing: border-box;
}

html,
body,
#founder-console-root {
  margin: 0;
  min-height: 100%;
}

body {
  background: #080d16;
  overflow: hidden;
}

button {
  font: inherit;
}

.founder-console {
  background:
    radial-gradient(
      circle at 32% -10%,
      rgba(217, 175, 72, 0.12),
      transparent 36rem
    ),
    radial-gradient(
      circle at 96% 4%,
      rgba(83, 166, 255, 0.08),
      transparent 30rem
    ),
    #080d16;
  display: grid;
  grid-template-areas:
    "navigation canvas activity"
    "status status status";
  grid-template-columns:
    minmax(210px, 0.19fr)
    minmax(0, 1fr)
    minmax(250px, 0.24fr);
  grid-template-rows:
    minmax(0, 1fr)
    34px;
  height: 100vh;
  overflow: hidden;
}

.founder-navigation {
  border-radius: 0 !important;
  border-width: 0 1px 0 0 !important;
  grid-area: navigation;
  min-width: 0;
  overflow: auto;
  padding: 26px 18px;
}

.founder-eyebrow {
  letter-spacing: 0.16em;
  margin-bottom: 8px !important;
}

.founder-navigation__items {
  display: grid;
  gap: 5px;
}

.founder-nav-button {
  align-items: center;
  background: transparent;
  border: 0;
  border-radius: 8px;
  color: #98a2b3;
  cursor: pointer;
  display: flex;
  gap: 10px;
  min-height: 42px;
  padding: 0 12px;
  text-align: left;
  transition:
    background 120ms cubic-bezier(0.2, 0, 0, 1),
    color 120ms cubic-bezier(0.2, 0, 0, 1);
  width: 100%;
}

.founder-nav-button:hover,
.founder-nav-button:focus-visible {
  background: rgba(217, 175, 72, 0.08);
  color: #eceff3;
  outline: none;
}

.founder-nav-button--active {
  background: rgba(217, 175, 72, 0.11);
  color: #ffffff;
}

.founder-nav-button__indicator {
  background: currentColor;
  border-radius: 50%;
  height: 5px;
  opacity: 0.42;
  width: 5px;
}

.founder-nav-button--active
.founder-nav-button__indicator {
  background: #d9af48;
  box-shadow: 0 0 10px rgba(217, 175, 72, 0.5);
  opacity: 1;
}

.founder-navigation__footer {
  border-top: 1px solid rgba(152, 162, 179, 0.12);
  display: grid;
  gap: 5px;
  margin-top: auto;
  padding-top: 18px;
}

.founder-canvas {
  grid-area: canvas;
  min-width: 0;
  overflow: auto;
  padding: clamp(24px, 3vw, 46px);
}

.founder-canvas__header {
  align-items: flex-start;
  display: flex;
  gap: 24px;
  justify-content: space-between;
}

.founder-title {
  font-size: clamp(34px, 4vw, 64px) !important;
  letter-spacing: -0.045em;
  line-height: 0.98 !important;
}

.founder-subtitle {
  margin-top: 14px !important;
  max-width: 680px;
}

.founder-runtime {
  align-items: center;
  border: 1px solid rgba(66, 207, 138, 0.25);
  border-radius: 10px;
  display: flex;
  flex: none;
  gap: 12px;
  padding: 11px 14px;
}

.founder-runtime__light,
.founder-activity__health-light {
  animation: founder-pulse 1.8s ease-in-out infinite;
  background: #42cf8a;
  border-radius: 50%;
  height: 7px;
  width: 7px;
}

.founder-primary-instruments > * {
  min-width: 0;
}

.founder-detail-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 18px;
}

.founder-thorx-checks {
  display: grid;
  gap: 6px;
}

.founder-thorx-checks span {
  color: #d8dde5;
  font-size: 11px;
  letter-spacing: 0.08em;
}

.founder-thorx-seal {
  border: 1px solid rgba(66, 207, 138, 0.34);
  border-radius: 6px;
  color: #42cf8a;
  font: 600 10px/1
    "IBM Plex Mono",
    "SFMono-Regular",
    monospace;
  letter-spacing: 0.12em;
  padding: 10px;
  text-align: center;
}

.founder-engine-cluster {
  padding: clamp(20px, 2.5vw, 34px);
}

.founder-section-heading {
  align-items: flex-end;
  display: flex;
  gap: 20px;
  justify-content: space-between;
}

.founder-meter {
  background: rgba(152, 162, 179, 0.12);
  border-radius: 999px;
  height: 5px;
  overflow: hidden;
  position: relative;
}

.founder-meter__fill {
  background: currentColor;
  border-radius: inherit;
  box-shadow: 0 0 14px
    color-mix(
      in srgb,
      currentColor 40%,
      transparent
    );
  display: block;
  height: 100%;
  transition:
    width 360ms cubic-bezier(0.2, 0, 0, 1);
}

.founder-activity {
  border-radius: 0 !important;
  border-width: 0 0 0 1px !important;
  grid-area: activity;
  min-width: 0;
  overflow: auto;
  padding: 26px 20px;
}

.founder-activity__list {
  display: grid;
  gap: 0;
  list-style: none;
  margin: 0;
  padding: 0;
}

.founder-activity__item {
  border-left: 1px solid
    rgba(152, 162, 179, 0.16);
  display: grid;
  gap: 7px;
  padding:
    0 0 22px 18px;
  position: relative;
}

.founder-activity__item::before {
  background: #d9af48;
  border-radius: 50%;
  box-shadow: 0 0 9px
    rgba(217, 175, 72, 0.38);
  content: "";
  height: 6px;
  left: -3px;
  position: absolute;
  top: 4px;
  width: 6px;
}

.founder-activity__health {
  align-items: center;
  border-top: 1px solid
    rgba(152, 162, 179, 0.12);
  display: flex;
  justify-content: space-between;
  padding-top: 16px;
}

.founder-status-bar {
  align-items: center;
  background: rgba(8, 13, 22, 0.96);
  border-top: 1px solid
    rgba(152, 162, 179, 0.14);
  display: flex;
  gap: 22px;
  grid-area: status;
  min-width: 0;
  overflow-x: auto;
  padding: 0 14px;
}

.founder-status-bar__item {
  align-items: center;
  color: #98a2b3;
  display: inline-flex;
  flex: none;
  font: 500 10px/1
    "IBM Plex Mono",
    "SFMono-Regular",
    monospace;
  gap: 7px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.founder-status-bar__dot {
  background: #42cf8a;
  border-radius: 50%;
  height: 5px;
  width: 5px;
}

@keyframes founder-pulse {
  0%,
  100% {
    box-shadow:
      0 0 0 0 rgba(66, 207, 138, 0);
    opacity: 0.7;
  }

  50% {
    box-shadow:
      0 0 0 7px rgba(66, 207, 138, 0.08);
    opacity: 1;
  }
}

@media (max-width: 1160px) {
  .founder-console {
    grid-template-areas:
      "navigation canvas"
      "activity activity"
      "status status";
    grid-template-columns:
      minmax(190px, 0.22fr)
      minmax(0, 1fr);
    grid-template-rows:
      minmax(0, 1fr)
      auto
      34px;
    overflow-y: auto;
  }

  .founder-activity {
    border-left: 0 !important;
    border-top: 1px solid
      rgba(152, 162, 179, 0.14) !important;
    max-height: 300px;
  }
}

@media (max-width: 760px) {
  body {
    overflow: auto;
  }

  .founder-console {
    display: block;
    height: auto;
    min-height: 100vh;
    overflow: visible;
  }

  .founder-navigation {
    border-bottom: 1px solid
      rgba(152, 162, 179, 0.14) !important;
    border-right: 0 !important;
  }

  .founder-navigation__items {
    display: flex;
    overflow-x: auto;
  }

  .founder-nav-button {
    flex: none;
    width: auto;
  }

  .founder-primary-instruments {
    grid-template-columns: 1fr !important;
  }

  .founder-canvas__header,
  .founder-section-heading {
    align-items: flex-start;
    flex-direction: column;
  }

  .founder-status-bar {
    bottom: 0;
    min-height: 34px;
    position: sticky;
    z-index: 10;
  }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }
}
''',

    "src/founder-console.tsx": r'''import {
  StrictMode,
} from "react";

import {
  createRoot,
} from "react-dom/client";

import {
  FounderConsoleShell,
} from "./nimble/founder-console/FounderConsoleShell";


const root = document.getElementById(
  "founder-console-root",
);

if (!root) {
  throw new Error(
    "Founder Console root is missing.",
  );
}

createRoot(root).render(
  <StrictMode>
    <FounderConsoleShell />
  </StrictMode>,
);
''',

    "founder-console.html": r'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0"
    />
    <meta
      name="theme-color"
      content="#080d16"
    />
    <title>
      AletheusOS Founder Console
    </title>
  </head>

  <body>
    <div id="founder-console-root"></div>

    <script
      type="module"
      src="/src/founder-console.tsx"
    ></script>
  </body>
</html>
''',

    "vite.founder-console.config.ts": r'''import {
  resolve,
} from "node:path";

import react from "@vitejs/plugin-react";

import {
  defineConfig,
} from "vite";


export default defineConfig({
  plugins: [
    react(),
  ],

  build: {
    emptyOutDir: true,
    outDir: "dist-founder-console",

    rollupOptions: {
      input: resolve(
        __dirname,
        "founder-console.html",
      ),
    },
  },
});
''',
}


def write_new(
    relative: str,
    content: str,
) -> None:
    path = SHELL / relative

    if path.exists():
        raise RuntimeError(
            "Refusing to overwrite existing file: "
            + str(path.relative_to(ROOT))
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        content.rstrip() + "\n",
        encoding="utf-8",
    )


def patch_manifest() -> None:
    path = SHELL / "package.json"

    package = json.loads(
        path.read_text(encoding="utf-8")
    )

    scripts = package.setdefault(
        "scripts",
        {},
    )

    scripts.setdefault(
        "build:founder-console",
        "vite build --config vite.founder-console.config.ts",
    )

    dependencies = package.setdefault(
        "dependencies",
        {},
    )

    dependencies.setdefault(
        "@aletheus/nimble-react",
        "0.1.0",
    )

    dependencies.setdefault(
        "@aletheus/nimble-workspace-engine",
        "0.1.0",
    )

    path.write_text(
        json.dumps(
            package,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def write_validator() -> None:
    VALIDATOR.write_text(
        r'''#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SHELL = ROOT / "nimble/apps/platform-shell"

REPORT = (
    ROOT
    / "reports/nimble/experience/"
    "founder-console-shell-validation-latest.json"
)


def main() -> int:
    failures: list[str] = []

    required = [
        "founder-console.html",
        "vite.founder-console.config.ts",
        "src/founder-console.tsx",
        "src/nimble/founder-console/FounderConsoleShell.tsx",
        "src/nimble/founder-console/founder-console.css",
    ]

    for relative in required:
        if not (
            SHELL / relative
        ).is_file():
            failures.append(
                f"Missing Founder Console file: {relative}"
            )

    combined = "\n".join(
        (SHELL / relative).read_text(
            encoding="utf-8"
        )
        for relative in required
        if (SHELL / relative).is_file()
    )

    concepts = [
        "founderWorkspace",
        "Founder Console™",
        "Aletheus Index",
        "THORᵡ",
        "Individual Engine Grades",
        "Activity Rail",
        "Runtime Healthy",
        "prefers-reduced-motion",
        "data-workspace-id",
    ]

    for concept in concepts:
        if concept not in combined:
            failures.append(
                f"Missing Founder Console concept: {concept}"
            )

    commands = [
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-shell",
        ],
        [
            "npm",
            "run",
            "build:founder-console",
            "--workspace",
            "@aletheus/nimble-shell",
        ],
    ]

    results = []

    for command in commands:
        result = subprocess.run(
            command,
            cwd=ROOT / "nimble",
            capture_output=True,
            text=True,
            check=False,
            timeout=240,
        )

        results.append(
            {
                "command": " ".join(command),
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            }
        )

        if result.returncode != 0:
            failures.append(
                "Command failed: "
                + " ".join(command)
            )

    status = (
        "PASS"
        if not failures
        else "FAIL"
    )

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "generated_at": datetime.now(
                    timezone.utc
                ).isoformat(),
                "status": status,
                "failures": failures,
                "commands": results,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ FOUNDER CONSOLE SHELL")
    print("=" * 72)
    print(f"Failures: {len(failures)}")
    print(f"Status: {status}")
    print(
        "Report:",
        REPORT.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    if failures:
        for result in results:
            if result["returncode"] != 0:
                print()
                print(result["command"])
                print(result["stdout"])
                print(result["stderr"])

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
''',
        encoding="utf-8",
    )


def write_tests() -> None:
    TEST_FILE.write_text(
        r'''from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SHELL = (
    ROOT
    / "nimble/apps/platform-shell"
)

COMPONENT = (
    SHELL
    / "src/nimble/founder-console/"
    "FounderConsoleShell.tsx"
)

CSS = COMPONENT.with_name(
    "founder-console.css"
)


def test_founder_console_uses_workspace_definition() -> None:
    text = COMPONENT.read_text(
        encoding="utf-8"
    )

    assert "founderWorkspace" in text
    assert "resolvePanel" in text


def test_founder_console_has_canonical_regions() -> None:
    text = COMPONENT.read_text(
        encoding="utf-8"
    )

    for region in [
        "NavigationPanel",
        "InstrumentationCanvas",
        "ActivityRail",
        "StatusBar",
    ]:
        assert region in text


def test_reserved_instruments_are_separate() -> None:
    text = COMPONENT.read_text(
        encoding="utf-8"
    )

    assert "AletheusIndexInstrument" in text
    assert "ThorxInstrument" in text
    assert "Council Consensus" not in text


def test_individual_engine_grades_are_present() -> None:
    text = COMPONENT.read_text(
        encoding="utf-8"
    )

    for engine in [
        "Evidence Engine™",
        "Knowledge Engine™",
        "Reason Engine™",
        "Memory Engine™",
        "Bias Engine™",
        "Risk Engine™",
        "Predictive Engine™",
    ]:
        assert engine in text


def test_founder_console_is_responsive() -> None:
    css = CSS.read_text(
        encoding="utf-8"
    )

    assert "@media (max-width: 1160px)" in css
    assert "@media (max-width: 760px)" in css


def test_founder_console_respects_reduced_motion() -> None:
    css = CSS.read_text(
        encoding="utf-8"
    )

    assert (
        "@media (prefers-reduced-motion: reduce)"
        in css
    )


def test_founder_console_validator_passes() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_founder_console_shell.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=300,
    )

    assert result.returncode == 0, (
        result.stdout + result.stderr
    )

    assert "Status: PASS" in result.stdout
''',
        encoding="utf-8",
    )


def run(
    command: list[str],
) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(
            result.returncode
        )


def main() -> int:
    for required in REQUIRED:
        if not required.is_file():
            raise RuntimeError(
                "Required package is missing: "
                + str(
                    required.relative_to(ROOT)
                )
            )

    for relative, content in FILES.items():
        write_new(
            relative,
            content,
        )

    patch_manifest()
    write_validator()
    write_tests()

    run(
        [
            "python",
            "-m",
            "py_compile",
            str(VALIDATOR),
        ]
    )

    run(
        [
            "python",
            str(VALIDATOR),
        ]
    )

    run(
        [
            "python",
            "-m",
            "pytest",
            "-q",
            str(TEST_FILE),
        ]
    )

    print()
    print("=" * 72)
    print("FOUNDER CONSOLE SHELL BUILD COMPLETE")
    print("=" * 72)
    print(
        "Run: cd nimble && "
        "npm run dev --workspace "
        "@aletheus/nimble-shell"
    )
    print(
        "Open: "
        "http://localhost:5173/"
        "founder-console.html"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
