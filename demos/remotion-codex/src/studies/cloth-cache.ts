export type ClothCache = {schemaVersion: 1; engine: 'taichi'; engineVersion: string; backend: string; fps: number; rows: number; columns: number; anchors: number[]; frames: [number, number][][]};

export const validateClothCache = (input: unknown): ClothCache => {
  const x = input as ClothCache;
  if (!x || x.schemaVersion !== 1 || x.engine !== 'taichi' || typeof x.engineVersion !== 'string' || typeof x.backend !== 'string' || !Number.isFinite(x.fps) || x.fps <= 0 || x.fps > 120 || !Number.isInteger(x.rows) || !Number.isInteger(x.columns) || x.rows < 2 || x.columns < 2 || x.rows * x.columns > 4096 || !Array.isArray(x.anchors) || x.anchors.length !== 2 || new Set(x.anchors).size !== 2 || x.anchors.some((i) => !Number.isInteger(i) || i < 0 || i >= x.rows * x.columns) || !Array.isArray(x.frames) || x.frames.length < 2 || x.frames.length > 900) throw new Error('Metadados do cache de tecido inválidos');
  for (const frame of x.frames) {
    if (!Array.isArray(frame) || frame.length !== x.rows * x.columns || frame.some((p) => !Array.isArray(p) || p.length !== 2 || p.some((v) => !Number.isFinite(v)))) throw new Error('Posições do cache inválidas');
    for (const id of x.anchors) for (let axis = 0; axis < 2; axis++) if (Math.abs(frame[id][axis] - x.frames[0][id][axis]) > 1e-5) throw new Error('Âncora do tecido se moveu');
  }
  return x;
};

export const clothFrameAt = (cache: ClothCache, timeMs: number) => {
  if (!Number.isFinite(timeMs) || timeMs < 0) throw new Error('Tempo de cache inválido');
  const index = Math.min(cache.frames.length - 1, Math.round(timeMs * cache.fps / 1000));
  return cache.frames[index];
};
