import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
import {createCablesSampler, type CablesRuntime} from '../src/studies/cables-bridge.ts';

const load = () => {
  const timers = new Set<ReturnType<typeof setTimeout>>();
  const window = Object.assign(new EventTarget(), {performance});
  const context = vm.createContext({window, performance, CustomEvent, structuredClone, console,
    setTimeout: (cb: () => void, ms: number) => {const id = setTimeout(() => {timers.delete(id); cb();}, ms); timers.add(id); return id;},
    setInterval: (cb: () => void, ms: number) => {const id = setInterval(cb, ms); timers.add(id); return id;},
    clearTimeout, clearInterval, document: {}, navigator: {userAgent: 'Node test'},
  });
  vm.runInContext(readFileSync(new URL('../public/vendor/cables/runtime.js', import.meta.url), 'utf8'), context);
  return {runtime: context.CABLES as CablesRuntime, cleanup: () => {for (const id of timers) {clearTimeout(id); clearInterval(id);}}};
};
const fixture = () => JSON.parse(readFileSync(new URL('../src/studies/cables-patch.json', import.meta.url), 'utf8'));

test('Cables: JSON e links originais avaliam valores conhecidos sem mutar os dados', () => {
  const {runtime, cleanup} = load(); const data = fixture(); const before = JSON.stringify(data);
  const sampler = createCablesSampler(runtime, data);
  try {
    assert.equal(sampler.sample(0), 0);
    assert.ok(Math.abs(sampler.sample(1000) - 100 * Math.sin(2)) < 1e-10);
    assert.ok(Math.abs(sampler.sample(500) - 100 * Math.sin(1)) < 1e-10);
    assert.equal(JSON.stringify(data), before);
  } finally {sampler.dispose(); cleanup();}
});

test('Cables: 90 seeks em ordem reversa, entrada inválida e descarte', () => {
  const {runtime, cleanup} = load(); const sampler = createCablesSampler(runtime, fixture());
  try {
    for (let i = 89; i >= 0; i--) assert.ok(Math.abs(sampler.sample(i * 1000 / 30) - 100 * Math.sin(i / 30 * 2)) < 1e-10);
    for (const ms of [-1, NaN, Infinity]) assert.throws(() => sampler.sample(ms));
    sampler.dispose(); sampler.dispose(); assert.throws(() => sampler.sample(0));
  } finally {sampler.dispose(); cleanup();}
});
