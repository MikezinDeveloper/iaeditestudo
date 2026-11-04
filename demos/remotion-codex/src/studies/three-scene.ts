import {Scene, Color, PerspectiveCamera, TorusKnotGeometry, MeshStandardMaterial, Mesh, HemisphereLight, DirectionalLight} from 'three';

export const createThreeScene = (timeMs: number) => {
  if (!Number.isFinite(timeMs) || timeMs < 0) throw new Error('Tempo 3D inválido');
  const scene = new Scene();
  scene.background = new Color('#101923');
  const camera = new PerspectiveCamera(40, 640 / 360, 0.1, 100);
  camera.position.set(0, 0, 7);
  const geometry = new TorusKnotGeometry(0.85, 0.24, 72, 12);
  const material = new MeshStandardMaterial({color: '#62f4c6', roughness: 0.35, metalness: 0.25});
  const mesh = new Mesh(geometry, material);
  const t = timeMs / 1000;
  mesh.rotation.set(t * 0.5, t * 0.9, 0.15);
  mesh.position.x = Math.sin(t * 1.8) * 0.6;
  scene.add(mesh, new HemisphereLight(0xe5f5ff, 0x303040, 2));
  const light = new DirectionalLight(0xffffff, 3);
  light.position.set(3, 4, 5);
  scene.add(light);
  scene.updateMatrixWorld(true);
  camera.updateMatrixWorld(true);
  return {scene, camera, mesh, dispose: () => {geometry.dispose(); material.dispose(); scene.clear();}};
};
