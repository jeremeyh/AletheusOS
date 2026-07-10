import type {
  CommandDefinition,
  CommandRisk,
} from "./commandTypes";
import type {
  CurrentPrincipal,
  PrincipalRole,
} from "./identityTypes";

const roleRank: Record<PrincipalRole, number> = {
  viewer: 10,
  operator: 20,
  administrator: 30,
  platform_architect: 40,
};

const minimumRoleByRisk: Record<
  CommandRisk,
  PrincipalRole
> = {
  read_only: "viewer",
  low: "operator",
  moderate: "administrator",
  high: "platform_architect",
};

export interface CommandEligibility {
  readonly eligible: boolean;
  readonly reason: string;
  readonly missingEntitlements: readonly string[];
}

export function evaluateCommandEligibility(
  command: CommandDefinition,
  principal: CurrentPrincipal,
): CommandEligibility {
  if (!principal.authenticated) {
    return {
      eligible: false,
      reason: "The current principal is not authenticated.",
      missingEntitlements: [],
    };
  }

  const principalRank = Math.max(
    ...principal.roles.map(
      (role) => roleRank[role],
    ),
  );

  const minimumRole =
    minimumRoleByRisk[command.risk];

  if (principalRank < roleRank[minimumRole]) {
    return {
      eligible: false,
      reason:
        `${formatRole(minimumRole)} or higher is required.`,
      missingEntitlements: [],
    };
  }

  const missingEntitlements =
    command.requiredEntitlements.filter(
      (entitlement) =>
        !principal.entitlements.includes(entitlement),
    );

  if (missingEntitlements.length) {
    return {
      eligible: false,
      reason:
        "The current principal lacks required entitlements.",
      missingEntitlements,
    };
  }

  return {
    eligible: true,
    reason:
      "Role and entitlement requirements appear satisfied.",
    missingEntitlements: [],
  };
}

function formatRole(value: string): string {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) =>
      character.toUpperCase()
    );
}
