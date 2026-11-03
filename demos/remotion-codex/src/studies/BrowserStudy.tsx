import React, {useLayoutEffect, useRef} from 'react';
import {AbsoluteFill, Html5Audio, staticFile, useCurrentFrame, useDelayRender, useVideoConfig} from 'remotion';

export type StudyMount = (host: HTMLDivElement, timeMs: number) => (() => void) | Promise<() => void>;

export const BrowserStudy: React.FC<{name: string; mount: StudyMount}> = ({name, mount}) => {
  const host = useRef<HTMLDivElement>(null);
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const {delayRender, continueRender, cancelRender} = useDelayRender();
  useLayoutEffect(() => {
    const element = document.createElement('div');
    Object.assign(element.style, {position: 'absolute', inset: '0'});
    host.current!.replaceChildren(element);
    const handle = delayRender(`Avaliar ${name} no frame ${frame}`);
    let disposed = false;
    let ready = false;
    let cleanup: (() => void) | undefined;
    const finish = () => { if (!ready) {ready = true; continueRender(handle);} };
    Promise.resolve().then(() => disposed ? undefined : mount(element, frame * 1000 / fps)).then((fn) => {
      if (typeof fn === 'function') {
        if (disposed) fn(); else cleanup = fn;
      }
      finish();
    }).catch((error) => { finish(); if (!disposed) cancelRender(error); });
    return () => {disposed = true; cleanup?.(); element.remove(); finish();};
  }, [frame, fps, mount, name, delayRender, continueRender, cancelRender]);
  return <AbsoluteFill style={{background: '#0b111c', color: '#eaf5fc', fontFamily: 'DejaVu Sans, sans-serif'}}>
    <Html5Audio src={staticFile('tone.wav')} volume={0.08} />
    <div ref={host} style={{position: 'absolute', inset: 0}} />
    <div style={{position: 'absolute', top: 22, left: 28, color: '#62f4c6', fontSize: 14, letterSpacing: 2}}>{name} / CODEX</div>
    <div style={{position: 'absolute', bottom: 20, left: 28, color: '#9aafc3', fontSize: 12}}>Avaliação por quadro · {frame} · {Math.round(frame * 1000 / fps)} ms</div>
  </AbsoluteFill>;
};
