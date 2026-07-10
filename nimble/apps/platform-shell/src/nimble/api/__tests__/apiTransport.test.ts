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
  sessionTokenProvider,
} from "../tokenProvider";

describe("authenticated API transport", () => {
  beforeEach(() => {
    clearAuthenticationMetadataCache();
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("uses no bearer token in local mode", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            mode: "local",
            issuer: null,
            audience: null,
            algorithms: ["RS256"],
            localIdentityAllowed: true,
          }),
          {
            status: 200,
            headers: {
              "Content-Type":
                "application/json",
            },
          },
        ),
      )
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            ok: true,
          }),
          {
            status: 200,
            headers: {
              "Content-Type":
                "application/json",
            },
          },
        ),
      );

    vi.stubGlobal(
      "fetch",
      fetchMock,
    );

    await apiRequest<{ ok: boolean }>(
      "/api/example",
    );

    const secondRequest =
      fetchMock.mock.calls[1]?.[1]
        as RequestInit;

    const headers =
      new Headers(secondRequest.headers);

    expect(
      headers.has("Authorization"),
    ).toBe(false);
  });

  it("attaches bearer token in OIDC mode", async () => {
    sessionTokenProvider.setAccessToken(
      "test-access-token",
    );

    const fetchMock = vi.fn()
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            mode: "oidc",
            issuer: "https://issuer.example",
            audience: "api://aletheus",
            algorithms: ["RS256"],
            localIdentityAllowed: false,
          }),
          {
            status: 200,
            headers: {
              "Content-Type":
                "application/json",
            },
          },
        ),
      )
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            ok: true,
          }),
          {
            status: 200,
            headers: {
              "Content-Type":
                "application/json",
            },
          },
        ),
      );

    vi.stubGlobal(
      "fetch",
      fetchMock,
    );

    await apiRequest<{ ok: boolean }>(
      "/api/example",
    );

    const secondRequest =
      fetchMock.mock.calls[1]?.[1]
        as RequestInit;

    const headers =
      new Headers(secondRequest.headers);

    expect(
      headers.get("Authorization"),
    ).toBe(
      "Bearer test-access-token",
    );
  });

  it("rejects OIDC calls when token is absent", async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce(
        new Response(
          JSON.stringify({
            mode: "oidc",
            issuer: "https://issuer.example",
            audience: "api://aletheus",
            algorithms: ["RS256"],
            localIdentityAllowed: false,
          }),
          {
            status: 200,
            headers: {
              "Content-Type":
                "application/json",
            },
          },
        ),
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
