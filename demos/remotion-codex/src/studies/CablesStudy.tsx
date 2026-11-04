import React from 'react';
import {staticFile} from 'remotion';
import {BrowserStudy, type StudyMount} from './BrowserStudy';
import data from './cables-patch.json';
import {createCablesSampler, type CablesRuntime} from './cables-bridge';

let loading: Promise<CablesRuntime> | undefined;
const runtime = () => loading ??= new Promise((resolve, reject) => {
  const script = document.createElement('script');
  script.src = staticFile('vendor/cables/runtime.js');
  script.onload = () => resolve((globalThis as typeof globalThis & {CABLES: CablesRuntime}).CABLES);
  script.onerror = () => {loading = undefined; script.remove(); reject(new Error('Falha ao carregar Cables'));};
  document.head.appendChild(script);
});

const mount: StudyMount = async (host, timeMs) => {
  const sampler = createCablesSampler(await runtime(), data);
  try {
    const x = 320 + sampler.sample(timeMs);
    const canvas = document.createElement('canvas'); canvas.width = 640; canvas.height = 360;
    const ctx = canvas.getContext('2d')!;
    ctx.fillStyle = '#101923'; ctx.fillRect(0, 0, 640, 360);
    ctx.strokeStyle = '#62f4c6'; ctx.lineWidth = 5;
    ctx.beginPath(); ctx.arc(x, 155, 42, 0, Math.PI * 2); ctx.stroke();
    ctx.fillStyle = '#ad9bff'; ctx.fillRect(x - 18, 137, 36, 36);
    const labels = ['FRAME / FPS', 'SINE × 2', 'MULTIPLY × 100'];
    ctx.font = '13px DejaVu Sans';
    for (let i = 0; i < 3; i++) {
      const left = 50 + i * 185;
      ctx.strokeStyle = '#596c83'; ctx.strokeRect(left, 260, 170, 42);
      ctx.fillStyle = '#eaf5fc'; ctx.fillText(labels[i], left + 10, 286);
      if (i < 2) {ctx.beginPath(); ctx.moveTo(left + 170, 281); ctx.lineTo(left + 185, 281); ctx.stroke();}
    }
    host.appendChild(canvas);
    return () => {sampler.dispose(); canvas.remove();};
  } catch (error) {sampler.dispose(); throw error;}
};
export const CablesStudy: React.FC = () => <BrowserStudy name="CABLES · PATCH JSON E FLUXO DE DADOS" mount={mount} />;
