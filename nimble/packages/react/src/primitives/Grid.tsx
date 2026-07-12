import {
  forwardRef,
  type HTMLAttributes,
} from "react";

import {
  cssValue,
  type ExperienceTokenName,
} from "./tokens";


export type GridGap =
  | "sm"
  | "md"
  | "lg"
  | "xl";


export interface GridProps
  extends HTMLAttributes<HTMLDivElement> {
  readonly columns?:
    | number
    | string;

  readonly gap?: GridGap;

  readonly minColumnWidth?:
    number;
}


const GAP_TOKENS: Readonly<
  Record<
    GridGap,
    ExperienceTokenName
  >
> = {
  sm: "space.2",
  md: "space.4",
  lg: "space.6",
  xl: "space.10",
};


export const Grid = forwardRef<
  HTMLDivElement,
  GridProps
>(function Grid(
  {
    columns = 1,
    gap = "md",
    minColumnWidth,
    style,
    ...props
  },
  ref,
) {
  const template =
    minColumnWidth !== undefined
      ? [
          "repeat(",
          "auto-fit, ",
          "minmax(",
          `min(100%, ${
            minColumnWidth
          }px), `,
          "1fr)",
          ")",
        ].join("")
      : typeof columns === "number"
        ? `repeat(${
            columns
          }, minmax(0, 1fr))`
        : columns;

  return (
    <div
      ref={ref}
      data-nimble-primitive="grid"
      style={{
        display: "grid",

        gap:
          cssValue(
            GAP_TOKENS[gap],
          ),

        gridTemplateColumns:
          template,

        ...style,
      }}
      {...props}
    />
  );
});
