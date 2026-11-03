import React from 'react';
import {BrowserStudy, type StudyMount} from './BrowserStudy';

const mount: StudyMount = async (host, timeMs) => {
  const {default: Two} = await import('two.js');
  const two = new Two({width: 640, height: 360, type: Two.Types.svg, autostart: false}).appendTo(host);
  const circle = two.makeCircle(0, 0, 68);
  circle.noFill(); circle.stroke = '#62f4c6'; circle.linewidth = 5;
  const star = two.makeStar(0, 0, 22, 50, 5);
  star.fill = '#ad9bff'; star.noStroke();
  const line = two.makeLine(-110, 0, 110, 0);
  line.stroke = '#eaf5fc'; line.linewidth = 2;
  const group = two.makeGroup(circle, star, line);
  const seconds = timeMs / 1000;
  group.translation.set(320 + 80 * Math.sin(seconds * 2), 180);
  group.rotation = seconds * 0.8;
  star.rotation = -seconds * 2;
  circle.scale = 1 + 0.15 * Math.sin(seconds * 3);
  two.update();
  // Published 0.8.24 has release(), but lacks the HEAD's dispose() API.
  return () => {
    two.pause(); two.release(); two.unbind();
    const index = Two.Instances.indexOf(two);
    if (index >= 0) Two.Instances.splice(index, 1);
    two.renderer.domElement.remove();
  };
};
export const TwoStudy: React.FC = () => <BrowserStudy name="TWO.JS · CENA VETORIAL SVG" mount={mount} />;
