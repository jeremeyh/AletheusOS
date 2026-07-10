export type CommandRisk =
  | "read_only"
  | "low"
  | "moderate"
  | "high";

export type CommandState =
  | "previewed"
  | "authorized"
  | "executed"
  | "rejected"
  | "failed"
  | "reversed";

export interface CommandDefinition {
  readonly id: string;
  readonly name: string;
  readonly description: string;
  readonly risk: CommandRisk;
  readonly reversible: boolean;
  readonly authorizationRequired: boolean;
  readonly requiredArguments: readonly string[];
  readonly effects: readonly string[];
  readonly requiredEntitlements: readonly string[];
}

export interface CommandPreviewRequest {
  readonly command_id: string;
  readonly arguments: Readonly<Record<string, unknown>>;
  readonly idempotency_key?: string;
}

export interface CommandPreview {
  readonly preview_id: string;
  readonly command_id: string;
  readonly name: string;
  readonly description: string;
  readonly risk: CommandRisk;
  readonly arguments: Readonly<Record<string, unknown>>;
  readonly effects: readonly string[];
  readonly required_entitlements: readonly string[];
  readonly reversible: boolean;
  readonly authorization_required: boolean;
  readonly requested_by: string;
  readonly created_at: string;
  readonly expires_at: string;
  readonly state: "previewed";
}

export interface CommandAuthorization {
  readonly authorization_id: string;
  readonly preview_id: string;
  readonly authorized_by: string;
  readonly authorized_at: string;
  readonly expires_at: string;
  readonly state: "authorized";
}

export interface CommandExecution {
  readonly execution_id: string;
  readonly preview_id: string;
  readonly authorization_id: string | null;
  readonly command_id: string;
  readonly state:
    | "executed"
    | "failed"
    | "reversed";
  readonly result: Readonly<Record<string, unknown>>;
  readonly requested_by: string;
  readonly executed_at: string;
  readonly reversible: boolean;
  readonly reversal_token: string | null;
  readonly failure: string | null;
}

export interface CommandExecutionRequest {
  readonly preview_id: string;
  readonly authorization_id: string | null;
  readonly idempotency_key?: string;
}

export interface CommandReversalRequest {
  readonly execution_id: string;
  readonly reversal_token: string;
}

export interface CommandApiFailure {
  readonly detail: string;
}
