import React, {useCallback} from 'react';
import {BrowserStudy, type StudyMount} from './BrowserStudy';
import {createStudyMaterial} from './csm-material';

export const CustomShaderMaterialStudy: React.FC<{lightIntensity?: number}> = ({lightIntensity = 3}) => {
  if (!Number.isFinite(lightIntensity) || lightIntensity < 0 || lightIntensity > 10) throw new Error('Intensidade de luz inválida');
  const mount = useCallback<StudyMount>(async (host, timeMs) => {
    const {WebGLRenderer, Scene, PerspectiveCamera, Color, Mesh, PlaneGeometry, HemisphereLight, DirectionalLight} = await import('three');
    const renderer = new WebGLRenderer({antialias: true, preserveDrawingBuffer: true});
    const material = createStudyMaterial(timeMs);
    const geometry = new PlaneGeometry(3, 1.7, 60, 34);
    const scene = new Scene(); scene.background = new Color('#101923');
    const camera = new PerspectiveCamera(40, 640 / 360, 0.1, 100); camera.position.z = 5;
    const mesh = new Mesh(geometry, material); mesh.rotation.set(0.2, -0.3, 0);
    const light = new DirectionalLight(0xffffff, lightIntensity); light.position.set(3, 4, 5);
    scene.add(mesh, light, new HemisphereLight(0xffffff, 0x303040, 1));
    const cleanup = () => {geometry.dispose(); material.dispose(); scene.clear(); renderer.dispose(); renderer.forceContextLoss(); renderer.domElement.remove();};
    try {
      renderer.setPixelRatio(1); renderer.setSize(640, 360); host.appendChild(renderer.domElement);
      // @types/three uses its internal wrapper here; the runtime passes a DOM GL program.
      renderer.debug.onShaderError = (gl, program) => {throw new Error(`Shader não compilou: ${gl.getProgramInfoLog(program as unknown as WebGLProgram)}`);};
      await renderer.compileAsync(scene, camera);
      renderer.render(scene, camera);
      return cleanup;
    } catch (error) {cleanup(); throw error;}
  }, [lightIntensity]);
  return <BrowserStudy name="CUSTOM SHADER MATERIAL · ONDA E ILUMINAÇÃO" mount={mount} />;
};
