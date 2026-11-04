import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {clothFrameAt, validateClothCache} from '../src/studies/cloth-cache.ts';

const fixture = () => JSON.parse(readFileSync(new URL('../src/studies/taichi-cloth.json', import.meta.url), 'utf8'));

test('Taichi: cache físico preserva âncoras, movimento e busca fora de ordem', () => {
  const provenance = JSON.parse(readFileSync(new URL('../../../estudo/taichi/resultados/simulation.json', import.meta.url), 'utf8'));
  const sha = (path: string) => createHash('sha256').update(readFileSync(new URL(path, import.meta.url))).digest('hex');
  assert.equal(sha('../src/studies/taichi-cloth.json'), provenance.cacheSha256);
  assert.equal(sha('../../../simulations/taichi/bake_cloth.py'), provenance.generatorSha256);
  const cache = validateClothCache(fixture());
  assert.equal(cache.frames.length, 90); assert.equal(cache.rows * cache.columns, 120);
  for (let i = 89; i >= 0; i--) assert.deepEqual(clothFrameAt(cache, i * 1000 / 30), cache.frames[i]);
  assert.notDeepEqual(cache.frames[0], cache.frames[30]);
  for (const frame of cache.frames) for (const id of cache.anchors) assert.deepEqual(frame[id], cache.frames[0][id]);
  assert.equal(clothFrameAt(cache, 100000), cache.frames[89]);
});

test('Taichi: rejeita cache corrompido e tempos inválidos antes de desenhar', () => {
  const cache = validateClothCache(fixture());
  for (const time of [-1, NaN, Infinity]) assert.throws(() => clothFrameAt(cache, time));
  const bad = fixture(); bad.frames[1][0][0] += 0.1; assert.throws(() => validateClothCache(bad));
  const invalid = fixture(); invalid.frames[0][3][0] = NaN; assert.throws(() => validateClothCache(invalid));
  assert.throws(() => validateClothCache({...fixture(), fps: 0}));
  assert.throws(() => validateClothCache({...fixture(), anchors: [0, 0]}));
});
