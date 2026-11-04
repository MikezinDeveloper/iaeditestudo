import React from 'react';
import {BrowserStudy, type StudyMount} from './BrowserStudy';
import {fluidFrameAt, validateFluidCache} from './fluid-cache';
import data from './splish-fluid.json';

const cache = validateFluidCache(data);
const mount: StudyMount = (host, timeMs) => {
  const positions = fluidFrameAt(cache, timeMs);
  const canvas = document.createElement('canvas'); canvas.width = 640; canvas.height = 360;
  const ctx = canvas.getContext('2d')!;
  ctx.fillStyle = '#101923'; ctx.fillRect(0, 0, 640, 360);
  const [left, bottom, right, top] = cache.bounds;
  ctx.fillStyle = '#132332'; ctx.fillRect(320 + left * 150, 305 - top * 150, (right - left) * 150, (top - bottom) * 150);
  for (let i = 0; i < positions.length; i++) {
    const [x, y] = positions[i];
    ctx.fillStyle = `hsl(${180 + i / positions.length * 35} 85% 63%)`;
    ctx.beginPath(); ctx.arc(320 + x * 150, 305 - y * 150, cache.particleRadius * 150 * 1.08, 0, Math.PI * 2); ctx.fill();
  }
  ctx.strokeStyle = '#738aa2'; ctx.lineWidth = 2;
  ctx.strokeRect(320 + left * 150, 305 - top * 150, (right - left) * 150, (top - bottom) * 150);
  host.appendChild(canvas);
  return () => canvas.remove();
};
export const SplishsplashStudy: React.FC = () => <BrowserStudy name="SPLISHSPLASH · FLUIDO DFSPH" mount={mount} />;
