import {
  type HTMLAttributes,
} from "react";

import {
  cssValue,
} from "./tokens";

import type {
  InstrumentStatus,
} from "../instrumentation/contracts";


export interface SignalProps
  extends HTMLAttributes<HTMLSpanElement> {
  readonly status:
    InstrumentStatus;

  readonly label?: string;
}


const STATUS_TOKENS = {
  initializing:
    "text.muted",

  healthy:
    "instrumentation.status.healthy",

  attention:
    "instrumentation.status.attention",

  review:
    "instrumentation.status.attention",

  critical:
    "instrumentation.status.critical",

  unavailable:
    "text.muted",
} as const;


export function Signal({
  status,
  label,
  style,
  ...props
}: SignalProps) {
  const color =
    cssValue(
      STATUS_TOKENS[status],
    );

  return (
    <span
      data-nimble-primitive="signal"
      data-status={status}
      style={{
        alignItems: "center",
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
        gap:
          cssValue("space.2"),
        ...style,
      }}
      {...props}
    >
      <span
        aria-hidden="true"
        style={{
          background: color,
          borderRadius: "50%",
          boxShadow:
            `0 0 10px ${
              color
            }`,
          height: 7,
          width: 7,
        }}
      />

      {label ?? status}
    </span>
  );
}
