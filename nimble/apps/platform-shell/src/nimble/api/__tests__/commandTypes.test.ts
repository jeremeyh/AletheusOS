import {
  describe,
  expect,
  it,
} from "vitest";

import type {
  CommandDefinition,
} from "../commandTypes";

describe("command contracts", () => {
  it("preserves governed command metadata", () => {
    const command: CommandDefinition = {
      id: "runtime.describe",
      name: "Describe runtime",
      description: "Read bounded runtime state.",
      risk: "read_only",
      reversible: false,
      authorizationRequired: false,
      requiredArguments: [],
      effects: [
        "Reads bounded runtime state",
      ],
      requiredEntitlements: [
        "runtime.read",
      ],
    };

    expect(command.risk).toBe("read_only");
    expect(command.authorizationRequired).toBe(false);
    expect(command.reversible).toBe(false);
  });
});
