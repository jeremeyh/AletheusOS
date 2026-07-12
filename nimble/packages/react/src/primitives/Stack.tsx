import {
  forwardRef,
  type CSSProperties,
  type HTMLAttributes,
} from "react";

import {
  cssValue,
  type ExperienceTokenName,
} from "./tokens";


export type StackSpacing =
  | "none"
  | "xs"
  | "sm"
  | "md"
  | "lg"
  | "xl"
  | "2xl";


export interface StackProps
  extends HTMLAttributes<HTMLDivElement> {
  readonly direction?:
    | "row"
    | "column";

  readonly spacing?: StackSpacing;

  readonly align?:
    CSSProperties["alignItems"];

  readonly justify?:
    CSSProperties["justifyContent"];

  readonly wrap?: boolean;
}


const SPACING_TOKENS: Readonly<
  Record<
    StackSpacing,
    ExperienceTokenName
  >
> = {
  none: "space.0",
  xs: "space.1",
  sm: "space.2",
  md: "space.4",
  lg: "space.6",
  xl: "space.10",
  "2xl": "space.16",
};


export const Stack = forwardRef<
  HTMLDivElement,
  StackProps
>(function Stack(
  {
    direction = "column",
    spacing = "md",
    align,
    justify,
    wrap = false,
    style,
    ...props
  },
  ref,
) {
  return (
    <div
      ref={ref}
      data-nimble-primitive="stack"
      data-direction={direction}
      style={{
        alignItems: align,
        display: "flex",
        flexDirection: direction,

        flexWrap: wrap
          ? "wrap"
          : "nowrap",

        gap:
          cssValue(
            SPACING_TOKENS[
              spacing
            ],
          ),

        justifyContent: justify,

        ...style,
      }}
      {...props}
    />
  );
});
