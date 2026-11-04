import {test} from 'node:test';
import assert from 'node:assert/strict';
import {chartFrame} from '../src/studies/d3-layout.ts';
const data = Object.freeze([{id: 'a', label: 'A', value: 20}, {id: 'b', label: 'B', value: 40}].map((item) => Object.freeze(item)));
test('D3 preserva dados, alturas proporcionais e bandas sem sobreposição', () => {
  const end = chartFrame(data, 60, 30);
  assert.equal(end[0].height, 75); assert.equal(end[1].height, 150);
  assert.ok(end[0].x + end[0].width < end[1].x);
  assert.equal(data[0].value, 20);
  assert.equal(chartFrame(data, 24, 30)[1].height, 75);
});
test('D3 valida IDs e valores em vez de ocultar dados no join', () => {
  assert.throws(() => chartFrame([], 0, 30), /vazios/);
  assert.throws(() => chartFrame([data[0], data[0]], 0, 30), /duplicado/);
  assert.throws(() => chartFrame([{id: 'x', label: 'X', value: NaN}], 0, 30), /inválido/);
  assert.throws(() => chartFrame([{id: 'x', label: 'X', value: -1}], 0, 30), /inválido/);
  assert.ok(chartFrame([{id: 'x', label: 'X', value: 0}], 30, 30).every((d) => Number.isFinite(d.height)));
});
test('D3 amostra 90 frames em ordem embaralhada sem depender do histórico', () => {
  const expected = Array.from({length: 90}, (_, frame) => chartFrame(data, frame, 30));
  for (let i = 0; i < 90; i++) {const frame = i * 37 % 90; assert.deepEqual(chartFrame(data, frame, 30), expected[frame]);}
});
