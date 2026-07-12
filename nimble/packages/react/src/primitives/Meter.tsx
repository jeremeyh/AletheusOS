import {
  type HTMLAttributes,
} from "react";

import {
  cssValue,
} from "./tokens";


export interface MeterProps
  extends Omit<
    HTMLAttributes<HTMLDivElement>,
    "children"
  > {
  readonly value: number;
  readonly minimum?: number;
  readonly maximum?: number;
  readonly segments?: number;
  readonly label?: string;
}


export function Meter({
  value,
  minimum = 0,
  maximum = 100,
  segments = 20,
  label,
  style,
  ...props
}: MeterProps) {
  const bounded =
    Math.max(
      minimum,
      Math.min(maximum, value),
    );

  const range =
    maximum - minimum;

  const ratio =
    range > 0
      ? (
          bounded - minimum
        ) / range
      : 0;

  const activeSegments =
    Math.round(
      ratio * segments,
    );

  return (
    <div
      role="meter"
      aria-label={label}
      aria-valuemin={minimum}
      aria-valuemax={maximum}
      aria-valuenow={bounded}
      data-nimble-primitive="meter"
      style={{
        display: "grid",
        gap:
          cssValue("space.1"),
        gridTemplateColumns:
          `repeat(${
            segments
          }, minmax(2px, 1fr))`,
        ...style,
      }}
      {...props}
    >
      {Array.from(
        {
          length: segments,
        },
        (_, index) => (
          <span
            key={index}
            aria-hidden="true"
            data-active={
              index < activeSegments
                ? "true"
                : "false"
            }
            style={{
              background:
                index < activeSegments
                  ? "currentColor"
                  : "rgba(152, 162, 179, 0.13)",

              borderRadius: 2,
              height: 14,

              transition: [
                "background",
                cssValue(
                  "motion.duration.normal",
                ),
                cssValue(
                  "motion.easing.standard",
                ),
              ].join(" "),
            }}
          />
        ),
      )}
    </div>
  );
}
