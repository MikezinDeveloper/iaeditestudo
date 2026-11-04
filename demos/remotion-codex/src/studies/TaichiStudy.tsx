import React from 'react';
import {BrowserStudy, type StudyMount} from './BrowserStudy';
import {clothFrameAt, validateClothCache} from './cloth-cache';
import data from './taichi-cloth.json';

const cache = validateClothCache(data);
const mount: StudyMount = (host, timeMs) => {
  const points = clothFrameAt(cache, timeMs);
  const canvas = document.createElement('canvas'); canvas.width = 640; canvas.height = 360;
  const ctx = canvas.getContext('2d')!;
  ctx.fillStyle = '#101923'; ctx.fillRect(0, 0, 640, 360);
  const xy = (index: number) => [80 + points[index][0] * 480, 320 - points[index][1] * 280];
  for (let row = 0; row < cache.rows - 1; row++) for (let col = 0; col < cache.columns - 1; col++) {
    const i = row * cache.columns + col;
    ctx.beginPath();
    for (const [k, id] of [i, i + 1, i + cache.columns + 1, i + cache.columns].entries()) {
      const [x, y] = xy(id); if (k === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.closePath(); ctx.fillStyle = `hsl(${158 + row * 9 + col * 2} 65% ${45 + row * 2}%)`; ctx.fill();
    ctx.strokeStyle = '#192c3d'; ctx.lineWidth = 1; ctx.stroke();
  }
  ctx.fillStyle = '#eaf5fc';
  for (const i of cache.anchors) {const [x, y] = xy(i); ctx.beginPath(); ctx.arc(x, y, 5, 0, 2 * Math.PI); ctx.fill();}
  ctx.strokeStyle = '#45546a'; ctx.beginPath(); ctx.moveTo(70, 300); ctx.lineTo(570, 300); ctx.stroke();
  host.appendChild(canvas);
  return () => canvas.remove();
};
export const TaichiStudy: React.FC = () => <BrowserStudy name="TAICHI · TECIDO, MOLAS E GRAVIDADE" mount={mount} />;
