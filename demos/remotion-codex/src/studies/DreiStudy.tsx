import React from 'react';
import {BrowserStudy, type StudyMount} from './BrowserStudy';
import {DreiScene} from './drei-scene';

const mount: StudyMount = async (host, timeMs) => {
  const {createRoot, extend, advance} = await import('@react-three/fiber');
  const {Group, Mesh, ExtrudeGeometry, MeshStandardMaterial, HemisphereLight, DirectionalLight, Color} = await import('three');
  extend({Group, Mesh, ExtrudeGeometry, MeshStandardMaterial, HemisphereLight, DirectionalLight});
  const canvas = document.createElement('canvas');
  canvas.width = 640; canvas.height = 360;
  host.appendChild(canvas);
  const root = createRoot(canvas);
  const cleanup = () => {root.unmount(); canvas.remove();};
  let timer: ReturnType<typeof setTimeout> | undefined;
  try {
    await root.configure({frameloop: 'never', dpr: 1, size: {width: 640, height: 360, top: 0, left: 0}, camera: {fov: 40, position: [0, 0, 6]}, scene: {background: new Color('#101923')}, gl: {antialias: true, preserveDrawingBuffer: true}});
    let markReady!: () => void;
    const ready = new Promise<void>((resolve, reject) => {markReady = resolve; timer = setTimeout(() => reject(new Error('Cena Drei não montou')), 10000);});
    const store = root.render(<DreiScene timeMs={timeMs} onReady={markReady} />);
    await ready;
    advance(timeMs / 1000, false, store.getState());
    return cleanup;
  } catch (error) {cleanup(); throw error;}
  finally {clearTimeout(timer);}
};
export const DreiStudy: React.FC = () => <BrowserStudy name="DREI · ROUNDED BOX E CENTRALIZAÇÃO" mount={mount} />;
