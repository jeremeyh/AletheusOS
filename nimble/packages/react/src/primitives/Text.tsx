import {
  createElement,
  forwardRef,
  type CSSProperties,
  type ElementType,
  type HTMLAttributes,
} from "react";

import {
  cssValue,
  token,
  type ExperienceTokenName,
} from "./tokens";


export type TextVariant =
  | "display"
  | "heading"
  | "body"
  | "caption"
  | "label"
  | "instrument"
  | "telemetry"
  | "code";


export interface TextProps
  extends HTMLAttributes<HTMLElement> {
  readonly as?: ElementType;
  readonly variant?: TextVariant;
  readonly muted?: boolean;
}


interface TextDefinition {
  readonly fontFamily:
    ExperienceTokenName;

  readonly fontSize:
    ExperienceTokenName;

  readonly fontWeight:
    ExperienceTokenName;

  readonly lineHeight: number;
}


const DEFINITIONS: Readonly<
  Record<
    TextVariant,
    TextDefinition
  >
> = {
  display: {
    fontFamily:
      "font.family.interface",

    fontSize:
      "font.size.display",

    fontWeight:
      "font.weight.bold",

    lineHeight: 1.05,
  },

  heading: {
    fontFamily:
      "font.family.interface",

    fontSize:
      "font.size.heading.md",

    fontWeight:
      "font.weight.semibold",

    lineHeight: 1.2,
  },

  body: {
    fontFamily:
      "font.family.interface",

    fontSize:
      "font.size.body.md",

    fontWeight:
      "font.weight.regular",

    lineHeight: 1.5,
  },

  caption: {
    fontFamily:
      "font.family.interface",

    fontSize:
      "font.size.caption",

    fontWeight:
      "font.weight.medium",

    lineHeight: 1.4,
  },

  label: {
    fontFamily:
      "font.family.interface",

    fontSize:
      "font.size.body.sm",

    fontWeight:
      "font.weight.semibold",

    lineHeight: 1.3,
  },

  instrument: {
    fontFamily:
      "font.family.instrument",

    fontSize:
      "font.size.heading.lg",

    fontWeight:
      "font.weight.semibold",

    lineHeight: 1.1,
  },

  telemetry: {
    fontFamily:
      "font.family.instrument",

    fontSize:
      "font.size.body.sm",

    fontWeight:
      "font.weight.medium",

    lineHeight: 1.35,
  },

  code: {
    fontFamily:
      "font.family.instrument",

    fontSize:
      "font.size.body.sm",

    fontWeight:
      "font.weight.regular",

    lineHeight: 1.5,
  },
};


export const Text = forwardRef<
  HTMLElement,
  TextProps
>(function Text(
  {
    as = "span",
    variant = "body",
    muted = false,
    style,
    ...props
  },
  ref,
) {
  const definition =
    DEFINITIONS[variant];

  const fontWeight =
    token(
      definition.fontWeight,
    );

  const computedStyle:
    CSSProperties = {
      color:
        cssValue(
          muted
            ? "text.muted"
            : "text.primary",
        ),

      fontFamily:
        cssValue(
          definition.fontFamily,
        ),

      fontSize:
        cssValue(
          definition.fontSize,
        ),

      fontWeight:
        typeof fontWeight === "number"
          ? fontWeight
          : undefined,

      lineHeight:
        definition.lineHeight,

      margin: 0,

      ...style,
    };

  return createElement(
    as,
    {
      ...props,
      ref,

      "data-nimble-primitive":
        "text",

      "data-variant":
        variant,

      style:
        computedStyle,
    },
  );
});
