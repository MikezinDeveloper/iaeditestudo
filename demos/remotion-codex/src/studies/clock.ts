export const progressFromMilliseconds = (timeMs: number, durationMs: number): number => {
  if (!Number.isFinite(timeMs)) throw new Error('Tempo inválido');
  if (!Number.isFinite(durationMs) || durationMs <= 0) throw new Error('Duração inválida');
  return Math.max(0, Math.min(1, timeMs / durationMs));
};

export const progressAt = (frame: number, fps: number, durationMs: number): number => {
  if (!Number.isSafeInteger(frame)) throw new Error('Frame deve ser inteiro');
  if (!Number.isFinite(fps) || fps <= 0) throw new Error('FPS inválido');
  return progressFromMilliseconds(frame * 1000 / fps, durationMs);
};
