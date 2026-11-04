export type FluidCache = {schemaVersion: 1; engine: 'SPlisHSPlasH'; engineVersion: string; solver: 'DFSPH'; backend: string; fps: number; particleRadius: number; bounds: [number, number, number, number]; frames: [number, number][][]; times: number[]; metrics: {particles: number; initialMass: number; finalMass: number}};

export const validateFluidCache = (input: unknown): FluidCache => {
  const x = input as FluidCache;
  if (!x || x.schemaVersion !== 1 || x.engine !== 'SPlisHSPlasH' || x.solver !== 'DFSPH' || typeof x.engineVersion !== 'string' || typeof x.backend !== 'string' || !Number.isFinite(x.fps) || x.fps <= 0 || x.fps > 120 || !Number.isFinite(x.particleRadius) || x.particleRadius <= 0 || !Array.isArray(x.bounds) || x.bounds.length !== 4 || x.bounds.some((n) => !Number.isFinite(n)) || x.bounds[0] >= x.bounds[2] || x.bounds[1] >= x.bounds[3] || !x.metrics || !Number.isInteger(x.metrics.particles) || x.metrics.particles < 1 || x.metrics.particles > 100000 || !Number.isFinite(x.metrics.initialMass) || x.metrics.initialMass <= 0 || !Number.isFinite(x.metrics.finalMass) || Math.abs(x.metrics.initialMass - x.metrics.finalMass) > 1e-6 || !Array.isArray(x.frames) || x.frames.length < 2 || x.frames.length > 900 || !Array.isArray(x.times) || x.times.length !== x.frames.length) throw new Error('Metadados do cache de fluido inválidos');
  x.frames.forEach((frame, i) => {
    if (!Number.isFinite(x.times[i]) || Math.abs(x.times[i] - i / x.fps) > 1e-5 || !Array.isArray(frame) || frame.length !== x.metrics.particles || frame.some((p) => !Array.isArray(p) || p.length !== 2 || p.some((v) => !Number.isFinite(v)) || p[0] < x.bounds[0] - 2 * x.particleRadius || p[0] > x.bounds[2] + 2 * x.particleRadius || p[1] < x.bounds[1] - 2 * x.particleRadius || p[1] > x.bounds[3] + 2 * x.particleRadius)) throw new Error('Quadro de fluido inválido');
  });
  return x;
};

export const fluidFrameAt = (cache: FluidCache, timeMs: number) => {
  if (!Number.isFinite(timeMs) || timeMs < 0) throw new Error('Tempo de fluido inválido');
  return cache.frames[Math.min(cache.frames.length - 1, Math.round(timeMs * cache.fps / 1000))];
};
