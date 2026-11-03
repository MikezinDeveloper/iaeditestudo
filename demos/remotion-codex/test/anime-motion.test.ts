import {test} from 'node:test';
import assert from 'node:assert/strict';
import {engine, createTimeline} from 'animejs';
import {createAnimeMotionSampler, frameToMilliseconds, sampleAnimeMotion} from '../src/anime-motion.ts';

test('converte frames em milissegundos com fps inteiro e fracionário', () => {
  assert.equal(frameToMilliseconds(30, 30), 1000);
  assert.equal(frameToMilliseconds(18, 60), 300);
  assert.equal(frameToMilliseconds(30, 30000 / 1001), 1001);
  assert.equal(frameToMilliseconds(-1, 30), 0);
});
test('rejeita relógios inválidos antes de criar uma timeline', () => {
  assert.throws(() => sampleAnimeMotion(1.5, 30), /inteiro/);
  for (const fps of [0, -1, NaN, Infinity]) assert.throws(() => sampleAnimeMotion(0, fps), /fps/);
});
test('amostra numérica conhecida: outCubic a 300 ms', () => {
  const state = sampleAnimeMotion(9, 30);
  assert.equal(state.title.opacity, 0.875);
  assert.equal(state.title.y, 6.25);
});
test('stagger parte do centro e os extremos iniciam depois', () => {
  const state = sampleAnimeMotion(10, 30);
  assert.ok(state.bars[3].opacity > 0);
  assert.equal(state.bars[0].opacity, 0);
  assert.equal(state.bars[6].opacity, 0);
});
test('seek fora de ordem equivale a uma instância nova nos 120 quadros', () => {
  const sampler = createAnimeMotionSampler();
  try {
    const order = Array.from({length: 120}, (_, i) => i * 37 % 120);
    for (const frame of [...order, 119, 0, 90, 9, 0]) {
      assert.deepEqual(sampler.sample(frameToMilliseconds(frame, 30)), sampleAnimeMotion(frame, 30), `frame ${frame}`);
    }
  } finally { sampler.dispose(); }
});
test('animação não agenda o motor autônomo e a saída não retém o target', () => {
  const before = engine.reqId;
  const first = sampleAnimeMotion(9, 30);
  first.title.y = 999;
  assert.equal(sampleAnimeMotion(9, 30).title.y, 6.25);
  assert.equal(engine.reqId, before);
});
test('descarte é idempotente e impede novo uso', () => {
  const sampler = createAnimeMotionSampler();
  sampler.dispose(); sampler.dispose();
  assert.throws(() => sampler.sample(300), /descartado/);
});
test('seek com callbacks silenciados modifica o target sem emitir eventos', () => {
  let callbacks = 0;
  const target = {x: 0};
  const timeline = createTimeline({autoplay: false, onUpdate: () => callbacks++})
    .add(target, {x: [0, 100], duration: 1000, ease: 'linear'}, 0);
  timeline.seek(500, true);
  assert.equal(target.x, 50);
  assert.equal(callbacks, 0);
  timeline.cancel();
});
