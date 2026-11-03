import {createTimeline, engine, stagger} from 'animejs';

export type AnimeMotionState = {
  title: {opacity: number; y: number};
  bars: {scale: number; opacity: number}[];
  line: {progress: number};
};

export const frameToMilliseconds = (frame: number, fps: number): number => {
  if (!Number.isSafeInteger(frame)) throw new Error('frame deve ser inteiro');
  if (!Number.isFinite(fps) || fps <= 0) throw new Error('fps deve ser finito e positivo');
  return Math.max(0, frame) * 1000 / fps;
};

// Anime mutates only these private numeric targets. React owns all DOM/SVG output.
// Explicit from/to values and a fresh factory make frame order irrelevant here.
export const createAnimeMotionSampler = () => {
  if (engine.timeUnit !== 'ms') throw new Error('Este adapter exige engine.timeUnit = ms; não altera a configuração global');
  let disposed = false;
  return {
    sample(milliseconds: number): AnimeMotionState {
      if (disposed) throw new Error('Sampler já descartado');
      if (!Number.isFinite(milliseconds)) throw new Error('Tempo deve ser finito');
      // A reused timeline with multiple tweens on the same property failed our
      // backwards-seek test. Rebuild private state for every requested time.
      const title = {opacity: 0, y: 50};
      const bars = Array.from({length: 7}, () => ({scale: 0, opacity: 0}));
      const line = {progress: 0};
      const timeline = createTimeline({autoplay: false})
        .label('enter', 0)
        .add(title, {opacity: [0, 1], y: [50, 0], duration: 600, ease: 'outCubic'}, 'enter')
        .add(bars, {scale: [0, 1], opacity: [0, 1], duration: 600, delay: stagger(80, {from: 'center'}), ease: 'outCubic'}, 250)
        .add(line, {progress: [0, 1], duration: 1200, ease: 'inOutCubic'}, 650)
        .label('exit', 3000)
        .add(title, {opacity: [1, 0], y: [0, -16], duration: 600, ease: 'inCubic'}, 'exit');
      try {
        timeline.seek(Math.max(0, milliseconds), true);
        return {title: {opacity: title.opacity, y: title.y}, bars: bars.map((bar) => ({scale: bar.scale, opacity: bar.opacity})), line: {progress: line.progress}};
      } finally {
        timeline.cancel();
      }
    },
    dispose() {
      disposed = true;
    },
  };
};

export const sampleAnimeMotion = (frame: number, fps: number): AnimeMotionState => {
  const milliseconds = frameToMilliseconds(frame, fps);
  const sampler = createAnimeMotionSampler();
  try {
    return sampler.sample(milliseconds);
  } finally {
    sampler.dispose();
  }
};
