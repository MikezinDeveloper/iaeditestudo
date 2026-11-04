import {easeCubicInOut, interpolateNumber, max, scaleBand, scaleLinear} from 'd3';
import {progressAt} from './clock.ts';
export type ChartDatum = {id: string; label: string; value: number};
export const chartFrame = (data: readonly ChartDatum[], frame: number, fps: number) => {
  if (!data.length) throw new Error('Dados vazios');
  const ids = new Set<string>();
  for (const item of data) {
    if (typeof item.id !== 'string' || !item.id || ids.has(item.id)) throw new Error('ID vazio ou duplicado');
    if (typeof item.label !== 'string' || !Number.isFinite(item.value) || item.value < 0) throw new Error('Valor ou rótulo inválido');
    ids.add(item.id);
  }
  const x = scaleBand<string>().domain(data.map((d) => d.id)).range([0, 480]).padding(0.2);
  const height = scaleLinear().domain([0, max(data, (d) => d.value) || 1]).range([0, 150]).clamp(true);
  const progress = easeCubicInOut(progressAt(frame, fps, 1600));
  return data.map((d) => {
    const value = interpolateNumber(0, d.value)(progress);
    return {...d, displayedValue: value, x: x(d.id)!, width: x.bandwidth(), height: height(value)};
  });
};
