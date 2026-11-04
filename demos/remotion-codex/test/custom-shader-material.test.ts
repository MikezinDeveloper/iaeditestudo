import test from 'node:test';
import assert from 'node:assert/strict';
import {ShaderLib, UniformsUtils, type WebGLRenderer} from 'three';
import {createStudyMaterial} from '../src/studies/csm-material.ts';

test('CSM: material padrão, uniforms temporais e chave de programa estável', () => {
  const a = createStudyMaterial(0), b = createStudyMaterial(1000);
  try {
    assert.equal(a.type, 'MeshStandardMaterial');
    assert.equal(a.uniforms.uTime.value, 0); assert.equal(b.uniforms.uTime.value, 1);
    assert.equal(a.customProgramCacheKey(), b.customProgramCacheKey());
    for (const ms of [-1, NaN, Infinity]) assert.throws(() => createStudyMaterial(ms));
  } finally {a.dispose(); b.dispose();}
});

test('CSM: extensão preserva etapas de luz e conecta uniforms ao shader real Three', () => {
  const material = createStudyMaterial(1000);
  try {
    const shader = {vertexShader: ShaderLib.standard.vertexShader, fragmentShader: ShaderLib.standard.fragmentShader, uniforms: UniformsUtils.clone(ShaderLib.standard.uniforms)};
    // Minimal compile-hook fixture. Actual GL compilation is checked by export.
    material.onBeforeCompile(shader as Parameters<typeof material.onBeforeCompile>[0], {} as WebGLRenderer);
    assert.ok(shader.vertexShader.includes('csm_Position'));
    assert.ok(shader.fragmentShader.includes('#include <lights_fragment_begin>'));
    assert.ok(shader.fragmentShader.includes('csm_DiffuseColor'));
    assert.equal(shader.uniforms.uTime, material.uniforms.uTime);
    material.uniforms.uTime.value = 2; assert.equal(shader.uniforms.uTime.value, 2);
  } finally {material.dispose();}
});
