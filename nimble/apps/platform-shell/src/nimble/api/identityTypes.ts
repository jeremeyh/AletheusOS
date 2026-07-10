export type PrincipalRole =
  | "viewer"
  | "operator"
  | "administrator"
  | "platform_architect";

export interface CurrentPrincipal {
  readonly subjectId: string;
  readonly displayName: string;
  readonly roles: readonly PrincipalRole[];
  readonly entitlements: readonly string[];
  readonly authenticationMethod: string;
  readonly authenticated: boolean;
}
