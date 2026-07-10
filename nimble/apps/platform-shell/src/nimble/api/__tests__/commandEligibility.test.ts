import {
  describe,
  expect,
  it,
} from "vitest";

import {
  evaluateCommandEligibility,
} from "../commandEligibility";
import type {
  CommandDefinition,
} from "../commandTypes";
import type {
  CurrentPrincipal,
} from "../identityTypes";

const command: CommandDefinition = {
  id: "experience.inspector.set",
  name: "Set inspector state",
  description: "Change the inspector preference.",
  risk: "low",
  reversible: true,
  authorizationRequired: true,
  requiredArguments: ["open"],
  effects: [
    "Changes one experience preference",
  ],
  requiredEntitlements: [
    "experience.preferences.write",
  ],
};

describe("command eligibility", () => {
  it("allows an entitled operator", () => {
    const principal: CurrentPrincipal = {
      subjectId: "operator-1",
      displayName: "Operator",
      roles: ["operator"],
      entitlements: [
        "experience.preferences.write",
      ],
      authenticationMethod: "test",
      authenticated: true,
    };

    expect(
      evaluateCommandEligibility(
        command,
        principal,
      ).eligible,
    ).toBe(true);
  });

  it("denies a viewer by role", () => {
    const principal: CurrentPrincipal = {
      subjectId: "viewer-1",
      displayName: "Viewer",
      roles: ["viewer"],
      entitlements: [
        "experience.preferences.write",
      ],
      authenticationMethod: "test",
      authenticated: true,
    };

    const result =
      evaluateCommandEligibility(
        command,
        principal,
      );

    expect(result.eligible).toBe(false);
    expect(result.reason).toContain("Operator");
  });

  it("denies a principal missing entitlement", () => {
    const principal: CurrentPrincipal = {
      subjectId: "operator-1",
      displayName: "Operator",
      roles: ["operator"],
      entitlements: [],
      authenticationMethod: "test",
      authenticated: true,
    };

    const result =
      evaluateCommandEligibility(
        command,
        principal,
      );

    expect(result.eligible).toBe(false);
    expect(result.missingEntitlements).toEqual([
      "experience.preferences.write",
    ]);
  });
});
