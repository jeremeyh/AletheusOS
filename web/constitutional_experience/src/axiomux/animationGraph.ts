export interface AnimationState {
  value: number;
  velocity: number;
  target: number;
}

export class AnimationGraph {
  step(state: AnimationState, dt: number, stiffness = 180, dampingRatio = 1): AnimationState {
    const bounded = Math.max(0, Math.min(dt, 0.032));
    const mass = 1;
    const damping = 2 * dampingRatio * Math.sqrt(stiffness * mass);
    let { value, velocity, target } = state;
    for (let i = 0; i < 4; i++) {
      const h = bounded / 4;
      const force = -stiffness * (value - target) - damping * velocity;
      velocity += (force / mass) * h;
      value += velocity * h;
    }
    return { value, velocity, target };
  }
}
