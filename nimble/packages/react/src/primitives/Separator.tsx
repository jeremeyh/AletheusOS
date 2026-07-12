import {
  type HTMLAttributes,
} from "react";

import {
  cssValue,
} from "./tokens";


export interface SeparatorProps
  extends HTMLAttributes<HTMLHRElement> {
  readonly orientation?:
    | "horizontal"
    | "vertical";
}


export function Separator({
  orientation = "horizontal",
  style,
  ...props
}: SeparatorProps) {
  return (
    <hr
      aria-orientation={orientation}
      data-nimble-primitive="separator"
      style={{
        background:
          cssValue("border.subtle"),
        border: 0,
        flex: "none",
        height:
          orientation === "horizontal"
            ? 1
            : "auto",
        margin: 0,
        minHeight:
          orientation === "vertical"
            ? 20
            : undefined,
        width:
          orientation === "horizontal"
            ? "100%"
            : 1,
        ...style,
      }}
      {...props}
    />
  );
}
