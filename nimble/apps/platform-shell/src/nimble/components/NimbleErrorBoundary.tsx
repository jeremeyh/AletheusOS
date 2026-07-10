import {
  Component,
} from "react";
import type {
  ErrorInfo,
  ReactNode,
} from "react";

interface NimbleErrorBoundaryProps {
  readonly children: ReactNode;
  readonly scope: string;
  readonly onReset?: () => void;
}

interface NimbleErrorBoundaryState {
  readonly error: Error | null;
}

export class NimbleErrorBoundary extends Component<
  NimbleErrorBoundaryProps,
  NimbleErrorBoundaryState
> {
  state: NimbleErrorBoundaryState = {
    error: null,
  };

  static getDerivedStateFromError(
    error: Error,
  ): NimbleErrorBoundaryState {
    return {
      error,
    };
  }

  componentDidCatch(
    error: Error,
    info: ErrorInfo,
  ): void {
    console.error(
      `Nimble boundary failure: ${this.props.scope}`,
      {
        error,
        componentStack:
          info.componentStack,
      },
    );
  }

  private reset = (): void => {
    this.setState({
      error: null,
    });

    this.props.onReset?.();
  };

  render(): ReactNode {
    const {
      error,
    } = this.state;

    if (!error) {
      return this.props.children;
    }

    return (
      <section
        className="nimble-boundary-failure"
        role="alert"
      >
        <p className="nimble-panel__eyebrow">
          Principle X · Failure disclosed
        </p>

        <h2>
          This experience could not be loaded
        </h2>

        <p>
          Scope: {this.props.scope}
        </p>

        <pre>
          {error.message}
        </pre>

        <div className="nimble-command-actions">
          <button
            className="nimble-button nimble-button--secondary"
            type="button"
            onClick={() => {
              window.location.reload();
            }}
          >
            Reload application
          </button>

          <button
            className="nimble-button nimble-button--primary"
            type="button"
            onClick={this.reset}
          >
            Retry experience
          </button>
        </div>
      </section>
    );
  }
}
