const SCHEMA =
  "aletheusos.workspace-studio.read-model.v1";

const ALLOWED = new Set([
  "inspect_workspace_identity",
  "inspect_workspace_state",
  "inspect_workspace_layout",
  "inspect_workspace_registry",
  "inspect_workspace_validation",
  "inspect_workspace_lifecycle",
  "inspect_workspace_experience"
]);

const REFUSED_PREFIXES = [
  "create",
  "update",
  "delete",
  "write",
  "persist",
  "transition",
  "register",
  "unregister",
  "execute",
  "invoke",
  "perform"
];

function refusal(operation, reason) {
  return Object.freeze({
    status: "REFUSED",
    operation,
    reason
  });
}

export function validateWorkspaceStudioReadModel(
  snapshot
) {
  if (
    !snapshot ||
    typeof snapshot !== "object"
  ) {
    return Object.freeze({
      valid: false,
      status: "DEGRADED_READ_ONLY",
      reason: "snapshot_not_object"
    });
  }

  if (snapshot.schema !== SCHEMA) {
    return Object.freeze({
      valid: false,
      status: "DEGRADED_READ_ONLY",
      reason: "schema_mismatch"
    });
  }

  if (snapshot.mode !== "READ_ONLY") {
    return Object.freeze({
      valid: false,
      status: "DEGRADED_READ_ONLY",
      reason: "mode_not_read_only"
    });
  }

  const runtime = snapshot.runtime || {};

  if (
    runtime.mutation_authority !== false ||
    runtime.direct_execution !== false ||
    runtime.external_transport !== false ||
    runtime.command_adapter_invocation !== false
  ) {
    return Object.freeze({
      valid: false,
      status: "DEGRADED_READ_ONLY",
      reason: "runtime_boundary_violation"
    });
  }

  return Object.freeze({
    valid: true,
    status: "READ_ONLY",
    reason: null
  });
}

export function createWorkspaceStudioAdapter(
  snapshot
) {
  const validation =
    validateWorkspaceStudioReadModel(
      snapshot
    );

  if (!validation.valid) {
    return Object.freeze({
      status: validation.status,

      inspect(operation) {
        return refusal(
          operation,
          validation.reason
        );
      },

      snapshot() {
        return null;
      }
    });
  }

  const frozenSnapshot =
    Object.freeze(snapshot);

  const sectionMap = Object.freeze({
    inspect_workspace_identity:
      "identity",

    inspect_workspace_state:
      "state",

    inspect_workspace_layout:
      "layout",

    inspect_workspace_registry:
      "registry",

    inspect_workspace_validation:
      "state",

    inspect_workspace_lifecycle:
      "state",

    inspect_workspace_experience:
      "experience"
  });

  return Object.freeze({
    status: "READ_ONLY",

    inspect(operation) {
      const normalized =
        String(operation || "")
          .trim();

      const lower =
        normalized.toLowerCase();

      if (
        REFUSED_PREFIXES.some(
          prefix =>
            lower.startsWith(prefix)
        )
      ) {
        return refusal(
          normalized,
          "Workspace Studio read-only boundary"
        );
      }

      if (!ALLOWED.has(normalized)) {
        return refusal(
          normalized,
          "Unknown Workspace Studio operation"
        );
      }

      const section =
        sectionMap[normalized];

      return Object.freeze({
        status: "READ_ONLY",
        operation: normalized,
        section,
        data: frozenSnapshot[section]
      });
    },

    snapshot() {
      return frozenSnapshot;
    }
  });
}
