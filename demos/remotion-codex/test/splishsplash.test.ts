import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fluidFrameAt, validateFluidCache} from '../src/studies/fluid-cache.ts';

const fixture = () => JSON.parse(readFileSync(new URL('../src/studies/splish-fluid.json', import.meta.url), 'utf8'));

test('SPlisHSPlasH: cache nativo e receita correspondem; massa e seek são preservados', () => {
  const provenance = JSON.parse(readFileSync(new URL('../../../estudo/splishsplash/resultados/simulation.json', import.meta.url), 'utf8'));
  const sha = (path: string) => createHash('sha256').update(readFileSync(new URL(path, import.meta.url))).digest('hex');
  assert.equal(sha('../src/studies/splish-fluid.json'), provenance.cacheSha256);
  for (const [file, hash] of Object.entries(provenance.generatorHashes)) assert.equal(sha(`../../../simulations/splishsplash/${file}`), hash);
  const cache = validateFluidCache(fixture());
  assert.equal(cache.metrics.particles, 168); assert.equal(cache.frames.length, 90);
  assert.equal(cache.metrics.initialMass, cache.metrics.finalMass);
  for (let i = 89; i >= 0; i--) assert.deepEqual(fluidFrameAt(cache, i * 1000 / 30), cache.frames[i]);
  assert.notDeepEqual(cache.frames[0], cache.frames[30]);
});

test('SPlisHSPlasH: rejeita alteração de massa, tempo, contagem e números não finitos', () => {
  const cache = validateFluidCache(fixture());
  for (const ms of [-1, NaN, Infinity]) assert.throws(() => fluidFrameAt(cache, ms));
  assert.equal(fluidFrameAt(cache, 99999), cache.frames[89]);
  const mass = fixture(); mass.metrics.finalMass *= 0.5; assert.throws(() => validateFluidCache(mass));
  const time = fixture(); time.times[30] += 0.01; assert.throws(() => validateFluidCache(time));
  const count = fixture(); count.frames[3].pop(); assert.throws(() => validateFluidCache(count));
  const number = fixture(); number.frames[0][0][0] = Infinity; assert.throws(() => validateFluidCache(number));
});
