export type {
  NimbleApplicationIdentity,
  NimblePreferences,
  NimbleTruthEnvelope,
} from "@aletheus/nimble-core";

export interface NimbleSurfaceProps {
  readonly surfaceId: string;
  readonly label: string;
  readonly busy?: boolean;
  readonly disabled?: boolean;
}
