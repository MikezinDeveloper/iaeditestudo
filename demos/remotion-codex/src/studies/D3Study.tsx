import React from 'react';
import {select} from 'd3';
import {BrowserStudy, type StudyMount} from './BrowserStudy';
import data from './chart-data.json';
import {chartFrame} from './d3-layout';

const mount: StudyMount = (host, timeMs) => {
  const bars = chartFrame(data, Math.round(timeMs * 30 / 1000), 30);
  const svg = select(host).append('svg').attr('width', 640).attr('height', 360);
  const group = svg.append('g').attr('transform', 'translate(80,100)');
  group.selectAll<SVGRectElement, typeof bars[number]>('rect').data(bars, (d) => d.id).join('rect')
    .attr('x', (d) => d.x).attr('y', (d) => 170 - d.height).attr('width', (d) => d.width).attr('height', (d) => d.height).attr('rx', 6).attr('fill', '#62f4c6');
  group.selectAll<SVGTextElement, typeof bars[number]>('text').data(bars, (d) => d.id).join('text')
    .attr('x', (d) => d.x + d.width / 2).attr('y', 195).attr('text-anchor', 'middle').attr('fill', '#eaf5fc').attr('font-size', 14).text((d) => `${d.label} ${Math.round(d.displayedValue)}`);
  return () => {svg.remove();};
};
export const D3Study: React.FC = () => <BrowserStudy name="D3 · GRÁFICO DIRIGIDO POR DADOS" mount={mount} />;
