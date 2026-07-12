import type {
  CSSProperties,
  HTMLAttributes,
  ReactNode,
} from "react";


export type ExperienceDensity =
  | "consumer"
  | "professional"
  | "enterprise"
  | "founder"
  | "developer";


export type SurfaceVariant =
  | "canvas"
  | "surface"
  | "panel"
  | "raised"
  | "floating"
  | "overlay"
  | "hud"
  | "instrument";


export type InstrumentKind =
  | "numeric"
  | "meter"
  | "gauge"
  | "signal"
  | "trend"
  | "timeline"
  | "status"
  | "authority"
  | "telemetry";


export type InstrumentStatus =
  | "initializing"
  | "healthy"
  | "attention"
  | "review"
  | "critical"
  | "unavailable";


export interface PrimitiveProps
  extends HTMLAttributes<HTMLElement> {
  readonly children?: ReactNode;
  readonly style?: CSSProperties;
}
