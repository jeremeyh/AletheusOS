import {
  type HTMLAttributes,
} from "react";

import {
  cssValue,
} from "./tokens";


export type BadgeIntent =
  | "neutral"
  | "healthy"
  | "attention"
  | "critical"
  | "authority";


export interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement> {
  readonly intent?: BadgeIntent;
}


const INTENT_TOKENS = {
  neutral: "text.secondary",
  healthy:
    "instrumentation.status.healthy",
  attention:
    "instrumentation.status.attention",
  critical:
    "instrumentation.status.critical",
  authority:
    "instrumentation.thorx.guard",
} as const;


export function Badge({
  intent = "neutral",
  style,
  ...props
}: BadgeProps) {
  const color =
    cssValue(
      INTENT_TOKENS[intent],
    );

  return (
    <span
      data-nimble-primitive="badge"
      data-intent={intent}
      style={{
        border:
          `1px solid ${
            color
          }`,
        borderRadius:
          cssValue("radius.pill"),
        color,
        display: "inline-flex",
        fontFamily:
          cssValue(
            "font.family.instrument",
          ),
        fontSize:
          cssValue(
            "font.size.caption",
          ),
        letterSpacing: "0.06em",
        padding:
          `${cssValue(
            "space.1",
          )} ${cssValue(
            "space.3",
          )}`,
        textTransform: "uppercase",
        ...style,
      }}
      {...props}
    />
  );
}
