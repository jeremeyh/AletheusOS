#!/usr/bin/env python3

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = ROOT / "nimble/packages/workspace"
SRC_ROOT = PACKAGE_ROOT / "src"
ENGINE_ROOT = SRC_ROOT / "engine"

VALIDATOR = ROOT / "validate_nimble_workspace_engine.py"
TEST_FILE = ROOT / "tests/nimble/test_workspace_engine.py"


FILES: dict[str, str] = {
    "contracts.ts": r'''export type WorkspaceDensity =
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
''',

    "lifecycle.ts": r'''import type {
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
''',

    "layout.ts": r'''import type {
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
''',

    "validation.ts": r'''import type {
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
''',

    "registry.ts": r'''import type {
  WorkspaceDefinition,
} from "./contracts";
import {
  validateWorkspace,
} from "./validation";

export class WorkspaceRegistry {
  readonly #workspaces = new Map<
    string,
    WorkspaceDefinition
  >();

  #activeWorkspaceId: string | undefined;

  register(
    workspace: WorkspaceDefinition,
  ): void {
    const validation =
      validateWorkspace(workspace);

    if (!validation.valid) {
      throw new Error(
        [
          "Workspace validation failed:",
          ...validation.failures,
        ].join("\n"),
      );
    }

    if (
      this.#workspaces.has(workspace.id)
    ) {
      throw new Error(
        `Duplicate workspace: ${workspace.id}`,
      );
    }

    this.#workspaces.set(
      workspace.id,
      workspace,
    );
  }

  unregister(id: string): void {
    if (!this.#workspaces.delete(id)) {
      throw new Error(
        `Unknown workspace: ${id}`,
      );
    }

    if (this.#activeWorkspaceId === id) {
      this.#activeWorkspaceId = undefined;
    }
  }

  resolve(id: string): WorkspaceDefinition {
    const workspace =
      this.#workspaces.get(id);

    if (!workspace) {
      throw new Error(
        `Unknown workspace: ${id}`,
      );
    }

    return workspace;
  }

  activate(id: string): WorkspaceDefinition {
    const workspace = this.resolve(id);

    this.#activeWorkspaceId = id;

    return workspace;
  }

  active(): WorkspaceDefinition | undefined {
    return this.#activeWorkspaceId
      ? this.resolve(this.#activeWorkspaceId)
      : undefined;
  }

  list(): readonly WorkspaceDefinition[] {
    return [...this.#workspaces.values()];
  }

  has(id: string): boolean {
    return this.#workspaces.has(id);
  }
}
''',

    "persistence.ts": r'''import type {
  WorkspaceDefinition,
  WorkspaceSnapshot,
} from "./contracts";

export interface WorkspaceStorage {
  read(
    key: string,
  ): string | undefined;

  write(
    key: string,
    value: string,
  ): void;

  remove(
    key: string,
  ): void;
}

export function createWorkspaceSnapshot(
  workspace: WorkspaceDefinition,
  capturedAt = new Date().toISOString(),
): WorkspaceSnapshot {
  return {
    schemaVersion: "1.0",
    capturedAt,
    workspace,
  };
}

export function serializeWorkspaceSnapshot(
  snapshot: WorkspaceSnapshot,
): string {
  return JSON.stringify(snapshot);
}

export function parseWorkspaceSnapshot(
  serialized: string,
): WorkspaceSnapshot {
  const parsed: unknown =
    JSON.parse(serialized);

  if (
    typeof parsed !== "object" ||
    parsed === null ||
    !("schemaVersion" in parsed) ||
    parsed.schemaVersion !== "1.0" ||
    !("workspace" in parsed)
  ) {
    throw new Error(
      "Invalid workspace snapshot.",
    );
  }

  return parsed as WorkspaceSnapshot;
}

export class MemoryWorkspaceStorage
  implements WorkspaceStorage {
  readonly #values = new Map<
    string,
    string
  >();

  read(key: string): string | undefined {
    return this.#values.get(key);
  }

  write(
    key: string,
    value: string,
  ): void {
    this.#values.set(key, value);
  }

  remove(key: string): void {
    this.#values.delete(key);
  }
}
''',

    "founder.ts": r'''import type {
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
''',

    "index.ts": r'''export * from "./contracts";
export * from "./founder";
export * from "./layout";
export * from "./lifecycle";
export * from "./persistence";
export * from "./registry";
export * from "./validation";
''',
}


def write_new(
    path: Path,
    content: str,
) -> None:
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


def patch_package_index() -> None:
    path = SRC_ROOT / "index.ts"
    export_line = 'export * from "./engine";'

    if not path.exists():
        path.write_text(
            export_line + "\n",
            encoding="utf-8",
        )
        return

    text = path.read_text(
        encoding="utf-8"
    )

    if export_line not in text:
        path.write_text(
            text.rstrip()
            + "\n\n"
            + export_line
            + "\n",
            encoding="utf-8",
        )


def write_validator() -> None:
    write_new(
        VALIDATOR,
        r'''#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent

ENGINE_ROOT = (
    ROOT
    / "nimble/packages/workspace/src/engine"
)

REPORT = (
    ROOT
    / "reports/nimble/experience/"
    "workspace-engine-validation-latest.json"
)


def main() -> int:
    failures: list[str] = []

    required_files = [
        "contracts.ts",
        "founder.ts",
        "index.ts",
        "layout.ts",
        "lifecycle.ts",
        "persistence.ts",
        "registry.ts",
        "validation.ts",
    ]

    for relative in required_files:
        if not (
            ENGINE_ROOT / relative
        ).is_file():
            failures.append(
                f"Missing Workspace Engine file: {relative}"
            )

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in ENGINE_ROOT.rglob("*.ts")
    )

    concepts = [
        "Founder Console™",
        "Intelligence Instrumentation™",
        "WorkspaceRegistry",
        "WorkspaceSnapshot",
        "activity-rail",
        "status-bar",
        "floating",
        "detached",
        "founder",
    ]

    for concept in concepts:
        if concept not in combined:
            failures.append(
                f"Missing Workspace Engine concept: {concept}"
            )

    typecheck = subprocess.run(
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-workspace-engine",
        ],
        cwd=ROOT / "nimble",
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )

    if typecheck.returncode != 0:
        failures.append(
            "Workspace Engine typecheck failed."
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
                "typecheck_stdout":
                    typecheck.stdout.strip(),
                "typecheck_stderr":
                    typecheck.stderr.strip(),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ WORKSPACE ENGINE")
    print("=" * 72)
    print(f"Failures: {len(failures)}")
    print(f"Status: {status}")
    print(
        "Report:",
        REPORT.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    if typecheck.returncode != 0:
        print(typecheck.stdout)
        print(typecheck.stderr)

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
''',
    )


def write_tests() -> None:
    write_new(
        TEST_FILE,
        r'''from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

ENGINE_ROOT = (
    ROOT
    / "nimble/packages/workspace/src/engine"
)


def read(relative: str) -> str:
    return (
        ENGINE_ROOT / relative
    ).read_text(encoding="utf-8")


def test_workspace_package_exports_engine() -> None:
    index = (
        ROOT
        / "nimble/packages/workspace/src/index.ts"
    ).read_text(encoding="utf-8")

    assert (
        'export * from "./engine";'
        in index
    )


def test_workspace_registry_exists() -> None:
    assert "class WorkspaceRegistry" in read(
        "registry.ts"
    )


def test_workspace_regions_are_canonical() -> None:
    contracts = read("contracts.ts")

    for region in [
        "navigation",
        "canvas",
        "activity-rail",
        "status-bar",
        "inspector",
        "overlay",
    ]:
        assert f'"{region}"' in contracts


def test_panel_dock_states_are_governed() -> None:
    contracts = read("contracts.ts")

    for state in [
        "left",
        "right",
        "bottom",
        "floating",
        "detached",
        "hidden",
    ]:
        assert f'"{state}"' in contracts


def test_layout_validation_exists() -> None:
    layout = read("layout.ts")

    assert "validateWorkspaceLayout" in layout
    assert "duplicate panel" in layout
    assert "unknown panel" in layout


def test_workspace_persistence_is_versioned() -> None:
    persistence = read("persistence.ts")

    assert 'schemaVersion: "1.0"' in persistence
    assert "Invalid workspace snapshot" in persistence


def test_founder_console_is_reference_workspace() -> None:
    founder = read("founder.ts")

    assert "Founder Console™" in founder
    assert "Intelligence Instrumentation™" in founder
    assert '"founder"' in founder


def test_workspace_engine_validator_passes() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_workspace_engine.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=240,
    )

    assert result.returncode == 0, (
        result.stdout + result.stderr
    )

    assert "Status: PASS" in result.stdout
''',
    )


def run(command: list[str]) -> None:
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
    if ENGINE_ROOT.exists():
        existing = [
            path
            for path in ENGINE_ROOT.rglob("*")
            if path.is_file()
        ]

        if existing:
            raise RuntimeError(
                "Refusing to overwrite existing "
                "Workspace Engine implementation."
            )

    for relative, content in FILES.items():
        write_new(
            ENGINE_ROOT / relative,
            content,
        )

    patch_package_index()
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
    print("WORKSPACE ENGINE BUILD COMPLETE")
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
