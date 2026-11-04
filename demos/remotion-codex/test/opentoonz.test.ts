import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {validateOca, ocaFrameAt} from '../src/studies/oca-exposure.ts';
const raw = () => JSON.parse(readFileSync(new URL('../public/opentoonz/walk.oca',import.meta.url),'utf8'));

test('OpenToonz/OCA: holds, mudança 24→30fps, blank, camadas e seek fora de ordem', () => {
  const input = raw(), before = JSON.stringify(input), scene = validateOca(input);
  const at = (frame: number) => ocaFrameAt(scene,frame*1000/30);
  assert.equal(at(0)[1].fileName,'walk_files/Cat.0001.png');
  assert.deepEqual(at(0),at(1)); assert.deepEqual(at(1),at(2));
  assert.equal(at(3)[1].fileName,'walk_files/Cat.0002.png');
  assert.deepEqual(at(58).map((c) => c.layer),['Ground']);
  assert.equal(at(60)[1].fileName,'walk_files/Cat.0001.png');
  assert.deepEqual(at(90),[]);
  const snapshots = Array.from({length:90},(_,f) => at(f));
  for (let f=89;f>=0;f--) assert.deepEqual(at(f),snapshots[f]);
  assert.equal(JSON.stringify(input),before);
  input.layers[1].reference = true;
  assert.equal(ocaFrameAt(validateOca(input),0).length,1);
  input.layers[1].reference = false; input.layers[1].visible = false;
  assert.equal(ocaFrameAt(validateOca(input),0).length,1);
  input.layers[1].visible = true; input.layers[1].opacity = 0.5;
  assert.equal(ocaFrameAt(validateOca(input),0)[1].opacity,0.5);
  assert.throws(() => ocaFrameAt(scene,NaN)); assert.throws(() => ocaFrameAt(scene,-1));
});

test('OpenToonz/OCA: rejeita recursos fora do contrato e verifica PNGs/receita versionados', () => {
  for (const mutate of [
    (s: any) => {s.layers[1].frames[1].frameNumber = 1;},
    (s: any) => {s.layers[1].frames[0].duration = 0;},
    (s: any) => {s.layers[1].frames[0].fileName = '../secret.png';},
    (s: any) => {s.layers[1].type = 'grouplayer';},
    (s: any) => {s.layers[1].position = [1,2];},
    (s: any) => {s.frameRate = 0;},
    (s: any) => {s.layers[1].frames[0].name = '_blank';},
  ]) {const s = raw(); mutate(s); assert.throws(() => validateOca(s));}
  const root = new URL('../../../',import.meta.url);
  const report = JSON.parse(readFileSync(new URL('estudo/opentoonz/resultados/fixture.json',root),'utf8'));
  const hash = (data: Buffer) => createHash('sha256').update(data).digest('hex');
  assert.equal(hash(readFileSync(new URL('simulations/opentoonz/generate_fixture.py',root))),report.scriptSha256);
  for (const [path,sha] of Object.entries(report.files as Record<string,string>)) {
    const bytes = readFileSync(new URL(path,root));
    assert.equal(hash(bytes),sha);
    if (path.endsWith('.png')) {
      assert.equal(bytes.subarray(0,8).toString('hex'),'89504e470d0a1a0a');
      assert.equal(bytes.readUInt32BE(16),640); assert.equal(bytes.readUInt32BE(20),360);
      assert.equal(bytes[24],8); assert.equal(bytes[25],6); // RGBA, U8
    }
  }
});
