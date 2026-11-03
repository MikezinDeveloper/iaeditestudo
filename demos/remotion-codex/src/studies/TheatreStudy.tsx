import React from 'react';
import {BrowserStudy, type StudyMount} from './BrowserStudy';
import state from './theatre-state.json';
import {createTheatreSampler} from './theatre-sampler';

const mount: StudyMount = async (host, timeMs) => {
  const sampler = await createTheatreSampler(state);
  const value = sampler.sample(timeMs / 1000);
  const card = document.createElement('div');
  Object.assign(card.style, {position: 'absolute', top: '50%', left: '50%', width: '120px', height: '120px', borderRadius: '24px', background: '#62f4c6', boxShadow: '0 0 50px #62f4c640', transform: `translate(-50%, -50%) translateX(${value.x}px) rotate(${value.angle}deg) scale(${value.scale})`});
  host.appendChild(card);
  return () => {sampler.dispose(); host.replaceChildren();};
};
export const TheatreStudy: React.FC = () => <BrowserStudy name="THEATRE.JS · ESTADO + KEYFRAMES" mount={mount} />;
