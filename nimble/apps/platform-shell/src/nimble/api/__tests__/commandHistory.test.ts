import {
  describe,
  expect,
  it,
} from "vitest";

import type {
  CommandExecution,
} from "../commandTypes";

describe("command history contracts", () => {
  it("preserves failure disclosure", () => {
    const execution: CommandExecution = {
      execution_id: "execution-1",
      preview_id: "preview-1",
      authorization_id: null,
      command_id: "runtime.describe",
      state: "failed",
      result: {},
      requested_by: "jeremey",
      executed_at: "2026-07-10T12:00:00+00:00",
      reversible: false,
      reversal_token: null,
      failure: "Runtime provider unavailable.",
    };

    expect(execution.state).toBe("failed");
    expect(execution.failure).toContain(
      "unavailable",
    );
  });

  it("preserves reversal state", () => {
    const execution: CommandExecution = {
      execution_id: "execution-2",
      preview_id: "preview-2",
      authorization_id: "authorization-1",
      command_id: "experience.inspector.set",
      state: "reversed",
      result: {
        reversal: {
          restored: true,
        },
      },
      requested_by: "jeremey",
      executed_at: "2026-07-10T12:05:00+00:00",
      reversible: true,
      reversal_token: null,
      failure: null,
    };

    expect(execution.state).toBe("reversed");
    expect(execution.reversal_token).toBeNull();
  });
});
