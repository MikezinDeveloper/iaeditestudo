import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {create} from '@react-three/test-renderer';
import {Box3, Vector3, type Mesh, type Group} from 'three';
import {DreiScene} from '../src/studies/drei-scene.ts';

(globalThis as typeof globalThis & {IS_REACT_ACT_ENVIRONMENT: boolean}).IS_REACT_ACT_ENVIRONMENT = true;

test('Drei: RoundedBox finito e Center corrigem a posição de uma malha deslocada', async () => {
  let ready = 0;
  const renderer = await create(React.createElement(DreiScene, {timeMs: 0, onReady: () => {ready++;}}));
  try {
    assert.equal(ready, 1);
    const card = renderer.scene.findByProps({name: 'card'}).instance as Mesh;
    const center = renderer.scene.findByProps({name: 'center'}).instance as Group;
    assert.ok(card.geometry.getAttribute('position').count > 100);
    assert.ok(Array.from(card.geometry.getAttribute('normal').array).every(Number.isFinite));
    center.updateWorldMatrix(true, true);
    const box = new Box3().setFromObject(center, true);
    assert.ok(box.getCenter(new Vector3()).length() < 1e-5);
    assert.ok(box.getSize(new Vector3()).length() > 2);
  } finally {await renderer.unmount();}
});

test('Drei: remontar o frame após o fim preserva a transformação absoluta', async () => {
  const sample = async (timeMs: number) => {
    const renderer = await create(React.createElement(DreiScene, {timeMs, onReady: () => {}}));
    try {const group = renderer.scene.findByProps({name: 'motion'}).instance as Group; group.updateMatrix(); return [...group.matrix.elements];}
    finally {await renderer.unmount();}
  };
  const expected = await sample(1000);
  await sample(2966.6667);
  assert.deepEqual(await sample(1000), expected);
  assert.notDeepEqual(await sample(0), expected);
});
