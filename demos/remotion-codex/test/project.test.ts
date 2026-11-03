import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {validateProject} from '../src/project.ts';

const project = () => JSON.parse(readFileSync(new URL('../project.json', import.meta.url), 'utf8'));
test('aceita a edição de referência: dois cortes cobrindo 180 quadros', () => {
  assert.equal(validateProject(project()).clips.length, 2);
});
test('rejeita gap e sobreposição em vez de produzir um corte ambíguo', () => {
  for (const start of [89, 91]) {
    const p = project(); p.clips[1].from = start;
    assert.throws(() => validateProject(p), /contíguos/);
  }
});
test('rejeita divergência entre a duração dos clipes e a composição', () => {
  const p = project(); p.durationInFrames = 181;
  assert.throws(() => validateProject(p), /Duração/);
});
test('rejeita referência fora do diretório de assets', () => {
  const p = project(); p.clips[0].source = '../private.mp4';
  assert.throws(() => validateProject(p), /Asset/);
});
test('rejeita fade sobreposto e volume fora do contrato', () => {
  const p = project(); p.audio.fadeFrames = 100;
  assert.throws(() => validateProject(p), /Fades/);
  p.audio.fadeFrames = 15; p.audio.volume = 2;
  assert.throws(() => validateProject(p), /volume/);
});
test('rejeita dimensões incompatíveis com a saída H.264 escolhida', () => {
  const p = project(); p.width = 641;
  assert.throws(() => validateProject(p), /Dimensões pares/);
});
