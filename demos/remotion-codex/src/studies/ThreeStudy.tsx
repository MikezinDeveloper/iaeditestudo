import React from 'react';
import {BrowserStudy, type StudyMount} from './BrowserStudy';
import {createThreeScene} from './three-scene';

const mount: StudyMount = async (host, timeMs) => {
  const {WebGLRenderer} = await import('three');
  const renderer = new WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
  const model = createThreeScene(timeMs);
  const cleanup = () => {model.dispose(); renderer.dispose(); renderer.forceContextLoss(); renderer.domElement.remove();};
  try {
    renderer.setPixelRatio(1);
    renderer.setSize(640, 360);
    host.appendChild(renderer.domElement);
    renderer.render(model.scene, model.camera);
    return cleanup;
  } catch (error) {cleanup(); throw error;}
};
export const ThreeStudy: React.FC = () => <BrowserStudy name="THREE.JS · CÂMERA, MATERIAL E LUZ" mount={mount} />;
