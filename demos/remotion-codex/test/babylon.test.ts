import test from 'node:test';
import assert from 'node:assert/strict';
import {NullEngine} from '@babylonjs/core/Engines/nullEngine.js';
import {createBabylonScene} from '../src/studies/babylon-scene.ts';

test('Babylon: keyframes nativos pausados preservam 90 seeks em ordem reversa', () => {
  const engine = new NullEngine();
  const model = createBabylonScene(engine);
  try {
    assert.equal(model.mesh.getTotalVertices(), 24);
    assert.equal(model.group.isPlaying, false);
    model.seek(1000);
    assert.ok(Math.abs(model.mesh.rotation.y - 2 * Math.PI / 3) < 1e-6);
    const baseline = Array.from({length: 90}, (_, i) => {model.seek(i * 1000 / 30); return model.mesh.getWorldMatrix().asArray().slice();});
    for (let i = 89; i >= 0; i--) {model.seek(i * 1000 / 30); assert.deepEqual(model.mesh.getWorldMatrix().asArray(), baseline[i]);}
  } finally {model.dispose(); engine.dispose();}
});

test('Babylon: contrato temporal, clamp e descarte da cena', () => {
  const engine = new NullEngine();
  const model = createBabylonScene(engine);
  for (const ms of [-1, NaN, Infinity]) assert.throws(() => model.seek(ms));
  model.seek(9999); assert.ok(Math.abs(model.mesh.rotation.y - 2 * Math.PI) < 1e-6);
  let disposed = 0; model.scene.onDisposeObservable.add(() => disposed++);
  model.dispose(); model.dispose();
  assert.equal(disposed, 1); assert.equal(model.scene.isDisposed, true);
  assert.throws(() => model.seek(0));
  engine.dispose();
});
