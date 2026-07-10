import {
  afterEach,
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

import {
  apiRequest,
  clearAuthenticationMetadataCache,
} from "../apiTransport";
import {
  oidcBrowserSession,
} from "../oidcSession";

describe("authenticated API transport", () => {
  beforeEach(() => {
    clearAuthenticationMetadataCache();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("uses no bearer token in local mode", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(
        jsonResponse({
          mode: "local",
          issuer: null,
          audience: null,
          algorithms: ["RS256"],
          localIdentityAllowed: true,
        }),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          ok: true,
        }),
      );

    vi.stubGlobal(
      "fetch",
      fetchMock,
    );

    await apiRequest<{ ok: boolean }>(
      "/api/example",
    );

    const call =
      fetchMock.mock.calls[1];

    const request =
      call?.[1] as RequestInit | undefined;

    const headers =
      new Headers(request?.headers);

    expect(
      headers.has("Authorization"),
    ).toBe(false);
  });

  it("attaches OIDC bearer token", async () => {
    vi.spyOn(
      oidcBrowserSession,
      "getAccessToken",
    ).mockResolvedValue(
      "test-access-token",
    );

    const fetchMock = vi.fn()
      .mockResolvedValueOnce(
        jsonResponse({
          mode: "oidc",
          issuer: "https://issuer.example",
          audience: "api://aletheus",
          algorithms: ["RS256"],
          localIdentityAllowed: false,
        }),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          ok: true,
        }),
      );

    vi.stubGlobal(
      "fetch",
      fetchMock,
    );

    await apiRequest<{ ok: boolean }>(
      "/api/example",
    );

    const call =
      fetchMock.mock.calls[1];

    const request =
      call?.[1] as RequestInit | undefined;

    const headers =
      new Headers(request?.headers);

    expect(
      headers.get("Authorization"),
    ).toBe(
      "Bearer test-access-token",
    );
  });

  it("rejects OIDC requests without a token", async () => {
    vi.spyOn(
      oidcBrowserSession,
      "getAccessToken",
    ).mockResolvedValue(null);

    const fetchMock = vi.fn()
      .mockResolvedValueOnce(
        jsonResponse({
          mode: "oidc",
          issuer: "https://issuer.example",
          audience: "api://aletheus",
          algorithms: ["RS256"],
          localIdentityAllowed: false,
        }),
      );

    vi.stubGlobal(
      "fetch",
      fetchMock,
    );

    await expect(
      apiRequest(
        "/api/identity/me",
      ),
    ).rejects.toMatchObject({
      status: 401,
    });
  });
});

function jsonResponse(
  value: unknown,
): Response {
  return new Response(
    JSON.stringify(value),
    {
      status: 200,
      headers: {
        "Content-Type":
          "application/json",
      },
    },
  );
}
