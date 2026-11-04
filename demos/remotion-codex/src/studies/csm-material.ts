import CustomShaderMaterial from 'three-custom-shader-material/vanilla';
import {MeshStandardMaterial, Color, DoubleSide} from 'three';

export const vertexShader = `
uniform float uTime;
varying vec2 vStudyUv;
void main() {
  vStudyUv = uv;
  float a = position.x * 3.0 + uTime * 2.0;
  float b = position.y * 4.0 - uTime;
  float height = 0.22 * sin(a) * cos(b);
  float dx = 0.66 * cos(a) * cos(b);
  float dy = -0.88 * sin(a) * sin(b);
  csm_Position = vec3(position.xy, height);
  csm_Normal = normalize(vec3(-dx, -dy, 1.0));
}`;

export const fragmentShader = `
uniform vec3 uColorA;
uniform vec3 uColorB;
varying vec2 vStudyUv;
void main() {
  csm_DiffuseColor = vec4(mix(uColorA, uColorB, vStudyUv.y), 1.0);
}`;

export const createStudyMaterial = (timeMs: number) => {
  if (!Number.isFinite(timeMs) || timeMs < 0) throw new Error('Tempo de shader inválido');
  return new CustomShaderMaterial({baseMaterial: MeshStandardMaterial, vertexShader, fragmentShader, uniforms: {uTime: {value: timeMs / 1000}, uColorA: {value: new Color('#ad9bff')}, uColorB: {value: new Color('#62f4c6')}}, roughness: 0.3, metalness: 0.2, side: DoubleSide});
};
