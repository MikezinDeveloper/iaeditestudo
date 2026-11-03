import {test} from 'node:test';
import assert from 'node:assert/strict';
import {progressAt} from '../src/studies/clock.ts';
test('progresso usa tempo da composição, com clamp e fps fracionário', () => {
  assert.equal(progressAt(36, 30, 2400), 0.5);
  assert.equal(progressAt(-1, 30, 2400), 0);
  assert.equal(progressAt(180, 30, 2400), 1);
  assert.equal(progressAt(30, 30000 / 1001, 1001), 1);
});
test('relógio dos estudos rejeita entradas inválidas', () => {
  assert.throws(() => progressAt(0.5, 30, 2400), /inteiro/);
  assert.throws(() => progressAt(0, 0, 2400), /FPS/);
  assert.throws(() => progressAt(0, 30, Infinity), /Duração/);
});
