import React from 'react';
import {BrowserStudy, type StudyMount} from './BrowserStudy';
import {progressFromMilliseconds} from './clock';

const mount: StudyMount = async (host, timeMs) => {
  const {default: mojs} = await import('@mojs/core');
  const shape = new mojs.Shape({parent: host, shape: 'polygon', points: 6, fill: 'none', stroke: '#62f4c6', radius: {20: 80}, strokeWidth: {12: 2}, rotate: {0: 120}, duration: 2400, easing: 'cubic.inout', isShowStart: true, isShowEnd: true});
  const burst = new mojs.Burst({parent: host, count: 12, radius: {35: 125}, degree: 360, children: {shape: 'circle', radius: {10: 3}, fill: '#ad9bff', duration: 2400, easing: 'cubic.inout', isSwirl: false, degreeShift: 0, isShowStart: true, isShowEnd: true}});
  const timeline = new mojs.Timeline().add(shape, burst);
  timeline.setProgress(0).setProgress(progressFromMilliseconds(timeMs, 2400));
  return () => {timeline.pause(); host.replaceChildren();};
};

export const MojsStudy: React.FC = () => <BrowserStudy name="MO.JS · SHAPE + BURST" mount={mount} />;
