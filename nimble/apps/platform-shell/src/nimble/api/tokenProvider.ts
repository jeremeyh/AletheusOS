import type {
  AccessTokenProvider,
} from "./authTypes";
import {
  oidcBrowserSession,
} from "./oidcSession";

class OidcAccessTokenProvider
implements AccessTokenProvider {
  getAccessToken(): Promise<string | null> {
    return oidcBrowserSession
      .getAccessToken();
  }
}

export const sessionTokenProvider =
  new OidcAccessTokenProvider();
