import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createTheatreSampler} from '../src/studies/theatre-sampler.ts';
const state = JSON.parse(readFileSync(new URL('../src/studies/theatre-state.json', import.meta.url), 'utf8'));
test('Theatre restaura o estado JSON e avalia keyframes e interpolação conhecidos', async () => {
  const sampler = await createTheatreSampler(JSON.parse(JSON.stringify(state)));
  try {
    assert.equal(sampler.sample(0).x, -130);
    assert.ok(Math.abs(sampler.sample(.75).x) < 1e-6);
    assert.equal(sampler.sample(1.5).x, 130);
    assert.equal(sampler.sample(3).angle, 330);
  } finally {sampler.dispose();}
});
test('Theatre preserva todos os 90 frames em ordem embaralhada e após o fim', async () => {
  const sampler = await createTheatreSampler(state);
  try {
    const expected = Array.from({length: 90}, (_, frame) => sampler.sample(frame / 30));
    for (let i = 0; i < 90; i++) {
      const frame = i * 37 % 90;
      assert.deepEqual(sampler.sample(frame / 30), expected[frame]);
    }
    assert.deepEqual(sampler.sample(0), expected[0]);
  } finally {sampler.dispose();}
});
test('Theatre rejeita tempo inválido e uso após cleanup', async () => {
  const sampler = await createTheatreSampler(state);
  assert.throws(() => sampler.sample(NaN), /inválido/);
  sampler.dispose();sampler.dispose();
  assert.throws(() => sampler.sample(1), /descartado/);
});
