import React, {useMemo} from 'react';
import {AbsoluteFill, Html5Audio, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {sampleAnimeMotion} from './anime-motion';

export const AnimeMotionStudy: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const state = useMemo(() => sampleAnimeMotion(frame, fps), [frame, fps]);
  return (
    <AbsoluteFill style={{background: '#0b111c', color: '#edf5fa', fontFamily: 'DejaVu Sans, sans-serif', padding: 32}}>
      <Html5Audio src={staticFile('tone.wav')} volume={0.12} />
      <div style={{display: 'flex', justifyContent: 'space-between', color: '#62f4c6', fontSize: 12, letterSpacing: 2}}>
        <span>ANIME.JS × REMOTION</span><span>{String(frame).padStart(3, '0')} / 119</span>
      </div>
      <div style={{marginTop: 25, opacity: state.title.opacity, transform: `translateY(${state.title.y}px)`}}>
        <div style={{fontSize: 36, fontWeight: 800}}>Motion por quadro</div>
        <div style={{marginTop: 8, color: '#a4b6c8', fontSize: 14}}>timeline + stagger + easing · controle pelo Codex</div>
      </div>
      <div style={{display: 'flex', gap: 14, alignItems: 'flex-end', position: 'absolute', bottom: 86, left: 36, height: 95}}>
        {state.bars.map((bar, index) => (
          <div key={index} style={{width: 48, height: 35 + index * 9, borderRadius: '7px 7px 0 0', background: index === 3 ? '#edf5fa' : '#62f4c6', transformOrigin: 'bottom', opacity: bar.opacity, transform: `scaleY(${bar.scale})`}} />
        ))}
      </div>
      <svg width="568" height="32" style={{position: 'absolute', left: 36, bottom: 40}}>
        <path d="M0 16 H568" stroke="#23344a" strokeWidth="3" />
        <path d="M0 16 H568" stroke="#62f4c6" strokeWidth="3" pathLength="1" strokeDasharray="1" strokeDashoffset={1 - state.line.progress} />
      </svg>
      <div style={{position: 'absolute', right: 36, bottom: 88, color: '#91a3b7', fontSize: 11, textAlign: 'right', lineHeight: 1.8}}>
        {Math.round(frame * 1000 / fps)} ms<br />30 fps / 640 × 360
      </div>
    </AbsoluteFill>
  );
};
