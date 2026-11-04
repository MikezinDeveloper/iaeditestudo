import test from 'node:test';
import assert from 'node:assert/strict';
import {Vector3} from 'three';
import {createThreeScene} from '../src/studies/three-scene.ts';

test('Three: geometria finita, câmera enquadra o objeto e recursos emitem dispose', () => {
  const model = createThreeScene(0);
  const positions = model.mesh.geometry.getAttribute('position');
  assert.equal(positions.count, 73 * 13);
  assert.ok(Array.from(positions.array).every(Number.isFinite));
  const projected = new Vector3().project(model.camera);
  assert.ok(Math.abs(projected.x) < 1 && Math.abs(projected.y) < 1 && projected.z > -1 && projected.z < 1);
  let released = 0;
  model.mesh.geometry.addEventListener('dispose', () => released++);
  model.mesh.material.addEventListener('dispose', () => released++);
  model.dispose();
  assert.equal(released, 2);
  assert.equal(model.scene.children.length, 0);
});

test('Three: matrizes independem da ordem temporal e entrada inválida é rejeitada', () => {
  const sample = (ms: number) => {const m = createThreeScene(ms); const values = [...m.mesh.matrixWorld.elements]; m.dispose(); return values;};
  const expected = Array.from({length: 90}, (_, i) => sample(i * 1000 / 30));
  for (let i = 89; i >= 0; i--) assert.deepEqual(sample(i * 1000 / 30), expected[i]);
  assert.notDeepEqual(expected[0], expected[30]);
  for (const ms of [-1, NaN, Infinity]) assert.throws(() => createThreeScene(ms));
});
