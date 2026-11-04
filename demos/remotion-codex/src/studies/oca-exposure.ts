/** Flat PNG subset of OCA 1.1.0, derived from OpenToonz's inspected ocaio.cpp. */
export type OcaCel = {name: string; fileName: string; frameNumber: number; duration: number};
export type OcaLayer = {name: string; opacity: number; visible: boolean; reference: boolean; frames: OcaCel[]};
export type OcaScene = {width: number; height: number; frameRate: number; endTime: number; backgroundColor: number[]; layers: OcaLayer[]};
const object = (v: unknown): Record<string, unknown> => {
  if (!v || typeof v !== 'object' || Array.isArray(v)) throw new Error('Objeto OCA inválido');
  return v as Record<string, unknown>;
};
const integer = (v: unknown, min: number, max: number): number => {
  if (typeof v !== 'number' || !Number.isInteger(v) || v < min || v > max) throw new Error('Inteiro OCA inválido');
  return v;
};
const text = (v: unknown): string => {if (typeof v !== 'string' || !v) throw new Error('Nome OCA inválido'); return v;};
const opacity = (v: unknown): number => {if (typeof v !== 'number' || !Number.isFinite(v) || v < 0 || v > 1) throw new Error('Opacidade OCA inválida'); return v;};
const boolean = (v: unknown): boolean => {if (typeof v !== 'boolean') throw new Error('Flag OCA inválida'); return v;};
const centered = (v: unknown, width: number, height: number) => {
  if (!Array.isArray(v) || v.length !== 2 || v[0] !== width / 2 || v[1] !== height / 2) throw new Error('Posição OCA fora do subconjunto centralizado');
};
export const validateOca = (input: unknown): OcaScene => {
  const s = object(input);
  if (s.ocaVersion !== '1.1.0' || s.colorDepth !== 'U8' || s.startTime !== 0) throw new Error('Versão, cor ou início OCA não suportado');
  const width = integer(s.width, 1, 4096), height = integer(s.height, 1, 4096);
  const endTime = integer(s.endTime, 1, 100000);
  if (typeof s.frameRate !== 'number' || !Number.isFinite(s.frameRate) || s.frameRate <= 0 || s.frameRate > 240) throw new Error('FPS OCA inválido');
  if (!Array.isArray(s.backgroundColor) || s.backgroundColor.length !== 4) throw new Error('Fundo OCA inválido');
  const backgroundColor = s.backgroundColor.map(opacity);
  if (!Array.isArray(s.layers) || !s.layers.length || s.layers.length > 100) throw new Error('Camadas OCA inválidas');
  const layers = s.layers.map((raw) => {
    const l = object(raw);
    if (l.type !== 'paintlayer' || l.fileType !== 'png' || l.blendingMode !== 'normal' || l.passThrough !== false || l.inheritAlpha !== false || !Array.isArray(l.childLayers) || l.childLayers.length) throw new Error('Tipo, grupo ou blending OCA não suportado');
    centered(l.position, width, height);
    if (l.width !== width || l.height !== height || !Array.isArray(l.frames) || l.frames.length > 100000) throw new Error('Dimensão ou exposições OCA inválidas');
    let previousEnd = 0;
    const frames = l.frames.map((rawFrame) => {
      const f = object(rawFrame);
      const name = text(f.name), frameNumber = integer(f.frameNumber, 0, endTime - 1), duration = integer(f.duration, 1, endTime);
      if (frameNumber < previousEnd || frameNumber + duration > endTime) throw new Error('Exposição OCA sobreposta ou fora da cena');
      previousEnd = frameNumber + duration;
      centered(f.position, width, height);
      if (f.opacity !== 1 || typeof f.fileName !== 'string') throw new Error('Cel OCA não suportada');
      const fileName = f.fileName;
      if (name === '_blank' ? fileName !== '' : fileName === '') throw new Error('Cel vazia OCA inconsistente');
      if (fileName && (!/^[a-zA-Z0-9_./-]+\.png$/.test(fileName) || fileName.startsWith('/') || fileName.split('/').some((p) => !p || p === '.' || p === '..'))) throw new Error('Caminho PNG OCA inválido');
      if (f.width !== (fileName ? width : 0) || f.height !== (fileName ? height : 0)) throw new Error('Dimensão de cel OCA inválida');
      return {name, fileName, frameNumber, duration};
    });
    return {name: text(l.name), opacity: opacity(l.opacity), visible: boolean(l.visible), reference: boolean(l.reference), frames};
  });
  return {width, height, frameRate: s.frameRate, endTime, backgroundColor, layers};
};

export const ocaFrameAt = (scene: OcaScene, timeMs: number) => {
  if (!Number.isFinite(timeMs) || timeMs < 0) throw new Error('Tempo OCA inválido');
  // Numerical tolerance at rational FPS boundaries; holds use half-open intervals.
  const row = Math.floor(timeMs * scene.frameRate / 1000 + 1e-8);
  if (row >= scene.endTime) return [];
  return scene.layers.flatMap((layer) => {
    if (!layer.visible || layer.reference || layer.opacity === 0) return [];
    const cel = layer.frames.find((f) => row >= f.frameNumber && row < f.frameNumber + f.duration);
    return cel?.fileName ? [{layer: layer.name, fileName: cel.fileName, opacity: layer.opacity}] : [];
  });
};
