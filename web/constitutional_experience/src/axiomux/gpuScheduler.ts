export type GPUJob = { id: string; priority: number; execute: () => Promise<void> };

export class GPUScheduler {
  private readonly queue: GPUJob[] = [];
  private running = false;

  enqueue(job: GPUJob): void {
    this.queue.push(job);
    this.queue.sort((a, b) => b.priority - a.priority || a.id.localeCompare(b.id));
  }

  async drain(maxJobs = 8): Promise<number> {
    if (this.running) return 0;
    this.running = true;
    let completed = 0;
    try {
      while (this.queue.length && completed < maxJobs) {
        const job = this.queue.shift();
        if (!job) break;
        await job.execute();
        completed += 1;
      }
      return completed;
    } finally {
      this.running = false;
    }
  }

  get depth(): number { return this.queue.length; }
}
