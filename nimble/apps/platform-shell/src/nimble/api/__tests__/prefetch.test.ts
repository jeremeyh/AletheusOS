import {
  describe,
  expect,
  it,
} from "vitest";

import {
  preloadCommandHistory,
  preloadCommandSurface,
  preloadOidcCallback,
  preloadPrincipalPanel,
} from "../../prefetch";

describe("Nimble lazy prefetch boundaries", () => {
  it("loads the command surface module", async () => {
    const module =
      await preloadCommandSurface();

    expect(module).toHaveProperty(
      "CommandSurface",
    );
  });

  it("loads the command history module", async () => {
    const module =
      await preloadCommandHistory();

    expect(module).toHaveProperty(
      "CommandHistoryRoute",
    );
  });

  it("loads the principal panel module", async () => {
    const module =
      await preloadPrincipalPanel();

    expect(module).toHaveProperty(
      "PrincipalPanel",
    );
  });

  it("loads the OIDC callback module", async () => {
    const module =
      await preloadOidcCallback();

    expect(module).toHaveProperty(
      "OidcCallbackRoute",
    );
  });
});
