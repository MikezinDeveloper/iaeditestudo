import React from 'react';
import {BrowserStudy, type StudyMount} from './BrowserStudy';
import {createBabylonScene} from './babylon-scene';

const mount: StudyMount = async (host, timeMs) => {
  const {Engine} = await import('@babylonjs/core/Engines/engine.js');
  const canvas = document.createElement('canvas');
  canvas.width = 640; canvas.height = 360;
  host.appendChild(canvas);
  const engine = new Engine(canvas, true, {preserveDrawingBuffer: true, stencil: true}, false);
  engine.setHardwareScalingLevel(1);
  const model = createBabylonScene(engine);
  const loss = (canvas.getContext('webgl2') ?? canvas.getContext('webgl'))?.getExtension('WEBGL_lose_context');
  const cleanup = () => {model.dispose(); engine.dispose(); loss?.loseContext(); canvas.remove();};
  try {
    model.seek(timeMs);
    await model.scene.whenReadyAsync();
    model.scene.render(true, true);
    return cleanup;
  } catch (error) {cleanup(); throw error;}
};
export const BabylonStudy: React.FC = () => <BrowserStudy name="BABYLON.JS · KEYFRAMES EM UMA CENA 3D" mount={mount} />;
