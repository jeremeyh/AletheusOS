import type {
  AccessTokenProvider,
} from "./authTypes";

const sessionTokenKey =
  "aletheus.session.access-token";

class BrowserSessionTokenProvider
implements AccessTokenProvider {
  async getAccessToken(): Promise<string | null> {
    const token =
      window.sessionStorage.getItem(
        sessionTokenKey,
      );

    return token?.trim() || null;
  }

  setAccessToken(token: string): void {
    window.sessionStorage.setItem(
      sessionTokenKey,
      token,
    );
  }

  clearAccessToken(): void {
    window.sessionStorage.removeItem(
      sessionTokenKey,
    );
  }
}

export const sessionTokenProvider =
  new BrowserSessionTokenProvider();
