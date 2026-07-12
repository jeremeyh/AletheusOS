import {
  forwardRef,
  type CSSProperties,
  type HTMLAttributes,
} from "react";

import {
  cssValue,
} from "./tokens";

import type {
  SurfaceVariant,
} from "./types";


export interface SurfaceProps
  extends HTMLAttributes<HTMLDivElement> {
  readonly variant?: SurfaceVariant;
  readonly interactive?: boolean;
}


const VARIANT_STYLES: Readonly<
  Record<
    SurfaceVariant,
    CSSProperties
  >
> = {
  canvas: {
    background:
      cssValue("surface.canvas"),
    color:
      cssValue("text.primary"),
  },

  surface: {
    background:
      cssValue("surface.primary"),
    color:
      cssValue("text.primary"),
  },

  panel: {
    background:
      cssValue("surface.secondary"),
    border:
      `1px solid ${
        cssValue("border.subtle")
      }`,
    color:
      cssValue("text.primary"),
  },

  raised: {
    background:
      cssValue("surface.raised"),
    boxShadow:
      cssValue("elevation.raised"),
    color:
      cssValue("text.primary"),
  },

  floating: {
    background:
      cssValue("surface.raised"),
    boxShadow:
      cssValue("elevation.floating"),
    color:
      cssValue("text.primary"),
  },

  overlay: {
    background:
      cssValue("surface.primary"),
    boxShadow:
      cssValue("elevation.overlay"),
    color:
      cssValue("text.primary"),
  },

  hud: {
    background:
      cssValue("surface.primary"),
    boxShadow:
      cssValue("elevation.hud"),
    color:
      cssValue("text.primary"),
  },

  instrument: {
    background:
      cssValue(
        "instrumentation.surface",
      ),
    border:
      `1px solid ${
        cssValue(
          "instrumentation.border",
        )
      }`,
    color:
      cssValue(
        "instrumentation.value",
      ),
  },
};


export const Surface = forwardRef<
  HTMLDivElement,
  SurfaceProps
>(function Surface(
  {
    variant = "surface",
    interactive = false,
    style,
    ...props
  },
  ref,
) {
  return (
    <div
      ref={ref}
      data-nimble-primitive="surface"
      data-variant={variant}
      data-interactive={
        interactive || undefined
      }
      style={{
        borderRadius:
          cssValue("radius.lg"),
        boxSizing: "border-box",

        transition: interactive
          ? [
              "transform",
              cssValue(
                "motion.duration.fast",
              ),
              cssValue(
                "motion.easing.standard",
              ),
            ].join(" ")
          : undefined,

        ...VARIANT_STYLES[variant],
        ...style,
      }}
      {...props}
    />
  );
});
