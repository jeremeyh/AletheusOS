const HEADER_WORDS = 4;
const WRITE_INDEX = 0;
const READ_INDEX = 1;
const CAPACITY_INDEX = 2;
const STRIDE_INDEX = 3;

export class AtomicFloatRingBuffer {
  private readonly header: Int32Array;
  private readonly body: Float32Array;

  constructor(
    readonly buffer: SharedArrayBuffer,
    readonly capacity: number,
    readonly stride: number,
  ) {
    const headerBytes = HEADER_WORDS * Int32Array.BYTES_PER_ELEMENT;
    this.header = new Int32Array(buffer, 0, HEADER_WORDS);
    this.body = new Float32Array(buffer, headerBytes);
    Atomics.store(this.header, CAPACITY_INDEX, capacity);
    Atomics.store(this.header, STRIDE_INDEX, stride);
  }

  static create(capacity: number, stride: number): AtomicFloatRingBuffer {
    const headerBytes = HEADER_WORDS * Int32Array.BYTES_PER_ELEMENT;
    const bodyBytes =
      capacity * stride * Float32Array.BYTES_PER_ELEMENT;
    return new AtomicFloatRingBuffer(
      new SharedArrayBuffer(headerBytes + bodyBytes),
      capacity,
      stride,
    );
  }

  write(packet: readonly number[]): boolean {
    if (packet.length !== this.stride) {
      throw new Error(`Expected packet stride ${this.stride}`);
    }

    const write = Atomics.load(this.header, WRITE_INDEX);
    const read = Atomics.load(this.header, READ_INDEX);
    const next = (write + 1) % this.capacity;
    if (next === read) return false;

    const offset = write * this.stride;
    for (let index = 0; index < this.stride; index += 1) {
      this.body[offset + index] = packet[index] ?? 0;
    }

    Atomics.store(this.header, WRITE_INDEX, next);
    Atomics.notify(this.header, WRITE_INDEX, 1);
    return true;
  }

  read(): number[] | null {
    const write = Atomics.load(this.header, WRITE_INDEX);
    const read = Atomics.load(this.header, READ_INDEX);
    if (read === write) return null;

    const offset = read * this.stride;
    const packet = Array.from(
      this.body.subarray(offset, offset + this.stride),
    );
    Atomics.store(this.header, READ_INDEX, (read + 1) % this.capacity);
    return packet;
  }
}
