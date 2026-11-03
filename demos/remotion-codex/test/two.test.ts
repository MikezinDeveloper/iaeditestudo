import {test} from 'node:test';
import assert from 'node:assert/strict';
import Two from 'two.js';
test('Two preserva vetores normalizados e rotação em radianos', () => {
  const vector = new Two.Vector(3, 4);
  assert.equal(vector.length(), 5);
  vector.normalize();
  assert.ok(Math.abs(vector.length() - 1) < 1e-12);
  const shape = new Two.Group();
  shape.rotation = Math.PI / 2;
  assert.equal(shape.rotation, Math.PI / 2);
});
test('Two transfere a propriedade de filhos sem duplicar o grafo', () => {
  const a = new Two.Group(), b = new Two.Group(), child = new Two.Group();
  a.add(child); b.add(child);
  assert.equal(a.children.length, 0);
  assert.equal(b.children.length, 1);
  assert.equal(b.children[0], child);
});
