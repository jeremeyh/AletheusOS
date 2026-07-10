export type AuthenticationMode =
  | "local"
  | "oidc";

export interface AuthenticationMetadata {
  readonly mode: AuthenticationMode;
  readonly issuer: string | null;
  readonly audience: string | null;
  readonly algorithms: readonly string[];
  readonly localIdentityAllowed: boolean;
}

export interface AccessTokenProvider {
  getAccessToken(): Promise<string | null>;
}
