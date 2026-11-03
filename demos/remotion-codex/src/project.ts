export type Project = {
  title: string;
  accent: string;
  width: number;
  height: number;
  fps: number;
  durationInFrames: number;
  clips: {source: string; from: number; durationInFrames: number; trimBefore: number}[];
  audio: {source: string; volume: number; fadeFrames: number};
};

// This prototype deliberately accepts one contiguous video track and one audio bed.
// This is our experiment's contract, not Remotion's native project format.
export const validateProject = (input: unknown): Project => {
  if (!input || typeof input !== 'object') throw new Error('Projeto deve ser um objeto');
  const p = input as Project;
  const integer = (value: number, name: string, min = 0) => {
    if (!Number.isSafeInteger(value) || value < min) throw new Error(`${name}: inteiro >= ${min} esperado`);
  };
  if (typeof p.title !== 'string' || !p.title.trim()) throw new Error('title obrigatório');
  if (typeof p.accent !== 'string' || !/^#[0-9a-f]{6}$/i.test(p.accent)) throw new Error('accent deve ser #RRGGBB');
  for (const key of ['width', 'height', 'fps', 'durationInFrames'] as const) integer(p[key], key, 1);
  if (p.width % 2 || p.height % 2) throw new Error('Dimensões pares para H.264 yuv420p');
  if (!Array.isArray(p.clips) || !p.clips.length) throw new Error('clips obrigatório');
  const asset = (source: string, pattern: RegExp) => {
    if (typeof source !== 'string' || !pattern.test(source)) throw new Error('Asset deve ser um nome local permitido, sem caminhos ou URLs');
  };
  let end = 0;
  for (const clip of p.clips) {
    if (!clip || typeof clip !== 'object') throw new Error('Clipe inválido');
    asset(clip.source, /^[a-zA-Z0-9][a-zA-Z0-9._-]*\.(mp4|webm|mov)$/);
    integer(clip.from, 'from');
    integer(clip.durationInFrames, 'clip.durationInFrames', 1);
    integer(clip.trimBefore, 'trimBefore');
    if (clip.from !== end) throw new Error('Clipes devem ser contíguos, sem gaps ou sobreposições neste protótipo');
    end += clip.durationInFrames;
  }
  if (end !== p.durationInFrames) throw new Error('Duração dos clipes difere da composição');
  if (!p.audio || typeof p.audio !== 'object') throw new Error('audio obrigatório');
  asset(p.audio.source, /^[a-zA-Z0-9][a-zA-Z0-9._-]*\.(wav|mp3|aac)$/);
  if (!Number.isFinite(p.audio.volume) || p.audio.volume < 0 || p.audio.volume > 1) throw new Error('volume deve estar entre 0 e 1');
  integer(p.audio.fadeFrames, 'fadeFrames', 1);
  if (2 * p.audio.fadeFrames >= p.durationInFrames) throw new Error('Fades devem deixar um trecho de volume constante');
  return p;
};
