import React from 'react';
import {BrowserStudy, type StudyMount} from './BrowserStudy';

const mount: StudyMount = async (host, timeMs) => {
  const {WebGLRenderer, Scene, PerspectiveCamera, Color} = await import('three');
  const {SparkRenderer, SplatMesh} = await import('@sparkjsdev/spark');
  const {createProceduralSplats} = await import('./spark-splats');
  const renderer = new WebGLRenderer({antialias: false, preserveDrawingBuffer: true});
  renderer.setPixelRatio(1); renderer.setSize(640, 360);
  host.appendChild(renderer.domElement);
  const scene = new Scene(); scene.background = new Color('#101923');
  const camera = new PerspectiveCamera(40, 640 / 360, 0.1, 100);
  camera.position.z = 6;
  const spark = new SparkRenderer({renderer, autoUpdate: false, enableLod: false, minSortIntervalMs: 0});
  const mesh = new SplatMesh({packedSplats: createProceduralSplats()});
  mesh.rotation.set(0.2, timeMs / 1000 * 0.8, -0.15);
  scene.add(spark, mesh);
  const cleanup = () => {spark.dispose(); mesh.dispose(); scene.clear(); renderer.dispose(); renderer.forceContextLoss(); renderer.domElement.remove();};
  try {
    await mesh.initialized;
    scene.updateMatrixWorld(true); camera.updateMatrixWorld(true);
    await spark.update({scene, camera});
    if (spark.sorting || spark.sortDirty || spark.activeSplats === 0) throw new Error('Ordenação dos splats não concluiu');
    renderer.render(scene, camera);
    return cleanup;
  } catch (error) {cleanup(); throw error;}
};
export const SparkStudy: React.FC = () => <BrowserStudy name="SPARK · GAUSSIAN SPLATS PROCEDURAIS" mount={mount} />;
