export type SignalSubscriber<T> = (value: T) => void;

export class ReactiveSignal<T> {
  private readonly subscribers = new Set<SignalSubscriber<T>>();

  constructor(private value: T) {}

  get(): T {
    return this.value;
  }

  set(value: T): void {
    if (Object.is(this.value, value)) return;
    this.value = value;
    for (const subscriber of this.subscribers) {
      subscriber(value);
    }
  }

  subscribe(subscriber: SignalSubscriber<T>): () => void {
    this.subscribers.add(subscriber);
    subscriber(this.value);
    return () => this.subscribers.delete(subscriber);
  }
}

export class ReactiveSignalGraph {
  private readonly signals = new Map<string, ReactiveSignal<unknown>>();

  create<T>(id: string, value: T): ReactiveSignal<T> {
    if (this.signals.has(id)) {
      throw new Error(`Signal already exists: ${id}`);
    }
    const signal = new ReactiveSignal(value);
    this.signals.set(id, signal as ReactiveSignal<unknown>);
    return signal;
  }

  get<T>(id: string): ReactiveSignal<T> {
    const signal = this.signals.get(id);
    if (!signal) throw new Error(`Signal not found: ${id}`);
    return signal as ReactiveSignal<T>;
  }
}
