import test from 'node:test';
import assert from 'node:assert/strict';
import {createProceduralSplats} from '../src/studies/spark-splats.ts';

test('Spark: packing real preserva atributos dentro da quantização esperada', () => {
  const splats = createProceduralSplats();
  try {
    assert.equal(splats.numSplats, 192);
    const first = splats.getSplat(0);
    assert.ok(Math.abs(first.center.x - 1.3) < 0.002);
    assert.ok(Math.abs(first.scales.x - 0.08) < 0.005);
    assert.ok(Math.abs(first.opacity - 0.85) < 1 / 255);
    assert.ok(Math.abs(first.quaternion.length() - 1) < 0.01);
    for (let i = 0; i < 192; i++) {
      const s = splats.getSplat(i);
      assert.ok([...s.center, ...s.scales, ...s.quaternion, s.opacity, s.color.r, s.color.g, s.color.b].every(Number.isFinite));
    }
  } finally {splats.dispose();}
});

test('Spark: dados procedurais são reproduzíveis e rejeitam quantidades inválidas', () => {
  const a = createProceduralSplats(32), b = createProceduralSplats(32);
  try {
    // getSplat() reuses one scratch object: snapshot before the next call.
    const snapshot = (splats: typeof a) => Array.from({length: splats.numSplats}, (_, i) => {
      const s = splats.getSplat(i);
      return [...s.center, ...s.scales, ...s.quaternion, s.opacity, s.color.r, s.color.g, s.color.b];
    });
    assert.deepEqual(snapshot(a), snapshot(b));
    for (const n of [0, 15, 4097, 16.5, NaN, Infinity]) assert.throws(() => createProceduralSplats(n));
  } finally {a.dispose(); b.dispose();}
});
