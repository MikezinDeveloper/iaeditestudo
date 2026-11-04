import React, {useLayoutEffect} from 'react';
import {RoundedBox} from '@react-three/drei/core/RoundedBox.js';
import {Center} from '@react-three/drei/core/Center.js';

export const DreiScene = ({timeMs, onReady}: {timeMs: number; onReady: () => void}) => {
  if (!Number.isFinite(timeMs) || timeMs < 0) throw new Error('Tempo Drei inválido');
  useLayoutEffect(onReady, [onReady]);
  return React.createElement(React.Fragment, null,
    React.createElement('hemisphereLight', {args: [0xffffff, 0x303040, 2]}),
    React.createElement('directionalLight', {position: [3, 4, 5], intensity: 3}),
    React.createElement('group', {name: 'motion', rotation: [0.2, timeMs / 1000 * 0.8, 0.1]},
      React.createElement(Center, {name: 'center'},
        React.createElement(RoundedBox, {name: 'card', args: [2.4, 1.4, 0.6], radius: 0.15, smoothness: 4, bevelSegments: 3, position: [2, 1, 0]},
          React.createElement('meshStandardMaterial', {color: '#ad9bff', roughness: 0.3, metalness: 0.2})))));
};
