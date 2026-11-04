import React from 'react';
import {staticFile} from 'remotion';
import {BrowserStudy, type StudyMount} from './BrowserStudy';
import {ocaFrameAt, validateOca} from './oca-exposure';

let scenePromise: Promise<ReturnType<typeof validateOca>> | undefined;
const images = new Map<string, Promise<HTMLImageElement>>();
const image = (file: string) => {
  if (!images.has(file)) images.set(file, (async () => {
    const img = new Image(); img.src = staticFile(`opentoonz/${file}`); await img.decode(); return img;
  })().catch((error) => {images.delete(file); throw error;}));
  return images.get(file)!;
};
const mount: StudyMount = async (host, timeMs) => {
  scenePromise ??= fetch(staticFile('opentoonz/walk.oca')).then((r) => {if (!r.ok) throw new Error(`OCA HTTP ${r.status}`); return r.json();}).then(validateOca).catch((error) => {scenePromise = undefined; throw error;});
  const scene = await scenePromise;
  const canvas = document.createElement('canvas'); canvas.width = scene.width; canvas.height = scene.height;
  const ctx = canvas.getContext('2d')!;
  const [r,g,b,a] = scene.backgroundColor;
  ctx.fillStyle = `rgba(${r*255},${g*255},${b*255},${a})`; ctx.fillRect(0,0,scene.width,scene.height);
  const cels = ocaFrameAt(scene, timeMs);
  const decoded = await Promise.all(cels.map((cel) => image(cel.fileName)));
  cels.forEach((cel, i) => {
    const img = decoded[i];
    if (img.naturalWidth !== scene.width || img.naturalHeight !== scene.height) throw new Error('PNG diverge da dimensão OCA');
    ctx.globalAlpha = cel.opacity; ctx.drawImage(img,0,0);
  });
  ctx.globalAlpha = 1;
  host.appendChild(canvas);
  return () => canvas.remove();
};
export const OpenToonzStudy: React.FC = () => <BrowserStudy name="OPENTOONZ · OCA E EXPOSIÇÃO DE DESENHOS" mount={mount} />;
