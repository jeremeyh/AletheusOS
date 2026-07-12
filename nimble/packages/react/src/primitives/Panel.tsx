import {
  forwardRef,
  type HTMLAttributes,
} from "react";

import {
  Surface,
} from "./Surface";

import {
  Stack,
  type StackSpacing,
} from "./Stack";

import {
  Text,
} from "./Text";


export interface PanelProps
  extends HTMLAttributes<HTMLDivElement> {
  readonly title?: string;
  readonly description?: string;
  readonly spacing?: StackSpacing;
}


export const Panel = forwardRef<
  HTMLDivElement,
  PanelProps
>(function Panel(
  {
    title,
    description,
    spacing = "lg",
    children,
    style,
    ...props
  },
  ref,
) {
  return (
    <Surface
      ref={ref}
      variant="panel"
      data-nimble-primitive="panel"
      style={{
        padding: 24,
        ...style,
      }}
      {...props}
    >
      <Stack spacing={spacing}>
        {title ? (
          <div>
            <Text
              as="h2"
              variant="heading"
            >
              {title}
            </Text>

            {description ? (
              <Text
                as="p"
                muted
                style={{
                  marginTop: 6,
                }}
              >
                {description}
              </Text>
            ) : null}
          </div>
        ) : null}

        {children}
      </Stack>
    </Surface>
  );
});
