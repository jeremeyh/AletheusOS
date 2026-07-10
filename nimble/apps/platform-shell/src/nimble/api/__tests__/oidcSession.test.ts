import {
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

describe("lazy OIDC session", () => {
  beforeEach(() => {
    vi.resetModules();
  });

  it("remains unconfigured without browser OIDC values", async () => {
    const {
      oidcBrowserSession,
    } = await import("../oidcSession");

    await oidcBrowserSession.initialize();

    expect(
      oidcBrowserSession.getSnapshot(),
    ).toMatchObject({
      state: "unconfigured",
      user: null,
      error: null,
    });
  });

  it("returns no token when OIDC is unconfigured", async () => {
    const {
      oidcBrowserSession,
    } = await import("../oidcSession");

    await expect(
      oidcBrowserSession.getAccessToken(),
    ).resolves.toBeNull();
  });
});
